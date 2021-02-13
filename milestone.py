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

data_correct_on = (datetime.today()+timedelta(days=-1)).strftime('%d/%m/%Y')
total_cases = region_data['cases_by_specimen_date'].sum()
total_cases_fmt = f'{total_cases:,.0f}'
total_deaths = region_data['deaths_28d_by_publish_date'].sum()
total_deaths_fmt = f'{total_deaths:,.0f}'
deaths_per_case = total_deaths / total_cases
deaths_per_case_fmt = f'{deaths_per_case:,.4f}'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


canvas_style = dict(
    maxHeight='100vh',
    maxWidth='100vw',
    minHeight='720px',
    minWidth='1280px',
    height='100vh',
    width='100vw',
    display='flex',
    flexDirection='column',
    backgroundColor='#E0E0E0'
)

header_base_style = dict(
    maxHeight='',
    maxWidth='',
    minHeight='72px',
    height='7%',
    width='100%',
    backgroundColor='#424242',
    fontWeight='bold'
)

header_side_box_style = dict(
    minWidth='',
    height='100%',
    color='#EEEEEE',
    backgroundColor='#295894'
)

header_side_text_style = dict(
    minWidth='',
    maxWidth='230px',
    height='',
    width='',
    textAlign='center',
    paddingLeft='5px',
    paddingRight='5px',
    paddingTop='2px',
    paddingBottom='2px'
)

header_box_style = dict(
    maxHeight='',
    maxWidth='',
    minHeight='',
    minWidth='1050px',
    height='100%'
)

header_box_inner_style = dict(
    minWidth='1050px',
    width='100%',
    height='100%'
)

header_text_style = dict(
    maxHeight='',
    maxWidth='',
    minHeight='',
    minWidth='',
    height='',
    width='',
    color='#EEEEEE',
    fontWeight='bold'
)

content_base_style = dict(
    height='93%',
    width='100%'
)

sidebar_col_style = dict(
    height='100%',
    width='100%',
    color='#EEEEEE',
    backgroundColor='#295894',
    fontWeight='bold',
    fontSize=22
)

sidebar_figure_box_style = dict(
    height='25%',
    display='flex',
    flexDirection='column'
)

graph_master_style = dict(
    height='100%',
    width='100%',
    display='flex',
    flexDirection='row'
)

filter_box_style = dict(
    height='10%',
    width='100%'
)

graph_row_style = dict(
    height='45%',
    width='50%'
)

graph_style = dict(
    height='100%',
    width='100%',
    backgroundColor='#E0E0E0'
)

region_dropdown_style = dict(
    height='42px',
    width='550px',
    display='inline-block'
)

app.layout = html.Div(
    children=[
        dbc.Row(
            id='header-master-row',
            style=header_base_style,
            no_gutters=True,
            children=[
                dbc.Col(
                    id='header-side-col',
                    style=header_side_box_style,
                    width=2,
                    children=[
                        dbc.Row(
                            id='header-side-box',
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=html.Div(
                            id='header-side-text',
                            children='Data sourced from Public Health England and Office of National Statistics',
                            style=header_side_text_style
                        )
                        )
                        
                    ]
                ),
                dbc.Col(
                    id='header-main-col',
                    style=header_box_style,
                    width=10,
                    children=[
                        dbc.Row(
                            id='header-main-box',
                            style=header_box_inner_style,
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=html.H1(
                                id='header-main-text',
                                style=header_text_style,
                                children='Coronavirus summary for England'
                            )
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            id='content-master-row',
            style=content_base_style,
            no_gutters=True,
            children=[
                dbc.Col(
                    id='content-side-col',
                    style=sidebar_col_style,
                    width=2,
                    children=[
                        dbc.Row(
                            id='data-date-box',
                            style=sidebar_figure_box_style,
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=[
                                html.Div(
                                    id='data-date-text',
                                    children='Data correct as of:'
                                ),
                                html.Div(
                                    id='data-date-value',
                                    children=data_correct_on
                                )
                            ]
                        ),
                        dbc.Row(
                            id='total-cases-box',
                            style=sidebar_figure_box_style,
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=[
                                html.Div(
                                    id='total-cases-text',
                                    children='Total cases:'
                                ),
                                html.Div(
                                    id='total-cases-value',
                                    children=total_cases_fmt
                                )
                            ]
                        ),
                        dbc.Row(
                            id='total-deaths-box',
                            style=sidebar_figure_box_style,
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=[
                                html.Div(
                                    id='total-deaths-text',
                                    children='Total deaths:'
                                ),
                                html.Div(
                                    id='total-deaths-value',
                                    children=total_deaths_fmt
                                ),
                                html.Div(
                                    id='total-deaths-text_add',
                                    children='(within 28 days of diagnosis)',
                                    style=dict(
                                        fontSize=15
                                    )
                                )
                            ]
                        ),
                        dbc.Row(
                            id='deaths-per-case-box',
                            style=sidebar_figure_box_style,
                            no_gutters=True,
                            align='center',
                            justify='center',
                            children=[
                                html.Div(
                                    id='deaths-per-case-text',
                                    children='Deaths per case:'
                                ),
                                html.Div(
                                    id='deaths-per-case-value',
                                    children=deaths_per_case_fmt
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    id='content-main-col',
                    width=10,
                    children=[
                        dbc.Row(
                            id='graph-master-row',
                            style=graph_master_style,
                            no_gutters=True,
                            children=[
                                dbc.Row(
                                    id='filter-master',
                                    style=filter_box_style,
                                    no_gutters=True,
                                    align='center',
                                    justify='center',
                                    children=[
                                        dcc.DatePickerRange(
                                            id='date-range-picker',
                                            min_date_allowed=datetime(2020,3,1),
                                            max_date_allowed=datetime.today()+timedelta(days=-4),
                                            start_date=datetime(2020,3,1),
                                            end_date=datetime.today()+timedelta(days=-4),
                                            display_format='DD/MM/YYYY'
                                        ),
                                        dcc.Dropdown(
                                            id='region-dropdown',
                                            style=region_dropdown_style,
                                            multi=True,
                                            options=regions,
                                            value=['Yorkshire and The Humber']
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    id='graph-one',
                                    style=graph_row_style,
                                    no_gutters=True,
                                    children=[
                                        dcc.Graph(
                                            id='abs-cases-graph',
                                            style=graph_style,
                                            figure=dict(
                                                data=[],
                                                layout=go.Layout(
                                                    title='New Cases',
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
                                ),
                                dbc.Row(
                                    id='graph-two',
                                    style=graph_row_style,
                                    no_gutters=True,
                                    children=[
                                        dcc.Graph(
                                            id='rel-cases-graph',
                                            style=graph_style,
                                            figure=dict(
                                                data=[],
                                                layout=go.Layout(
                                                    title='New Cases per 100K Population',
                                                    xaxis=dict(
                                                        title='Specimen Date'
                                                    ),
                                                    yaxis=dict(
                                                        title='New Cases per 100k'
                                                    )
                                                )
                                            )
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    id='graph-three',
                                    style=graph_row_style,
                                    no_gutters=True,
                                    children=[
                                        dcc.Graph(
                                            id='abs-deaths-graph',
                                            style=graph_style,
                                            figure=dict(
                                                data=[],
                                                layout=go.Layout(
                                                    title='Deaths by Publish Date',
                                                    xaxis=dict(
                                                        title='Publish Date'
                                                    ),
                                                    yaxis=dict(
                                                        title='New Deaths'
                                                    )
                                                )
                                            )
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    id='graph-four',
                                    style=graph_row_style,
                                    no_gutters=True,
                                    children=[
                                        dcc.Graph(
                                            id='rel-deaths-graph',
                                            style=graph_style,
                                            figure=dict(
                                                data=[],
                                                layout=go.Layout(
                                                    title='Deaths per Case',
                                                    xaxis=dict(
                                                        title='Publish Date'
                                                    ),
                                                    yaxis=dict(
                                                        title='Deaths per Case'
                                                    )
                                                )
                                            )
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ],
    style=canvas_style
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
            ),
            paper_bgcolor='#E0E0E0'
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
            ),
            paper_bgcolor='#E0E0E0'
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
            ),
            paper_bgcolor='#E0E0E0'
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
            ),
            paper_bgcolor='#E0E0E0'
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server()