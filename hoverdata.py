import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import json
import pandas as pd
import base64

app = dash.Dash()

df = pd.read_csv('data/wheels.csv')

def encode_image(image_file):
    encoded = base64.b64encode(
        open(image_file, 'rb').read()
    )
    return 'data:image/png;base64,{}'.format(encoded.decode())

app.layout = html.Div(
    [
        html.Div(
            dcc.Graph(
                id='wheels-plot',
                figure=dict(
                    data=[go.Scatter(
                        x=df['color'],
                        y=df['wheels'],
                        dy=1,
                        mode='markers',
                        marker=dict(
                            size=15
                        )
                    )],
                    layout=go.Layout(
                        title='Test',
                        hovermode='closest'
                    )
                )
            ),
            style=dict(
                width='30%',
                float='left'
            )
        ),
        html.Div(
            html.Img(
                id='hover-data',
                src='children',
                height=300
            ),
            style=dict(
                    width='30%',
                    paddingTop=35
                )
        )
    ]
)

@app.callback(
    Output('hover-data', 'src'),
    [Input('wheels-plot', 'hoverData')]
)
def callback_image(hoverData):
    wheel = hoverData['points'][0]['y']
    color = hoverData['points'][0]['x']
    path = 'data/images/'
    return encode_image(
        path + df[
            (df['wheels'] == wheel) &
            (df['color'] == color)
        ]['image'].values[0])

if __name__ == '__main__':
    app.run_server()