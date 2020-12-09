import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('data/mpg.csv')

data = [go.Scatter(x=df['displacement'],
                   y=df['acceleration'],
                   text=df['name'],
                   mode='markers',
                   marker=dict(size=df['cylinders']*3,
                               showscale=True
                               )
                   )]

layout = go.Layout(title='Bubble Chart Exercise')
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='ex4_bubblechart.html')