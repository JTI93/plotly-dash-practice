import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from numpy import random

app = dash.Dash()

df = pd.read_csv('data/mpg.csv')

# Use the random module to add some jitter to graph
df['year'] = random.randint(-2, 3, len(df))*0.1 + df['model_year']

app.layout = html.Div(
    [
        html.Div(
            dcc.Graph(
                id='mpg-scatter',
                figure=dict(
                    data=[
                        go.Scatter(
                            x=df['year'] + 1900,
                            y=df['mpg'],
                            text= df['name'],
                            hoverinfo='text+y',
                            mode='markers'
                        )
                    ],
                    layout=go.Layout(
                        title='MPG Data',
                        hovermode='closest',
                        xaxis=dict(
                            title='Model Year'
                        ),
                        yaxis=dict(
                            title='MPG'
                        )
                    )
                )
            ),
            style=dict(
                width='50%',
                display='inline-block'
            )
        ),
        html.Div(
            dcc.Graph(
                id='acc-line',
                figure=dict(
                    data=[
                        go.Scatter(
                            x=[0,1],
                            y=[0,1],
                            mode='lines'
                        )
                    ],
                    layout=go.Layout(
                        xaxis=dict(
                        visible=False
                        ),
                    yaxis=dict(
                        visible=False,
                        range=[0,60/df['acceleration'].min()]
                        ),
                    margin=dict(
                        l=0
                        ),
                    height=300
                    )
                )
            ),
            style=dict(
                width='20%',
                height='50%',
                display='inline-block'
            )
        ),
        html.Div(
            dcc.Markdown(
                id='mpg-stats',
                children='test'
            ),
            style=dict(
                width='20%',
                height='50%',
                display='inline-block'
            )
        )
    ]
)


@app.callback(
    Output('acc-line', 'figure'),
    [Input('mpg-scatter', 'hoverData')]
)
def callback_graph(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    figure=dict(
        data=[
            go.Scatter(
                x=[0,1],
                y=[0,60/df.iloc[v_index]['acceleration']],
                mode='lines',
                line=dict(
                    width=2*df.iloc[v_index]['cylinders']
                )
            )
        ],
        layout=go.Layout(
            title=df.iloc[v_index]['name'],
            xaxis=dict(
                visible=False
            ),
            yaxis=dict(
                visible=False,
                range=[0,60/df['acceleration'].min()]
            ),
            margin=dict(
                l=0
            ),
            height=300
        )
    )
    return figure


@app.callback(
    Output('mpg-stats', 'children'),
    [Input('mpg-scatter', 'hoverData')]
)
def callback_stats(hoverData):
    v_index = hoverData['points'][0]['pointIndex']
    stats = """
            {} cylinders
            {} cc displacement
            0 to 60 mph in {} seconds
    """.format(
        df.iloc[v_index]['cylinders'],
        df.iloc[v_index]['displacement'],
        df.iloc[v_index]['acceleration']
    )
    return stats


if __name__ == '__main__':
    app.run_server()