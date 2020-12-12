import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('data/gapminderDataFiveYear.csv')

app = dash.Dash()

# Create dictionary of years for the callback input
year_options = []
for year in df['year'].unique():
    year_options.append(
        dict(
            label=str(year),
            value=year
        )
    )

app.layout = html.Div([
    dcc.Graph(
        id='graph'
    ),
    dcc.Dropdown(
        id='year-picker',
        options=year_options,
        value=df['year'].min()
    )
])

@app.callback(
    Output('graph', 'figure'),
    [Input('year-picker', 'value')]
)
def update_figure(selected_year):
    filtered_df = df[df['year'] == selected_year]
    traces = []
    for continent in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent']==continent]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            mode='markers',
            opacity=0.7,
            marker=dict(
                size=15
            ),
            name=continent
        ))
    return dict(
        data=traces,
        layout=go.Layout(
            title='Life Expenctancy vs GDP',
            xaxis=dict(
                title='GDP per Capita',
                type='log'
            ),
            yaxis=dict(
                title='Life Expectancy'
            )
        )
    )

if __name__ == '__main__':
    app.run_server()