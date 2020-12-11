import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv('data/2010SantaBarbaraCA.csv')

data = [go.Heatmap(
                   x=data['DAY'],
                   y=data['LST_TIME'],
                   z=data['T_HR_AVG'].values.tolist(),
                   colorscale='Jet'
                  )
       ]
layout = go.Layout(title='SB CA Temps')
fig = go.Figure(data=data, layout=layout)

pyo.plot(fig, filename='heatmap.html')