import plotly.offline as pyo
import plotly.figure_factory as ff
import pandas as pd

# Import the Iris dataset
data = pd.read_csv('data/iris.csv')

# Separate out petal lengths into the iris classes
setosa = data[data['class'] == 'Iris-setosa']['petal_length']
virginica = data[data['class'] == 'Iris-virginica']['petal_length']
versicolor = data[data['class'] == 'Iris-versicolor']['petal_length']

# Set up the dist plot
hist_data = [setosa, virginica, versicolor]
group_labels = ['Setosa', 'Virginica', 'Versicolor']

# Plot and show
fig = ff.create_distplot(hist_data=hist_data, group_labels=group_labels, bin_size=[0.2, 0.2, 0.2])
pyo.plot(fig, filename='ex7_distplot.html')
