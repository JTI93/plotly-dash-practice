import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


app = dash.Dash()

app.layout = html.Div(
    [
        dcc.Input(
            id='number-in',
            value=1,
            style=dict(
                fontSize=24
            )
        ),
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit here',
            style=dict(
                fontSize=24
            )
        ),
        html.H1(
            id='number-out'
        )
    ]
)

@app.callback(
    Output('number-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('number-in', 'value')]
)
def out(n_clicks, number):
    return '{} was typed in and button was clicked {} times'.format(number, n_clicks)

if __name__ == '__main__':
    app.run_server()