import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.tools as tools
import pandas as pd

# Import temp data for three cities
df1 = pd.read_csv('data/2010SitkaAK.csv')
df2 = pd.read_csv('data/2010SantaBarbaraCA.csv')
df3 = pd.read_csv('data/2010YumaAZ.csv')

# Set up heat maps for each city
data1 = go.Heatmap(
                   x=df1['DAY'],
                   y=df1['LST_TIME'],
                   z=df1['T_HR_AVG'].values.tolist(),
                   colorscale='Jet',
                   zmin=5,
                   zmax=40
                   )     
data2 = go.Heatmap(
                   x=df2['DAY'],
                   y=df2['LST_TIME'],
                   z=df2['T_HR_AVG'].values.tolist(),
                   colorscale='Jet',
                   zmin=5,
                   zmax=40
                   )
data3 = go.Heatmap(
                   x=df3['DAY'],
                   y=df3['LST_TIME'],
                   z=df3['T_HR_AVG'].values.tolist(),
                   colorscale='Jet',
                   zmin=5,
                   zmax=40
                   )

# Configure the figure and subplots
fig = tools.make_subplots(rows=1,
                          cols=3,
                          subplot_titles=['Sitka AK', 'Santa Barbara CA', 'Yuma AZ'],
                          shared_yaxes=False
                         )
fig.append_trace(data1, 1, 1)
fig.append_trace(data2, 1, 2)
fig.append_trace(data3, 1, 3)
fig['layout'].update(title='Temps for three cities')

pyo.plot(fig, filename='heatmap2.html')