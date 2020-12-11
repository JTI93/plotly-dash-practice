import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np

app = dash.Dash()

# Create some data to visualize
np.random.seed(42)
random_x = np.random.randint(1, 101, 100)
random_y = np.random.randint(1, 101, 100)

# Use plotly to create a graph 
app.layout = html.Div(
    [
        dcc.Graph(
            id='scatterplot',
            figure={
                'data': [go.Scatter(
                    x=random_x,
                    y=random_y,
                    mode='markers',
                    marker={
                        'size':12,
                        'color':'rgb(51,204,153)',
                        'symbol':'pentagon',
                        'line':{'width':2}
                    }
                )],
                'layout': go.Layout(
                    title='Random Scatterplot',
                    xaxis={'title':'Random integers'}
                )
            }
        ),
        dcc.Graph(
            id='scatterplot2',
            figure={
                'data': [go.Scatter(
                    x=random_x,
                    y=random_y,
                    mode='markers',
                    marker={
                        'size':12,
                        'color':'rgb(200,53,153)',
                        'symbol':'pentagon',
                        'line':{'width':2}
                    }
                )],
                'layout': go.Layout(
                    title='A Second Random Scatterplot',
                    xaxis={'title':'Random integers'}
                )
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server()