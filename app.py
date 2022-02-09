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

world_map_en_df = load_data('world_map_re.csv')
co2_df = load_data("co2_plot_df.csv")


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.config.suppress_callback_exceptions = True



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


fig_re = world_map_re(world_map_en_df)
fig_co2 = plotly_fct(co2_df)

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='RECO2 Maps'),
        html.H2(children="A web application to show the global growth of electricity production with Renewable Energies in relation to the growth of CO2-emissions. 'RECO2'"),
        html.H4("by Andreas Ueberschaer"),

        html.Div(children='''
            World Map displaying the growth of electricity production with renewable energies.
        '''),

        dcc.Graph(
            id='renewable energy',
            figure=fig_re
        ),  
    ]),
    html.Div([
        
        html.Div(children='''
            World Map displaying the growth of CO2-emissions.
        '''),
        
        dcc.Graph(
            id='greenhouse gas',
            figure=fig_co2
        ),  
    ]),
])


if __name__ == "__main__":
    app.run_server(debug=True)