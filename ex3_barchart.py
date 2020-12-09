import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('data/mocksurvey.csv')
df.set_index('Unnamed: 0', inplace=True)

data = [go.Bar(
               x=df[response],
               y=df.index,
               name=response,
               orientation='h'
              ) for response in df.columns]

layout = go.Layout(title='Responses to Questions',
                   barmode='stack')

fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='ex3_barchart.html')