import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from uk_covid19 import Cov19API
from datetime import datetime
from datetime import timedelta


# Call COVID API and format
region_api = Cov19API(
    filters=[
        'areaType=region'
    ],
    structure=dict(
        date='date',
        areaName='areaName',
        newCasesByPublishDate='newCasesByPublishDate',
        newCasesBySpecimenDate='newCasesBySpecimenDate',
        newDeaths28DaysByPublishDate='newDeaths28DaysByPublishDate'
    )
)
region_data = region_api.get_dataframe()
region_data['date'] = pd.to_datetime(region_data['date'])

region_data.rename(
    columns=dict(
        areaName='region',
        newCasesBySpecimenDate='cases_by_specimen_date',
        newCasesByPublishDate='cases_by_publish_date',
        newDeaths28DaysByPublishDate='deaths_28d_by_publish_date'
    ),
    inplace=True
)

# 2019 population estimates from
# https://www.ons.gov.uk/visualisations/dvc845/poppyramids/pyramids/datadownload.xlsx
# Load and pre-process
pops = pd.read_csv('data/ons_population_estimates_mid_2019.csv')
pops.loc[pops['region'] == 'East', ['region']] = 'East of England'


# Calculate metrics for region graphs
region_data = region_data.merge(pops, on='region')
region_data['cases_per_100k'] = (
    region_data['cases_by_specimen_date'] /
    region_data['pop_est'] * 100000
)
region_data['deaths_28_per_case_by_publish_date'] = (
    region_data['deaths_28d_by_publish_date'] /
    region_data['cases_by_publish_date']
)


# Generate dropdown options
regions = []
for region in region_data['region'].unique():
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
        html.Div(
            [
                html.H3(
                    'Select a date range:',
                    style=dict(
                        width='50%'
                    )
                ),
                html.H3(
                    'Select one or more regions:',
                    style=dict(
                        width='50%'
                    )
                )
            ],
            style=dict(
                display='flex',
                flexDirection='row',
                textAlign='center'
            )
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            style=dict(
                                display='flex',
                                flexGrow=1
                            )
                        ),
                        dcc.DatePickerRange(
                            id='date-range-picker',
                            min_date_allowed=datetime(2020,3,1),
                            max_date_allowed=datetime.today()+timedelta(days=-4),
                            start_date=datetime(2020,3,1),
                            end_date=datetime.today()+timedelta(days=-4),
                            display_format='DD/MM/YYYY',
                            style=dict(
                                height=48,
                                fontSize=20,
                                alignContent='center'
                            )
                        ),
                        html.Div(
                            style=dict(
                                display='flex',
                                flexGrow=1
                            )
                        )
                    ],
                    style=dict(
                        width='50%',
                        display='flex',
                        flexDirection='row'
                    )
                ),
                html.Div(
                    dcc.Dropdown(
                        id='region-dropdown',
                        multi=True,
                        options=regions,
                        value=['Yorkshire and The Humber'],
                        style=dict(
                            width='100%',
                            height=48,
                            fontSize=22,
                            textAlign='center'
                        )
                    ),
                    style=dict(
                        width='50%',
                        display='flex',
                        alignContent='center'
                    )
                )
            ],
            style=dict(
                fontSize=16,
                display='flex',
                flexDirection='row',
                alignContent='center'
            )
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        id='abs-cases-graph',
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
                    ),
                    style=dict(
                        width='50%',
                        display='inline-block'
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id='rel-cases-graph',
                        figure=dict(
                            data=[],
                            layout=go.Layout(
                                title='New Cases per 100k Population',
                                xaxis=dict(
                                    title='Specimen Date'
                                ),
                                yaxis=dict(
                                    title='Cases per 100k'
                                )
                            )
                        )
                    ),
                    style=dict(
                        width='50%',
                        display='inline-block'
                    )
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id='abs-deaths-graph',
                        figure=dict(
                            data=[],
                            layout=go.Layout(
                                title='New Deaths by Publish Date',
                                xaxis=dict(
                                    title='Date Published'
                                ),
                                yaxis=dict(
                                    title='New Deaths'
                                )
                            )
                        )
                    ),
                    style=dict(
                        width='50%',
                        display='inline-block'
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id='rel-deaths-graph',
                        figure=dict(
                            data=[],
                            layout=go.Layout(
                                title='Deaths per Case by Publish Date',
                                xaxis=dict(
                                    title='Date Published'
                                ),
                                yaxis=dict(
                                    title='Deaths per Case'
                                )
                            )
                        )
                    ),
                    style=dict(
                        width='50%',
                        display='inline-block'
                    )
                )
            ]
        )

    ]
)

@app.callback(
    Output('abs-cases-graph', 'figure'),
    [
        Input('region-dropdown', 'value'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    ]
)
def update_abs_case_fig(selected_regions, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    filtered_df = region_data[
        (region_data['date'] >= start) &
        (region_data['date'] <= end)
    ]
    traces = []
    for region in selected_regions:
        region_df = filtered_df[
            filtered_df['region'] == region
        ]
        trace = go.Scatter(
            x=region_df['date'],
            y=region_df['cases_by_specimen_date'],
            name=region,
            hoverinfo='x+y',
            mode='lines'
        )
        traces.append(trace)

    fig = dict(
        data=traces,
        layout=go.Layout(
            title='New Cases by Specimen Date',
            hovermode='x',
            xaxis=dict(
                title='Specimen Date'
            ),
            yaxis=dict(
            title='New Cases'
            )    
        )
    )
    return fig

@app.callback(
    Output('abs-deaths-graph', 'figure'),
    [
        Input('region-dropdown', 'value'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    ]
)
def update_abs_death_fig(selected_regions, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    filtered_df = region_data[
        (region_data['date'] >= start) &
        (region_data['date'] <= end)
    ]
    traces = []
    for region in selected_regions:
        region_df = filtered_df[
            filtered_df['region'] == region
        ]
        trace = go.Scatter(
            x=region_df['date'],
            y=region_df['deaths_28d_by_publish_date'],
            name=region,
            hoverinfo='x+y',
            mode='lines'
        )
        traces.append(trace)

    fig = dict(
        data=traces,
        layout=go.Layout(
            title='New Deaths by Publish Date',
            hovermode='x',
            xaxis=dict(
                title='Date Published'
            ),
            yaxis=dict(
            title='New Deaths'
            )    
        )
    )
    return fig

@app.callback(
    Output('rel-cases-graph', 'figure'),
    [
        Input('region-dropdown', 'value'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    ]
)
def update_rel_case_fig(selected_regions, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    filtered_df = region_data[
        (region_data['date'] >= start) &
        (region_data['date'] <= end)
    ]
    traces = []
    for region in selected_regions:
        region_df = filtered_df[
            filtered_df['region'] == region
        ]
        trace = go.Scatter(
            x=region_df['date'],
            y=region_df['cases_per_100k'],
            name=region,
            hoverinfo='x+y',
            mode='lines'
        )
        traces.append(trace)

    fig = dict(
        data=traces,
        layout=go.Layout(
            title='New Cases per 100k Population',
            hovermode='x',
            xaxis=dict(
                title='Specimen Date'
            ),
            yaxis=dict(
            title='New Cases per 100k Population'
            )    
        )
    )
    return fig

@app.callback(
    Output('rel-deaths-graph', 'figure'),
    [
        Input('region-dropdown', 'value'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    ]
)
def update_rel_death_fig(selected_regions, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    filtered_df = region_data[
        (region_data['date'] >= start) &
        (region_data['date'] <= end)
    ]
    traces = []
    for region in selected_regions:
        region_df = filtered_df[
            filtered_df['region'] == region
        ]
        trace = go.Scatter(
            x=region_df['date'],
            y=region_df['deaths_28_per_case_by_publish_date'],
            name=region,
            hoverinfo='x+y',
            mode='lines'
        )
        traces.append(trace)

    fig = dict(
        data=traces,
        layout=go.Layout(
            title='Deaths per Case by Publish Date',
            hovermode='x',
            xaxis=dict(
                title='Date Published'
            ),
            yaxis=dict(
            title='Deaths per Case'
            )    
        )
    )
    return fig

def has_data(df):
    uniques = df.unique()
    if len(uniques) == 1 and uniques[0] == None:
        return False
    else:
        return True

if __name__ == '__main__':
    app.run_server()