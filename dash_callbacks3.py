import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv('data/mpg.csv')

app = dash.Dash()

# Create a list of features to work with
features = df.columns

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='x-dropdown',
            options=[
                {'label':i,'value':i} for i in features
            ],
            value='displacement'
        )
    ],
    style=dict(
        width='48%',
        display='inline-block'
    )),
    html.Div([
        dcc.Dropdown(
            id='y-dropdown',
            options=[
                {'label':i,'value':i} for i in features
            ],
            value='mpg'
        )
    ],
    style=dict(
        width='48%',
        display='inline-block'
    )),
    dcc.Graph(
        id='feature-graphic'
    )
],
style=dict(
    padding=10
))


@app.callback(
    Output('feature-graphic', 'figure'),
    [
        Input('x-dropdown', 'value'),
        Input('y-dropdown', 'value')
    ]
)
def update_graph(xaxis, yaxis):
    return dict(
        data=[
            go.Scatter(
                x=df[xaxis],
                y=df[yaxis],
                text=df['name'],
                mode='markers',
                marker=dict(
                    size=15,
                    opacity=0.5,
                    line=dict(
                        width=0.5,
                        color='white'
                    )
                )
            )
        ],
        layout=go.Layout(
            title='Dashboard for MPG data',
            xaxis=dict(
                title=xaxis
            ),
            yaxis=dict(
                title=yaxis
            ),
            hovermode='closest'
        )
    )


if __name__ == '__main__':
    app.run_server()