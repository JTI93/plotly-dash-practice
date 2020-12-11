import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()

# Define colour scheme, to be referenced later
colours = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

# Define the layout of the dashboard
# Give manual data inputs for basic example
app.layout = html.Div(children=[
    html.H1('Hello Dash!',
        style={
            'textAlign': 'center',
            'color': colours['text']
            }
        ),
    html.Div('Dash: Web Dashboards with Python'),
    dcc.Graph(
        id='example',
        figure={
            'data':[
                {
                'x': [1,2,3],
                'y': [4,2,1],
                'type': 'bar',
                'name': 'SF'
                },
                {
                'x': [1,2,3],
                'y': [2,4,5],
                'type': 'bar',
                'name': 'NYC'
                }
            ],
            'layout':{
                'plot_bgcolour': colours['background'],
                'paper_bgcolor': colours['background'],
                'font': {
                    'color': colours['text']
                },
                'title': 'Bar Plots'
            }
        }
    )
],
style={'backgroundColor': colours['background']}
)


# If executing this file directly, run the server
if __name__ == '__main__':
    app.run_server()