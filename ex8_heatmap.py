import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd

# Import flight data
df = pd.read_csv('data/flights.csv')

data = go.Heatmap(
    x=df['year'],
    y=df['month'],
    z=df['passengers'],
    colorscale='Jet'
)

layout = go.Layout(title='Average Passengers per Flight')
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='ex8_heatmap.html')