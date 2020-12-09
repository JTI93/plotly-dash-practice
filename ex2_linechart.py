import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('data/2010YumaAZ.csv')


data = [go.Scatter(
                   x=df['LST_TIME'][df['DAY'] == day],
                   y=df['T_HR_AVG'][df['DAY'] == day],
                   mode='lines',
                   name=day
                  ) for day in df['DAY'].unique()]

layout = go.Layout(title='Temperature',
                   hovermode='x unified')

fig = go.Figure(
                data=data,
                layout=layout
               )
pyo.plot(fig, filename='ex2_linecharts.html')