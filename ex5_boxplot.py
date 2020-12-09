import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('data/abelone.csv')

sample1 = np.random.choice(df['rings'], 20, replace=False)
sample2 = np.random.choice(df['rings'], 30, replace=False)

data = [go.Box(y=sample1,
               name='Sample 1',
               boxpoints='outliers',
               jitter=0.2,
               pointpos=0
              ),
        go.Box(y=sample2,
               name='Sample 2',
               boxpoints='outliers',
               jitter=0.2,
               pointpos=0
              )
       ]

layout = go.Layout(title='Two Random Samples')
fig = go.Figure(data=data, layout=layout)

pyo.plot(fig, filename='ex5_boxplot.html')