import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from uk_covid19 import Cov19API


# Set up COVID api calls
api = Cov19API(
    filters=[
        'areaType=region'
    ],
    structure=dict(
        date='date',
        areaName='areaName',
        newCasesByPublishDate='newCasesByPublishDate',
        newDeathsByPublishDate='newDeathsByPublishDate'
    )
)

data = api.get_dataframe()

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
            value='All'
        ),
        dcc.Graph(
            id='cases-graph',
            figure=dict(
                data=dict(

                ),
                figure=dict(

                )
            )
        )
    ]
)



if __name__ == '__main__':
    #app.run_server()
    print(pd.to_datetime(data['date']))