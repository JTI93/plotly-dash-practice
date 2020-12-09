import plotly.offline as pyo
import plotly.graph_objs as go


y = [1,14,14,15,16,18,18,19,19,20,20,23,24,26,27,27,28,29,33,54]

data = [go.Box(y=y,
               boxpoints='all', # shows all data points in the box plot
               jitter=0.3,      # distributes points across box plot for easier viewing of dense data
               pointpos=2.0     # moves data points along x-axis 
              )]
pyo.plot(data, filename='boxplot1.html')
