import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash()

app.layout = html.Div(
    [
        dcc.RangeSlider(
            id='range-slider',
            min=-10,
            max=10,
            step=1,
            value=[-1,1],
            marks={
                i:i for i in range(-10,11)
            }
        ),
        html.Hr(),
        html.Div(
            id='result'
        )
    ]
)


@app.callback(
    Output('result', 'children'),
    [Input('range-slider', 'value')]
)
def update_text(values):
    return '{} times {} is {}'.format(
        values[0], values[1], values[0]*values[1]
    )

if __name__ == '__main__':
    app.run_server()