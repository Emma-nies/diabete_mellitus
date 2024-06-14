import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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
