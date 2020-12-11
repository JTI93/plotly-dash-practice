import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash()

# Import Old Faithful data
data = pd.read_csv('data/OldFaithful.csv')

# Define the layout
app.layout = (html.Div(children=[
    html.H1('Old Faithful Eruption Data',
        style={'textAlign':'center'}),
    dcc.Graph(
        id='eruption_times',
        figure={
            'data':[go.Scatter(
                x=data['X'],
                y=data['Y'],
                mode='markers'
            )],
            'layout':go.Layout(
                title='Eruption Interval vs Duration',
                xaxis={'title':'Time to next eruption (minutes)'},
                yaxis={'title':'Duration of eruption'}
            )
        }
    )]
))

if __name__ == '__main__':
    app.run_server()