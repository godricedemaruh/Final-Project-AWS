import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import regex
import numpy as np
import country_converter as coco
import pycountry
import os


file_path = os.path.join(os.getcwd(), "data")


def load_data(filename, file_path=file_path):
    csv_path = os.path.join(file_path, filename)
    return pd.read_csv(csv_path)

en_df = load_data('world_map_re.csv')
co2_df = load_data("co2_plot_df.csv")
polls = load_data('pollutants.csv')


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server




fig_re = px.scatter_geo(en_df, locations="iso_code", color_discrete_sequence=["green"],
                 hover_name="Country", size="all_renew_electricity",
                 animation_frame="Year",
                 projection="natural earth", width=1200, height=800, size_max=70,
                     title='Electricity with renewable energy [TWh]')
fig_re.update_layout(
    title={
        'text': "Electricity with renewable energy [TWh]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})



co2_df = co2_df.query('Country_1!="International Aviation "').query('Country_1!="International Shipping "')
name_list = co2_df['Country_1'].tolist()
Country_list_names = coco.convert(names=name_list, to='name_short')
co2_df['Country'] = Country_list_names
co2_df = co2_df.drop(columns={'Country_1'})
iso_list = coco.convert(names=Country_list_names, to='ISO3')
co2_df['iso_3'] = iso_list

fig_co2 = px.scatter_geo(co2_df, locations="iso_3", color_discrete_sequence=["red"],
                     size="CO2_Mton",
                     animation_frame="Year",
                     projection="natural earth", width=1200, height=800, size_max=60,
                         title='CO2-Emissions [Mton]')
fig_co2.update_layout(
    title={
        'text': "CO2-Emissions [Mton]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


polls.drop(columns={'Unnamed: 0'}, inplace=True)
polls = polls.query('year<=2020').fillna(0)
polls = polls[['year', 'iso_code', 'average_m', 'average_c', 'average_o', 'average_n']]
polls.rename(columns={"average_m": "average_methane", "average_c": "average_carbonmonoxide", "average_o":"average_ozone", "average_n":"average_nitrogendioxide"}, inplace=True)

fig_co = px.scatter_geo(polls, locations="iso_code", color_discrete_sequence=["grey"],
                     size="average_carbonmonoxide",
                     animation_frame="year",
                     projection="natural earth", width=1200, height=800, size_max=20,
                         title='Carbonmonoxide [mol/m2]')
fig_co.update_layout(
    title={
        'text': "Carbonmonoxide [mol/m2]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


fig_m = px.scatter_geo(polls, locations="iso_code", color_discrete_sequence=["grey"],
                     size="average_methane",
                     animation_frame="year",
                     projection="natural earth", width=1200, height=800, size_max=20,
                         title='Methane [mol/m2]')
fig_m.update_layout(
    title={
        'text': "PMethane [mol/m2]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


fig_o = px.scatter_geo(polls, locations="iso_code", color_discrete_sequence=["grey"],
                     size="average_ozone",
                     animation_frame="year",
                     projection="natural earth", width=1200, height=800, size_max=20,
                         title='Ozone [mol/m2]')
fig_o.update_layout(
    title={
        'text': "Ozone [mol/m2]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})


fig_n = px.scatter_geo(polls, locations="iso_code", color_discrete_sequence=["grey"],
                     size="average_nitrogendioxide",
                     animation_frame="year",
                     projection="natural earth", width=1200, height=800, size_max=20,
                         title='Nitrogendioxide [mol/m2]')
fig_n.update_layout(
    title={
        'text': "Nitrogendioxide [mol/m2]",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig_n.show()



app.layout = html.Div(children=[
    html.Div([
        html.H1(children='RECO2 Maps'),
        html.H2(children="A web application to show the global growth of electricity production with Renewable Energy in relation to the growth of CO2-emissions. 'RECO2'"),
        html.H5("by Andreas Ueberschaer"),

        html.Div(children='''
            World Map displaying the growth of electricity production with renewable energy.
        '''),

        dcc.Graph(
            id='fig_re',
            figure=fig_re
        ),  
    ]),

    html.Div([
        
        html.Div(children='''
            World Map displaying the growth of CO2-emissions.
        '''),
        
        dcc.Graph(
            id='fig_co2',
            figure=fig_co2
        ),  
    ]),
    
    html.Div([
        
        html.H5(children="World Map displaying the growth of some pollutions"),
        html.Div(children='''
            World Map displaying the growth of carbonmonoxide-emissions.
        '''),
        
        dcc.Graph(
            id='fig_co',
            figure=fig_co
        ),  
    ]),
    
    html.Div([
        
        html.Div(children='''
            World Map displaying the growth of methane-emissions.
        '''),
        
        dcc.Graph(
            id='fig_m',
            figure=fig_m
        ),  
    ]),
    
    html.Div([
        
        html.Div(children='''
            World Map displaying the growth of ozone-emissions.
        '''),
        
        dcc.Graph(
            id='fig_o',
            figure=fig_o
        ),  
    ]),
    
    html.Div([
        
        html.Div(children='''
            World Map displaying the growth of nitrogendioxide-emissions.
        '''),
        
        dcc.Graph(
            id='fig_n',
            figure=fig_n
        ),  
    ]),
])


if __name__ == "__main__":
    app.run_server(debug=True)