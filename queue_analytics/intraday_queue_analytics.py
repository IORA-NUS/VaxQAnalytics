
import dash, json, dash_table, os
from dash_html_components.Data import Data
import dash_core_components as dcc
# import dash_bootstrap_components as dbc
# import dash_daq as daq
import dash_html_components as html

from dash.dependencies import Input, Output, State

import pandas as pd

import plotly.express as px
import plotly

from data_manager import DataManager

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


dm = DataManager()
num_scenarios = 2


app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                html.Img(src='static/CoBrand-IORA_H-web-1.png',style={'width':'90%', 'margin': '5%'}),
            ], className="two columns"),
            html.Div([
                html.H1(children='Intraday Queue Analytics'),
            ], className="ten columns"),
        ], className="row",
        ),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.H1(children='Inputs'),
            ], className="six columns"),
            # html.Div([
            #     html.H1(children='Recommended Actions'),
            # ], className="six columns"),
        ], className="row"),

        html.Div([
            html.H4(children='VC Settings'),

            html.P(children='Num Registration Counters'),
            dcc.Dropdown(
                id="RegistrationDesks", #type="number", placeholder="input with range",
                #min=dm.min_extents['RegistrationDesks'], max=dm.max_extents['RegistrationDesks'], step=1,
                options = [{'label': v, 'value': v} for v in dm.RegistrationDesks],
                value=dm.RegistrationDesks[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Num Vaccine Counters'),
            dcc.Dropdown(
                id="VaccineDesks", #type="number", placeholder="input with range",
                # min=dm.min_extents['VaccineDesks'], max=dm.max_extents['VaccineDesks'], step=1,
                options = [{'label': v, 'value': v} for v in dm.VaccineDesks],
                value=dm.VaccineDesks[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Post Vaccine Observation Seating Capacity'),
            dcc.Dropdown(
                id="SeatingCap", #type="number", placeholder="input with range",
                # min=dm.min_extents['SeatingCap'], max=dm.max_extents['SeatingCap'], step=1,
                options = [{'label': v, 'value': v} for v in dm.SeatingCap],
                value=dm.SeatingCap[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

        ], className="three columns"),
        html.Div([
            html.H4(children='Service Rate'),

            html.P(children='Registration Time (Mins)'),
            dcc.Dropdown(
                id="RegistrationTime", #type="number", placeholder="input with range",
                #min=dm.min_extents['RegistrationDesks'], max=dm.max_extents['RegistrationDesks'], step=1,
                options = [{'label': v, 'value': v} for v in dm.RegistrationTime],
                value=dm.RegistrationTime[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Vaccination Time (Mins)'),
            dcc.Dropdown(
                id="VaccineTime", #type="number", placeholder="input with range",
                # min=dm.min_extents['VaccineDesks'], max=dm.max_extents['VaccineDesks'], step=1,
                options = [{'label': v, 'value': v} for v in dm.VaccineTime],
                value=dm.VaccineTime[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Observation Time'),
            dcc.Dropdown(
                id="Waitingtime", #type="number", placeholder="input with range",
                # min=dm.min_extents['SeatingCap'], max=dm.max_extents['SeatingCap'], step=1,
                options = [{'label': v, 'value': v} for v in dm.Waitingtime],
                value=dm.Waitingtime[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

        ], className="three columns"),
        html.Div([
            html.H4(children='Performance Settings'),

            html.P(children='Max Seating at Registration'),
            dcc.Dropdown(
                id="max_QueueOutside", #type="number", placeholder="input with range",
                options = [{'label': v, 'value': v} for v in range(10, 200, 5)],
                value=100,
                # min=10, max=100, step=5,
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Max Wait Time Per Station'),
            dcc.Dropdown(
                id="max_wait", #type="number", placeholder="input with range",
                options = [{'label': v, 'value': v} for v in range(1, 11, 1)],
                value=5,
                # min=0, max=10,
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.P(children='Arrivals Per Day'),
            dcc.Dropdown(
                id="NoPerDay", #type="number", placeholder="input with range",
                # min=dm.min_extents['NoPerDay'], max=dm.max_extents['NoPerDay'], step=25,
                options = [{'label': v, 'value': v} for v in dm.NoPerDay],
                value=dm.NoPerDay[0],
                persistence=True,
            ),
            html.Div([html.Br()]),

            html.Button('Recommended Actions', id='compute_recommendation', n_clicks=0),
            html.Div([html.Br()]),

        ], className="three columns"),
        # html.Div([
        #     html.Div(id='recommendation_table'),

        # ], className="six columns"),
    ], className="row",),

    html.Div([
        html.Div([
            html.H1(children='Outputs'),
        ], className="six columns"),
    ], className="row",),
    html.Div([
        html.Div([
            html.Div(id='recommendation_table'),
        ], className="six columns", style={'margin': '40px'}),

    ], className="row",),

])


@app.callback([
        Output('recommendation_table', 'children'),
        Output('compute_recommendation', 'n_clicks'),
    ],
    [
        Input('compute_recommendation', 'n_clicks'),
    ],
    [
        State('RegistrationDesks', 'value'),
        State('VaccineDesks', 'value'),
        State('SeatingCap', 'value'),
        State('max_QueueOutside', 'value'),
        State('max_wait', 'value'),
        State('NoPerDay', 'value'),
    ])
def compute_recommendation(n, RegistrationDesks, VaccineDesks, SeatingCap, max_QueueOutside, max_wait, NoPerDay):

    if n > 0:
        ''' '''
        scenario = {
            'NoPerDay': NoPerDay,
            'max_QueueOutside': max_QueueOutside,
            'max_wait': max_wait,
            'settings': {
                'RegistrationDesks': RegistrationDesks,
                'VaccineDesks': VaccineDesks,
                'SeatingCap': SeatingCap,
            }
        }

        result = dm.evaluate_scenario(scenario)

        df = pd.DataFrame(list(result.items()),columns = ['Variable', 'Recommended Actions'])
        # for index, row in df.iterrows():
        #     if type(row['Value']) is dict or type(row['Value']) is list:
        #         row['Value'] = json.dumps(row['Value'])

        results_table = dash_table.DataTable(
            id='stats_table',
            style_header={
                'font-size': '24px',
                'whiteSpace': 'normal',
                'text-align': 'center',
                'text-weight': 'bold',
                'height': 'auto',
                'width': 'auto',
                'background-color': 'black',
                'color': 'white'
            },
            style_data={
                'textAlign': 'left',
                'font-size': '16px',
                'whiteSpace': 'normal',
                'height': 'auto',
                'width': 'auto'
            },
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )

        return results_table, 0

    return None, 0



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8100)
