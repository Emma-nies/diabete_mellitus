import pandas as pd
import numpy as np
import pycountry


# Get list of all countries
countries = [country.name for country in pycountry.countries]
years = list(range(2003, 2023))


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load the data
df = pd.read_csv('prevalence_data.csv')


# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"


server = app.server  # C'est la ligne à ajouter pour que Gunicorn puisse trouver le serveur

app.layout = html.Div([
    dcc.Input(id='input', value='initial value', type='text'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_output_div(input_value):
    return f'You\'ve entered "{input_value}"'

if __name__ == '__main__':
    app.run_server(debug=True)
