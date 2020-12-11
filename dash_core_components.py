import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(
    [
        html.Label('Dropdown'),
        dcc.Dropdown(
            options=
            [
                dict(
                    label='New York City',
                    value='NYC'
                ),
                dict(
                    label='San Francisco',
                    value='SF'
                )
            ],
            value='SF' # Set the dropdown's default value
        ),
        html.Label('Slider'),
        dcc.Slider(
            min=-10,
            max=10,
            step=0.5,
            value=0,
            marks={
                i:i for i in range(-10,11)
            }
        ),
        html.P(
            html.Label('Radio Items') # Wraps components in a paragraph, solves some spacing issues on the dashboard
        ),
        dcc.RadioItems(
            options=[
                dict(
                    label='New York City',
                    value='NYC'
                ),
                dict(
                    label='San Francisco',
                    value='SF'
                )
            ],
            value='SF'
            )
    ]
)

if __name__ == '__main__':
    app.run_server()