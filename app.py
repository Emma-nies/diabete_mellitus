import pandas as pd
import numpy as np
import pycountry

# Générer des données simulées
countries = [country.name for country in pycountry.countries]
years = list(range(2003, 2023))

data = {
    "Country": [],
    "Year": [],
    "Diabetes": [],
    "Obesity": [],
    "Overconsumption": []
}

for country in countries:
    for year in years:
        data["Country"].append(country)
        data["Year"].append(year)
        data["Diabetes"].append(np.random.uniform(3, 15))
        data["Obesity"].append(np.random.uniform(10, 40))
        data["Overconsumption"].append(np.random.uniform(50, 200))

df = pd.DataFrame(data)
df.to_csv('prevalence_data.csv', index=False)

# Importer Dash
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go

# Charger les données
df = pd.read_csv('prevalence_data.csv')

# Initialiser l'application Dash
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"
server = app.server

# Définir le layout de l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # Header
    html.Div([
        html.H1("Global Health Dashboard", style={'display': 'inline-block', 'margin': '0', 'color': '#2c3e50'}),
        html.Div([
            html.Button("Map", id='map_button', style={
                'background-color': '#1abc9c',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'margin': '0 10px',
                'cursor': 'pointer',
                'borderRadius': '5px'
            }),
            html.Button("Table", id='table_button', style={
                'background-color': '#1abc9c',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'margin': '0 10px',
                'cursor': 'pointer',
                'borderRadius': '5px'
            }),
        ], style={'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '20px', 'background-color': '#ffffff', 'borderBottom': '1px solid #dcdcdc'}),
    
    # Content
    html.Div(id='page_content')
], style={
    'font-family': 'Helvetica, Arial, sans-serif',
    'backgroundColor': '#ecf0f1',
    'padding': '20px'
})

# Définir les layouts pour les différentes pages
map_layout = html.Div([
    html.H3("Select Variable", style={'margin-top': '10px', 'color': '#16a085'}),
    dcc.Tabs(
        id='variable_selector_tabs',
        value='Diabetes',
        children=[
            dcc.Tab(label='Diabetes', value='Diabetes', style={'padding': '10px'}),
            dcc.Tab(label='Obesity', value='Obesity', style={'padding': '10px'}),
            dcc.Tab(label='Overconsumption', value='Overconsumption', style={'padding': '10px'}),
        ],
        style={'backgroundColor': '#ecf0f1', 'borderRadius': '5px'}
    ),
    html.Div([
        html.P(id='variable_description', style={
            'flex': '0 1 70%',
            'margin-top': '10px',
            'color': '#34495e',
            'padding': '10px',
            'backgroundColor': '#ecf0f1',
            'borderRadius': '10px'
        }),
        html.Button("Switch Projection", id="switch_projection", n_clicks=0, style={
            'flex': '0 1 auto',
            'margin-left': 'auto',
            'margin-right': '20px',
            'margin-top': '10px',
            'background-color': '#1abc9c',
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'cursor': 'pointer',
            'borderRadius': '5px'
        })
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.H3(id='map_title', style={'textAlign': 'center', 'color': 'red'}),
    dcc.Graph(id='map', style={'padding': '10px'}),
    dcc.Slider(
        id='year_slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=None,
        tooltip={"placement": "bottom", "always_visible": True}
    )
], style={
    'width': '100%',
    'display': 'inline-block',
    'verticalAlign': 'top',
    'padding': '20px',
    'backgroundColor': '#ffffff',
    'borderRadius': '10px',
    'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
})

table_layout = html.Div([
    html.H3("Select Variable", style={'margin-top': '10px', 'color': '#16a085'}),
    dcc.Tabs(
        id='table_variable_selector',
        value='Diabetes',
        children=[
            dcc.Tab(label='Diabetes', value='Diabetes', style={'padding': '10px'}),
            dcc.Tab(label='Obesity', value='Obesity', style={'padding': '10px'}),
            dcc.Tab(label='Overconsumption', value='Overconsumption', style={'padding': '10px'}),
        ],
        style={'backgroundColor': '#ecf0f1', 'borderRadius': '5px'}
    ),
    html.H3(id='table_title', style={'textAlign': 'center', 'color': '#16a085'}),
    dash_table.DataTable(
        id='table',
        style_table={'height': '400px', 'overflowY': 'auto', 'border': '1px solid #dddddd', 'borderRadius': '10px', 'width': '100%'},
        style_header={'backgroundColor': '#16a085', 'fontWeight': 'bold', 'color': 'white'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'whiteSpace': 'normal', 'height': 'auto', 'border': '1px solid #dddddd'},
        style_data={'backgroundColor': '#f3f3f3', 'border': '1px solid #dddddd'}
    ),
    html.Button("Download Data", id="btn_csv", style={
        'margin-top': '20px',
        'background-color': '#1abc9c',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'cursor': 'pointer',
        'borderRadius': '5px'
    }),
    dcc.Download(id="download-dataframe-csv")
], style={
    'padding': '20px',
    'backgroundColor': '#f7f9f9',
    'borderRadius': '10px',
    'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
})

# Définir les callbacks
@app.callback(
    Output('url', 'pathname'),
    [Input('map_button', 'n_clicks'),
     Input('table_button', 'n_clicks')]
)
def display_page(map_clicks, table_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '/'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'map_button':
        return '/map'
    elif button_id == 'table_button':
        return '/table'
    else:
        return '/'

@app.callback(
    Output('page_content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/map':
        return map_layout
    elif pathname == '/table':
        return table_layout
    else:
        return map_layout

@app.callback(
    Output('variable_description', 'children'),
    [Input('variable_selector_tabs', 'value')]
)
def update_description(selected_variable):
    return variable_descriptions[selected_variable]

@app.callback(
    Output('map', 'figure'),
    Output('map_title', 'children'),
    Output('country_graph_container', 'style'),
    Output('country_graph_title', 'children'),
    [Input('variable_selector_tabs', 'value'), Input('year_slider', 'value'), Input('map', 'clickData'), Input('switch_projection', 'n_clicks')]
)
def update_map(selected_variable, selected_year, clickData, n_clicks):
    filtered_df = df[df['Year'] == selected_year]
    projection_type = "orthographic" if n_clicks % 2 == 1 else "equirectangular"
    fig = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode='country names',
        color=selected_variable,
        hover_name="Country",
        color_continuous_scale=color_scales[selected_variable],
        projection=projection_type
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="red"
    )
    map_title = f'{selected_variable} in {selected_year}'
    if clickData is None:
        return fig, map_title, {'display': 'none'}, ""
    country = clickData['points'][0]['location']
    title = f'{selected_variable} in {country} over Time'
    return fig, map_title, {'display': 'block'}, title

@app.callback(
    Output('country_graph', 'figure'),
    [Input('map', 'clickData'), Input('variable_selector_tabs', 'value')]
)
def update_country_graph(clickData, selected_variable):
    if clickData is None:
        return go.Figure()
    country = clickData['points'][0]['location']
    country_df = df[df['Country'] == country]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=country_df['Year'], y=country_df[selected_variable],
                             mode='lines+markers', name=country,
                             marker=dict(color='#1abc9c')))
    fig.update_layout(title=f'{selected_variable} in {country} over Time',
                      xaxis_title='Year',
                      yaxis_title=selected_variable,
                      paper_bgcolor="#ecf0f1")
    return fig

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table_title', 'children'),
    [Input('table_variable_selector', 'value')]
)
def update_table(selected_variable):
    table_df = df.pivot(index='Country', columns='Year', values=selected_variable).reset_index()
    table_df = table_df.round(2)
    columns = [{"name": str(i), "id": str(i)} for i in table_df.columns]
    data = table_df.to_dict('records')
    title = f'Table of {selected_variable} Data'
    return data, columns, title

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks")],
    [State('table_variable_selector', 'value')],
    prevent_initial_call=True,
)
def download_csv(n_clicks, selected_variable):
    table_df = df.pivot(index='Country', columns='Year', values=selected_variable).reset_index()
    return dcc.send_data_frame(table_df.to_csv, f"{selected_variable}_data.csv")

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
