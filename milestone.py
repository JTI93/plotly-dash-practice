import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from uk_covid19 import Cov19API


# Call COVID API and format
api = Cov19API(
    filters=[
        'areaType=region'
    ],
    structure=dict(
        date='date',
        areaName='areaName',
        newCasesBySpecimenDate='newCasesBySpecimenDate',
        newCasesByPublishDate='newCasesByPublishDate',
        newTestsByPublishDate='newTestsByPublishDate'#,
        #newDeathsBySpecimenDate='newDeathsBySpecimenDate'
    )
)
data = api.get_dataframe()
data['date'] = pd.to_datetime(data['date'])

data.rename(
    columns=dict(
        areaName='region',
        newCasesBySpecimenDate='cases_by_specimen_date',
        newCasesByPublishDate='cases_by_publish_date',
        newTestsByPublishDate='tests_by_publish_date'
    ),
    inplace=True
)

# Generate dropdown options
regions = []
for region in data['region'].unique():
    regions.append(
            dict(
            label=region,
            value=region
        )
    )

# 2019 population estimates from
# https://www.ons.gov.uk/visualisations/dvc845/poppyramids/pyramids/datadownload.xlsx
# Load and pre-process
pops = pd.read_csv('data/ons_population_estimates_mid_2019.csv')
pops.loc[pops['region'] == 'East', ['region']] = 'East of England'

app = dash.Dash()

app.layout = html.Div(
    [
        html.H1(
            children='Coronavirus Summary',
            style=dict(
                textAlign='center'
            )
        ),
        html.H3(
            'Select a region:'
        ),
        dcc.Dropdown(
            id='region-dropdown',
            options=regions,
            value='Yorkshire and The Humber'
        ),
        dcc.Graph(
            id='cases-graph',
            figure=dict(
                data=[
                    go.Scatter(
                        hoverinfo='x+y',
                        mode='lines'
                    )
                ],
                layout=go.Layout(
                    title='New Cases by Specimen Date',
                    hovermode='closest',
                    xaxis=dict(
                        title='Specimen Date'
                    ),
                    yaxis=dict(
                        title='New Cases'
                    )
                )
            )
        )
    ]
)

@app.callback(
    Output('cases-graph', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_figure(region):
    filtered_df = data[data['region'] == region]
    fig = dict(
        data=[
            go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['cases_by_specimen_date'],
                hoverinfo='x+y',
                mode='lines'
            )
        ],
        layout=go.Layout(
            title='New Cases by Specimen Date',
            hovermode='closest',
            xaxis=dict(
                title='Specimen Date'
            ),
            yaxis=dict(
            title='New Cases'
            )    
        )
    )
    return fig

if __name__ == '__main__':
    #app.run_server()
    #print(data.groupby(['date']).sum())
    #for col in data.columns:
    #    print(type(data[col][0]))
    #print(data)
    print(data.merge(pops, how='inner', on='region'))
    print(data['region'].unique())
    print(pops['region'].unique())