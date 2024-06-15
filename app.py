import pandas as pd
import numpy as np
import pycountry


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load the data
df = pd.read_csv('output.csv', sep= ';')


df.rename(columns={'Entity': 'Country', 'Year': 'Year', 'diabetes': 'Diabetes', 'obesity': 'Obesity', 'calories': 'Consumption'}, inplace=True)
# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"

server = app.server 
# Descriptions for each variable
variable_descriptions = {
    "Diabetes": "Diabetes is a chronic (long-lasting) health condition that affects how your body turns food into energy. "
                "The prevalence of diabetes refers to the percentage of the population that has been diagnosed with diabetes.",
    "Obesity": "Obesity is a complex disease involving an excessive amount of body fat. "
               "The prevalence of obesity refers to the percentage of the population that is considered obese.",
    "Consumption": "Daily supply of calories per person. Measured in kilocalories per person per day. "
                   "This indicates the calories that are available for consumption, but does not necessarily measure the number of calories actually consumed, since it does not factor in consumer waste."
}

color_scales = {
    "Diabetes": px.colors.sequential.Viridis,
    "Obesity": px.colors.sequential.Bluyl_r,
    "Consumption": px.colors.sequential.PuBu
}

variables_in_percent = ["Diabetes", "Obesity"]

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # Header
    html.Div([
        html.Img(src='https://i.goopics.net/slfuw3.png', style={'height': '40px', 'margin-right': '10px'}),
            html.H1("Diabetes Mellitus Evolution", style={'display': 'inline-block', 'margin': '0', 'color': 'white'}),
        html.Div([
            html.Button("Map", id='map_button', style={
                'background-color': 'rgb(143, 210, 66)',
                'color': 'white',
                'border': 'none',
                'padding': '12px 22px',
                'margin': '0 10px',
                'cursor': 'pointer',
                'borderRadius': '5px'
            }),
            html.Button("Table", id='table_button', style={
                'background-color': 'rgb(143, 210, 66)',
                'color': 'white',
                'border': 'none',
                'padding': '12px 22px',
                'margin': '0 10px',
                'cursor': 'pointer',
                'borderRadius': '5px'
            }),
        ], style={'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '20px', 'background-color': 'rgb(48,47,47)', 'borderBottom': '2px solid #dcdcdc'}),
   
    # Content will be rendered here
    html.Div(id='page_content')
], style={
    'width': '100%',
    'font-family': 'Helvetica, Arial, sans-serif',
    'display': 'inline-block',
    'verticalAlign': 'top',
    'backgroundColor': 'black',
    'padding': '10px'
})

# Define the content for the Map page
map_layout = html.Div([
    # Select Variable section
    html.Div([
        dcc.Tabs(
            id='variable_selector_tabs',
            value='Diabetes',
            children=[
                dcc.Tab(label='Diabetes', value='Diabetes', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                        selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
                dcc.Tab(label='Obesity', value='Obesity', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                        selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
                dcc.Tab(label='Consumption', value='Consumption', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                        selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
            ],
            style={
                'backgroundColor': 'bleu',
                'borderRadius': '5px'
            },
        ),
        # Wrap variable description and switch button in a flex container
        html.Div([
            html.P(id='variable_description', style={
                'flex': '0 1 70%',
                'margin-top': '20px',
                'color': '#34495e',
                'padding': '10px',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '10px',
                'font-size': '12px',  # Smaller font size
                'font-weight': 'bold',  # Bold text
                'font-style': 'italic',  # Italic text
                'margin-left': '5px',
            }),
            html.Button("Switch Projection", id="switch_projection", n_clicks=0, style={
                'flex': '0 1 auto',
                'margin-left': 'auto',
                'margin-right': '20px',
                'margin-top': '10px',
                'background-color': 'rgb(39,93,238)',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'cursor': 'pointer',
                'borderRadius': '5px'
            })
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.H3(id='map_title', style={'textAlign': 'center', 'color': '#4995ff'}),
        dcc.Graph(id='map', style={
            'padding': '10px'
        }),
        dcc.Slider(
            id='year_slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].min(),
            marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
            step=None,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag'  # This updates the figure while dragging
        )
    ], style={
        'width': '100%',
        'display': 'inline-block',
        'verticalAlign': 'top',
        'padding': '0px',
        'backgroundColor': 'rgb(66,64,64)',
        'borderRadius': '10px',
        'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
    }),
    # Map section
    # Country Graph section (outside Select Variable and Map sections)
    html.Div([
        html.H3(id='country_graph_title', style={'textAlign': 'center', 'color': 'rgb(73, 149, 255)'}),
        dcc.Graph(id='country_graph', style={
            'margin-top': '20px',
            'backgroundColor': '#ffffff',
            'borderRadius': '10px',
            'padding': '10px',
            'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
        }),
        html.P(id='country_graph_text', style={
            'textAlign': 'center',
            'color': 'white',
            'padding': '10px',
            'backgroundColor': 'rgb(48,47,47)',
            'borderRadius': '10px',
            'margin-top': '20px'
        })
    ], id='country_graph_container', style={'display': 'none', 'width': '95%', 'padding': '20px', 'backgroundColor': '#black', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
])

# Define the content for the Table page
table_layout = html.Div([
    dcc.Tabs(
        id='table_variable_selector',
        value='Diabetes',
        children=[
            dcc.Tab(label='Diabetes', value='Diabetes', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                    selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
            dcc.Tab(label='Obesity', value='Obesity', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                    selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
            dcc.Tab(label='Consumption', value='Consumption', style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': 'rgba(0, 107, 254, 0.48)', 'color': '#ffffff'},
                    selected_style={'padding': '10px', 'border-radius': '10px', 'backgroundColor': '#006BFE', 'color': '#ffffff'}),
        ],
        style={
            'backgroundColor': 'bleu',
            'borderRadius': '5px'
        },
    ),
    dcc.Dropdown(
        id='country_selector',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        multi=True,
        placeholder="Select countries",
        style={'margin-top': '10px'},
        className='custom-dropdown'
    ),
    dcc.Dropdown(
        id='year_selector',
        options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
        multi=True,
        placeholder="Select years",
        style={'margin-top': '10px'},
        className='custom-dropdown'
    ),
    html.H3(id='table_title', style={'textAlign': 'center', 'color': 'rgb(73, 149, 255)'}),
    dash_table.DataTable(
        id='table',
        style_table={'height': '400px', 'overflowY': 'auto', 'border': '1px solid #dddddd', 'borderRadius': '10px', 'width': '100%'},
        style_header={'backgroundColor': 'rgb(0 146 255 / 69%)', 'fontWeight': 'bold', 'color': 'black'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'whiteSpace': 'normal', 'height': 'auto', 'border': '1px solid #dddddd'},
        style_data={'backgroundColor': '#f3f3f3', 'border': '1px solid #dddddd'}
    ),
    html.Button("Download Data", id="btn_csv", style={
        'margin-top': '20px',
        'background-color': 'rgb(39, 93, 238)',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'cursor': 'pointer',
        'borderRadius': '5px'
    }),
    dcc.Download(id="download-dataframe-csv")
], style={
    'padding': '20px',
    'backgroundColor': 'rgb(66,64,64)',
    'borderRadius': '10px',
    'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
})

# Callback to navigate between pages
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

# Callback to update the content based on the selected page
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

# Callback to update the variable description
@app.callback(
    Output('variable_description', 'children'),
    [Input('variable_selector_tabs', 'value')]
)
def update_description(selected_variable):
    return variable_descriptions[selected_variable]

# Callback to update the map
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

    # Custom hover text with "Click on me" in red
    unit = "%" if selected_variable in variables_in_percent else "kcal"
    filtered_df['hover_text'] = filtered_df.apply(
        lambda row: f"<span style='font-size:15px;'><b>{row['Country']}</b></span><br><br><b>{selected_variable}: {round(row[selected_variable], 2) if selected_variable in variables_in_percent else int(row[selected_variable])}{unit}</b><br><span style='color:rgb(143, 210, 66);'>Click on me</span>", axis=1
    )

    fig = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode='country names',
        color=selected_variable,
        hover_name="Country",
        hover_data={'hover_text': True, 'Country': False, selected_variable: False},  # Use custom hover text
        color_continuous_scale=color_scales[selected_variable],  # Use the appropriate color scale
        projection=projection_type,
        custom_data=['hover_text']
    )
   
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        font=dict(color="white" ),
        paper_bgcolor="rgb(66, 64, 64)",  # Set the background color of the entire figure
        plot_bgcolor="rgb(66, 64, 64)",   # Set the plot area background color
        geo=dict(
            bgcolor='rgb(66, 64, 64)'  # Set the background color of the geo area
        )
    )

    # Update hover template
    fig.update_traces(hovertemplate="%{customdata[0]}")

    if selected_variable in variables_in_percent:
        title = f'{selected_variable} in {selected_year} (in %)'
    else:
        title = f'{selected_variable} in {selected_year} (in kcal)'

    map_title = title

    if clickData is None:
        return fig, map_title, {'display': 'none'}, ""

    country = clickData['points'][0]['location']
    if selected_variable in variables_in_percent:
        title = f'{selected_variable} in {country} over Time (in %)'
    else:
        title = f'{selected_variable} in {country} over Time (in kcal)'

    return fig, map_title, {'display': 'block'}, title

# Callback to update the country graph
@app.callback(
    Output('country_graph', 'figure'),
    Output('country_graph_text', 'children'),
    [Input('map', 'clickData'), Input('variable_selector_tabs', 'value')]
)
def update_country_graph(clickData, selected_variable):
    if clickData is None:
        return go.Figure(), ""
    
    country = clickData['points'][0]['location']
    country_df = df[df['Country'] == country]
    
    # Calculate the yearly change
    country_df['yearly_change'] = country_df[selected_variable].diff()
    avg_change = country_df['yearly_change'].mean()
    
    # Separate current and predicted data
    current_data = country_df[country_df['Year'] < 2022]
    predicted_data = country_df[country_df['Year'] >= 2022]
    
    fig = go.Figure()
    
    # Define rounding function
    if selected_variable in variables_in_percent:
        round_value = lambda x: round(x, 2)
        change_unit = "%"
    else:
        round_value = lambda x: int(x)
        change_unit = "kcal"
    
    # Plot current data
    fig.add_trace(go.Scatter(
        x=current_data['Year'], 
        y=current_data[selected_variable].apply(round_value),
        mode='lines+markers', 
        name='Prevalence',
        line=dict(color='red'),
        marker=dict(color='red')
    ))
    
    # Plot predicted data
    fig.add_trace(go.Scatter(
        x=predicted_data['Year'], 
        y=predicted_data[selected_variable].apply(round_value),
        mode='lines+markers', 
        name='Prediction',
        line=dict(color='orange'),
        marker=dict(color='orange')
    ))

    # Connect current and predicted data
    if not current_data.empty and not predicted_data.empty:
        connection_line = go.Scatter(
            x=[current_data['Year'].iloc[-1], predicted_data['Year'].iloc[0]],
            y=[current_data[selected_variable].apply(round_value).iloc[-1], predicted_data[selected_variable].apply(round_value).iloc[0]],
            mode='lines', 
            line=dict(color='#EC745A'),
            showlegend=False
        )
        fig.add_trace(connection_line)
    
    if selected_variable in variables_in_percent:
        title = f'Prevalence of {selected_variable} in {country} among adults over Time'
        yaxis_title = f'{selected_variable}'
        yaxis = dict(ticksuffix='%')
    else:
        title = f'Prevalence of {selected_variable} in {country} among adults over Time'
        yaxis_title = f'{selected_variable} (kcal)'
        yaxis = dict(ticksuffix='kcal')

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=yaxis_title,
        yaxis=yaxis,
        paper_bgcolor="white",
        legend_title_text=' '
    )

    if selected_variable in variables_in_percent:
        trend = "increasing" if avg_change > 0 else "decreasing"
        explanation_text = (f"In {country}, the average yearly change in {selected_variable.lower()} among adults is "
                            f"{round(avg_change, 2)} percentage points, indicating a {trend} trend over the years. ")
    else:
        trend = "increasing" if avg_change > 0 else "decreasing"
        explanation_text = (f"In {country}, the average yearly change in {selected_variable.lower()} among adults is "
                            f"{int(avg_change)} kcal, indicating a {trend} trend over the years. ")

    return fig, explanation_text

# Callback to update the table
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('table_title', 'children'),
    [Input('table_variable_selector', 'value'),
     Input('country_selector', 'value'),
     Input('year_selector', 'value')]
)
def update_table(selected_variable, selected_countries, selected_years):
    filtered_df = df.copy()
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

    filtered_df = filtered_df.groupby(['Country', 'Year'], as_index=False).agg({selected_variable: 'mean'})
    
    table_df = filtered_df.pivot(index='Country', columns='Year', values=selected_variable).reset_index()
    table_df = table_df.round(2)
    
    columns = [{"name": str(i), "id": str(i)} for i in table_df.columns]
    data = table_df.to_dict('records')
    
    if selected_variable in variables_in_percent:
        title = f'Table of {selected_variable} Data (in %)'
    else:
        title = f'Table of {selected_variable} Data (in kcal)'
    
    return data, columns, title

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks")],
    [State('table_variable_selector', 'value'),
     State('country_selector', 'value'),
     State('year_selector', 'value')],
    prevent_initial_call=True,
)
def download_csv(n_clicks, selected_variable, selected_countries, selected_years):
    filtered_df = df.copy()
    
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    
    if selected_years:
        filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
    
    table_df = filtered_df.pivot(index='Country', columns='Year', values=selected_variable).reset_index()
    return dcc.send_data_frame(table_df.to_csv, f"{selected_variable}_data.csv")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)