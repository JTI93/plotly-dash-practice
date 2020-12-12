import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div([
    dcc.Input(
        id='input-id',
        value='Initial text',
        type='text'
    ),
    html.Div(
        id='div-id',
        style=dict(
            border='2px blue solid'
            )
        )
])

@app.callback(
    Output(
        component_id='div-id',
        component_property='children'
    ),
    [Input(
        component_id='input-id',
        component_property='value'
    )]
)
def update_out_div(input_value):
    return "You entered: {}".format(input_value)

if __name__ == '__main__':
    app.run_server()