import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import base64

df = pd.read_csv('data/wheels.csv')

app = dash.Dash()

def encode_image(image_file):
    encoded = base64.b64encode(
        open(image_file, 'rb').read()
    )
    return 'data:image/png;base64,{}'.format(encoded.decode())

app.layout = html.Div([
    dcc.RadioItems(
        id='wheels',
        options=[
            dict(
                label=i,
                value=i
            ) for i in df['wheels'].unique()
        ],
        value=1
    ),
    html.Div(
        id='wheels-output'
    ),
    html.Hr(),
    dcc.RadioItems(
        id='color',
        options=[
            dict(
                label=i,
                value=i
            ) for i in df['color'].unique()
        ],
        value='blue'
    ),
    html.Div(
        id='color-output'
    ),
    html.Img(
        id='display-image',
        src='children',
        height=300
    )
],
style=dict(
    fontFamily='helvetica',
    fontSize=18
))


@app.callback(
    Output('wheels-output', 'children'),
    [Input('wheels', 'value')]
)
def callback_a(wheel_val):
    return "You chose {}".format(wheel_val)

@app.callback(
    Output('color-output', 'children'),
    [Input('color', 'value')]
)
def callback_b(color_val):
    return "You chose {}".format(color_val)

@app.callback(
    Output('display-image', 'src'),
    [
        Input('wheels', 'value'),
        Input('color', 'value')
    ]
)
def callback_image(wheel, color):
    path = 'data/images/'
    return encode_image(
        path + df[
            (df['wheels'] == wheel) &
            (df['color'] == color)
        ]['image'].values[0])

if __name__ == '__main__':
    app.run_server()