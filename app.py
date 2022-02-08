# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import regex
import numpy as np
import country_converter as coco
from selenium import webdriver
from selenium.webdriver.common.by import By
import pycountry

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

urlfile = 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'
data_en = pd.read_csv(urlfile)

def start_pipeline(data): 
    return data.copy()

def df_re_creation(data):
    data.rename(columns={"year":"Year", "country":"Country"}, inplace=True)
    data_biofuel = data.filter(regex='biofuel_electricity')
    data_hydro = data.filter(regex='hydro_electricity')
    data_o_renew = data.filter(regex='other_renewable_electricity')
    data_renew = data.filter(regex='renewables_electricity')
    data_solar = data.filter(regex='solar_electricity')
    data_wind = data.filter(regex='wind_electricity')
    data_sev_values = data.filter(['iso_code', 'Country', 'Year', 'electricity_generation', 'primary_energy_consumption'])
    data = data_sev_values.join(data_wind.join(data_biofuel.join(data_solar.join(data_hydro.join(data_o_renew.join(data_renew))))))
    data = data.query('Year>=2000').query('Country!="World"').reset_index()
    arr = np.array(np.where(pd.isnull(data.filter(['iso_code', 'Country'])))).tolist()
    arr_list = arr[0]
    data = data.drop(axis=0, index=arr_list).reset_index()
    data = data.drop(columns={'level_0', 'index'})
    data.fillna(0, inplace=True)
    data = data.assign(all_renew_electricity = round((data.other_renewable_electricity + data.renewables_electricity),2))
    return data

def world_map_re(data):
    fig = px.scatter_geo(data, locations="iso_code", color_discrete_sequence=["green"],
                     hover_name="Country", size="all_renew_electricity",
                     animation_frame="Year",
                     projection="natural earth", width=1200, height=800, size_max=70,
                         title='Electricity with renewable energies [TWh]')
    fig.update_layout(
        title={
            'text': "Electricity with renewable energies [TWh]",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig.show()

def co2_plot_df():
    url = "https://edgar.jrc.ec.europa.eu/report_2021#emissions_table"
    driver = webdriver.Chrome()
    driver.get(url)
    test_text = driver.find_element(By.CLASS_NAME, "ecl-table__body").find_element(By.CSS_SELECTOR, 'tr:nth-child(3)').text
    test_list = [td.text for td in driver.find_elements(By.XPATH, "//tbody[@class='ecl-table__body']/tr")]
    CO2_Mton = []
    for j in range(2, len(test_list)):
        for i in range(len(test_list[j].split(' ')[-8:-1])):
            if ',' in test_list[j].split(' ')[-8:-1][i]:
                CO2_Mton.append(test_list[j].split(' ')[-8:-1][i].replace(',',''))
            else: CO2_Mton.append(test_list[j].split(' ')[-8:-1][i])
    Country = []
    for j in range(2, len(test_list)):
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
        Country.append(regex.findall("^(.+?)(?=\\d).*", test_list[j])[0])
    for i in range(len(Country)):
        if Country[i] == 'Congo ':
            Country[i] = 'COG'
        elif Country[i] == 'France and Monaco ':
            Country[i] = 'France'
        elif Country[i] == 'Israel and Palestine, State of ':
            Country[i] = 'Israel'
        elif Country[i] == 'Italy, San Marino and the Holy See ':
            Country[i] = 'Italy'
        elif Country[i] == 'Serbia and Montenegro ':
            Country[i] = 'SRB'
        elif Country[i] == 'Spain and Andorra ':
            Country[i] = 'Spain'
        elif Country[i] == 'Switzerland and Liechtenstein ':
            Country[i] = 'Switzerland'
    year_list = [1990, 2000, 2005, 2010, 2015, 2019, 2020]
    Year = []
    for j in range(2, len(test_list)):
        for years in year_list:
            Year.append(years)
    co2_df_plotly = pd.DataFrame({'Country_1':Country, 'Year':Year, 'CO2_Mton':CO2_Mton})
    co2_df_plotly['CO2_Mton'] = pd.to_numeric(co2_df_plotly['CO2_Mton'], downcast="float")
    return co2_df_plotly

def plotly_fct(data):
    data = data.query('Country_1!="International Aviation "').query('Country_1!="International Shipping "')
    name_list = data['Country_1'].tolist()
    Country_list_names = coco.convert(names=name_list, to='name_short')
    data['Country'] = Country_list_names
    data = data.drop(columns={'Country_1'})
    iso_list = coco.convert(names=Country_list_names, to='ISO3')
    data['iso_3'] = iso_list
    fig = px.scatter_geo(data, locations="iso_3", color_discrete_sequence=["red"],
                         size="CO2_Mton",
                         animation_frame="Year",
                         projection="natural earth", width=1200, height=800, size_max=60,
                             title='CO2-Emissions [Mton]')
    fig.update_layout(
        title={
            'text': "CO2-Emissions [Mton]",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig.show()

fig_re = data_en.pipe(start_pipeline).pipe(df_re_creation).pipe(world_map_re)
fig_co2 = co2_plot_df().pipe(plotly_fct)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='renewable energy',
            figure=fig_re
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='greenhouse gas',
            figure=fig_co2
        ),  
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)