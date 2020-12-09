import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('data/mpg.csv')

data = [go.Histogram(x=df['mpg'],
                     xbins=dict(
                                start=0,
                                end=50,
                                size=2
                               )
                    )]
layout = go.Layout(title='Histogram MPG Example')
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='histogram.html')