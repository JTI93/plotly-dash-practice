import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(
    children=[
        'This is the outer most div.',
        html.Div(
            'This in an inner div',
            style=dict(
                color='red',
                border='2px red solid'
            )
        ),
        html.Div([
            'Another inner div'
            ],
            style=dict(
                color='blue',
                border='3px blue solid'
            )
        )
    ],
    style=dict(
        color='green',
        border='2px green solid'
    )
)

if __name__ == '__main__':
    app.run_server()