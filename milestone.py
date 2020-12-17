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
        newCasesByPublishDate='newCasesBySpecimenDate',
        newTestsByPublishDate='newTestsByPublishDate'#,
        #newDeathsBySpecimenDate='newDeathsBySpecimenDate'
    )
)
data = api.get_dataframe()
data['date'] = pd.to_datetime(data['date'])

# Generate dropdown options
regions = []
for region in data['areaName'].unique():
    regions.append(
            dict(
            label=region,
            value=region
        )
    )

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
    filtered_df = data[data['areaName'] == region]
    fig = dict(
        data=[
            go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['newCasesByPublishDate'],
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
    app.run_server()
    #print(data.groupby(['date']).sum())
    #for col in data.columns:
    #    print(type(data[col][0]))
