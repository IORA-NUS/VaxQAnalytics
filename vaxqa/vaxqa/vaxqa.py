
import dash, json, dash_table, os
from dash_html_components.Data import Data
import dash_core_components as dcc
import dash_bootstrap_components as dbc
# import dash_daq as daq
import dash_html_components as html
from dash_table.Format import Format
import json

from dash.dependencies import Input, Output, State

import pandas as pd

import plotly.express as px
import plotly

from statistics import median

# from data_manager import DataManager
# from data_manager_split import DataManagerSplit
from logic.query_manager import QueryManager
from app import app

# external_stylesheets = [dbc.themes.FLATLY, 'https://codepen.io/chriddyp/pen/bWLwgP.css', ]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# if app.config["ENV"] == "production":
#     app.config.from_object("config.ProductionConfig")
# elif  app.config["ENV"] == "development":
#     app.config.from_object("config.DevelopmentConfig")
# elif  app.config["ENV"] == "testing":
#     app.config.from_object("config.TestingConfig")
# else:
#     app.config.from_object("config.LocalConfig")



# scenario = 'results_cleaned_20210521'
# scenario = 'results_cleaned_20210527'

# q_manager = DataManager()
q_manager = QueryManager()
extents = q_manager.get_extents()

num_scenarios = 2

column_names = {
    "NoPerDay": "Arrivals Per Day",
    "RegistrationTime": "Registration Time (mins)",
    "VaccineTime": "Vaccination Time (mins)",
    "WaitingTime": "Observation Time (mins)",
    "RegistrationDesks": "Num Registration Counters",
    "VaccineDesks": "Num Vaccine Counters",
    "SeatingCap": "Observation Area Seating Capacity",
    "W1": "Waiting time for Registration (Secs)",
    "W2": "Waiting time for Vaccination (Secs)",
    "W3": "Waiting time to get seat for Observation (Secs)",
    "QueueOutside": "Queue at Registration Counter (Persons)",
    # "measure": "measure",
    "score": "Score",
}

percentile_options = {'Avg': 'Average', '90': '90 Percentile', '95': '95 Percentile'}

stations = ['Register', 'Vaccine', 'Observation']
options = ['Fixed', 'Search']


app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                html.Img(src='/static/CoBrand-IORA_H-web-1.png',style={'height': '50px', 'margin': '15px',}),
            ], className="two columns", style={'margin-left': '20px', 'width': '240px'}),
            html.Div([
                html.Img(src='/static/VaxQALogo_thin.png',style={'height': '50px','margin': '15px',}),
            ], className="six columns"),

            dbc.Button("User Guide", id="open-xl", style={'margin': '20px', 'font-size': '14px'}),
            dbc.Modal(
                [
                    # dbc.ModalHeader("Usage Instructions"),
                    dbc.ModalBody(
                        html.Div([
                            html.P('VaxQA is based on the Queuing model in the Figure and provides Performance Query and Recommendation Features.'),
                            html.H4('Performance Query'),
                            html.Ol([
                                html.Li('Choose the appropriate Number of Registration, Vaccination and Observation Stations from the VC Settings.'),
                                html.Li('Choose the mean Service rates for each of the stations.'),
                                html.Li('Choose the Appropriate Arrival rate to evaluate the VC Configuration,'),
                                html.Li('The VC Performance will be updated in the "Expected Performance" Table.'),
                                html.Li(html.B('Error Handling'),),
                                html.Ul([
                                    html.Li('Certain configurations might represent an unstable Queue System. In such cases, the "Expected Performance" section will report "NA" for all metrics'),
                                    html.Div([
                                        html.Img(src='/static/expected_na.png',style={'width': '600px','margin': '15px',}),
                                    ]),
                                    html.Li('To handle this situation, choose a different configuration. You can use the "Recommendation" module to identify the appropriate changes to the config'),
                                    # html.Li('Note: "NA" Indicates that the configuration cannot support the Arrival rate and results in ever increasing Queue length at the entry Station'),
                                ]),
                            ]),
                            html.Br(),
                            html.H4('Recommedation of Optimal VC Configuration'),
                            html.Ol([
                                html.Li('Choose appropriate thresholds from  the Performance target Section'),
                                html.Li('Each of the VC Settings and Service rates has an additional configuration Box ("Search" or"Fixed")'),
                                html.Ol([
                                    html.Li('Each of the VC Settings and Service rate chooser has an additional configuration Box ("Search" or"Fixed")'),
                                    html.Li('Choosing "Search" allows the Optmizer to modify this setting.'),
                                    html.Li('Choosing "Fixed" Applies a strict constraint to not modify this setting'),
                                    html.Li('For each of the settings, choose the appropriate config'),
                                    html.Li('Tip: Start by setting all Config to "Search" and progressively restrict the search'),
                                ]),
                                html.Li('The optimizer uses a Distance metric to find the nearest Configuration that meets the Performance criteria'),
                                html.Li('Initiate the search by clicking on "Recommend Actions"'),
                                html.Li(html.B('Error Handling'),),
                                html.Ul([
                                    html.Li('Certain configurations might might cause an error to be reported by the "Recommendation" module'),
                                    html.Div([
                                        html.Img(src='/static/rec_error.png',style={'width': '600px','margin': '15px',}),
                                    ]),
                                    html.Li('This is because, the VC config does not satisfy the SLA requirements and also that the search criteria is too Stringent. To resolve this issue, change a few of the constraints from "Fixed" to "Search" '),
                                    html.Div([
                                        html.Img(src='/static/rec_error_fix.png',style={'width': '600px','margin': '15px',}),
                                    ]),
                                ]),

                            ])
                        ]),
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-xl", className="ml-auto", style={'font-size': '14px'})
                    ),
                ],
                id="modal-xl",
                size="xl",
                scrollable=True,
                backdrop='static',
                centered=True,
            ),
                # html.Div([
                #     html.H4(children='(Vaccine Appointments Optimization Suite)')
                # ]),
        ], className="row",
            style={'background-color':'white',
                'height': '80px', #'14%',
                'position':'fixed',
                'top':'0', 'width':'100%',
                'zIndex':'99',
                '-webkit-box-shadow': '0 6px 6px -6px #777',
                '-moz-box-shadow': '0 6px 6px -6px #777',
                'box-shadow': '0 6px 6px -6px #777',
            },
        ),
    ]),

    html.Div([
        html.Div([
            html.Img(src='/static/process.png',style={'width': '100%',}),
        ], className="eight columns"),
    ], className="row", style={'margin-left': '10px', 'margin-top': '80px', 'margin-bottom': '10px'}),

    html.Div([
        html.Div([
            html.H4(children='VC Settings'),

            html.P(children='Num Registration Counters'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="RegistrationDesks", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': v} for v in q_manager.RegistrationDesks],
                        # value=q_manager.RegistrationDesks[0],
                        options = [{'label': v, 'value': v} for v in extents['RegistrationDesks']],
                        value = extents['RegistrationDesks'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="RegistrationDeskSearch", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v} for v in options],
                        value = options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%',}),

            ], className='row', style={'margin-left': '0px'}),
            html.Div([html.Br()]),

            html.P(children='Num Vaccine Counters'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="VaccineDesks",
                        # options = [{'label': v, 'value': v} for v in q_manager.VaccineDesks],
                        # value=q_manager.VaccineDesks[0],
                        options = [{'label': v, 'value': v} for v in extents['VaccineDesks']],
                        value = extents['VaccineDesks'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="VaccineDeskSearch",
                        options = [{'label': v, 'value': v} for v in options],
                        value=options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%'}),

            ], className='row', style={'margin-left': '0px'}),
            html.Div([html.Br()]),

            html.P(children='Post Vaccine Observation Seating Capacity'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="SeatingCap",
                        # options = [{'label': v, 'value': v} for v in q_manager.SeatingCap],
                        # value = q_manager.SeatingCap[0],
                        options = [{'label': v, 'value': v} for v in extents['SeatingCap']],
                        value = extents['SeatingCap'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="SeatingCapSearch", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v} for v in options],
                        value = options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%'}),

            ], className='row', style={'margin-left': '0px'}),
            html.Div([html.Br()]),

        ], className="three columns", style={'margin-left': '40px'}),
        html.Div([
            html.H4(children='Service Rate'),

            html.P(children='Registration Time (mins): Exponential'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="RegistrationTime", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': v} for v in q_manager.RegistrationTime],
                        # value=q_manager.RegistrationTime[0],
                        options = [{'label': v, 'value': v} for v in extents['RegistrationTime']],
                        value = extents['RegistrationTime'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="RegistrationTimeSearch", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v} for v in options],
                        value = options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%'}),

            ], className='row', style={'margin-left': '0px'}),
            html.Div([html.Br()]),

            html.P(children='Vaccination Time (mins): Exponential'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="VaccineTime", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': v} for v in q_manager.VaccineTime],
                        # value=q_manager.VaccineTime[0],
                        options = [{'label': v, 'value': v} for v in extents['VaccineTime']],
                        value = extents['VaccineTime'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="VaccineTimeSearch", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v} for v in options],
                        value = options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%'}),

            ], className='row', style={'margin-left': '0px'}),
            html.Div([html.Br()]),

            html.P(children='Observation Time (mins): Deterministic'),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="WaitingTime", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': v} for v in q_manager.WaitingTime],
                        # value=q_manager.WaitingTime[0],
                        options = [{'label': v, 'value': v} for v in extents['WaitingTime']],
                        value = extents['WaitingTime'][0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '60%'}),

                html.Div([
                    dcc.Dropdown(
                        id="WaitingTimeSearch", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v} for v in options],
                        value = options[0],
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '30%'}),

            ], className='row', style={'margin-left': '0px'}),

        ], className="three columns"),

        html.Div([
            html.H4(children='Arrival Rate'),
            html.Div([
                html.Div([
                    html.P(children='11 hrs/Day with 3 fire breaks: Poisson'),
                    dcc.Dropdown(
                        id="NoPerDay", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': v} for v in q_manager.NoPerDay],
                        # value=q_manager.NoPerDay[0],
                        options = [{'label': v, 'value': v} for v in extents['NoPerDay']],
                        value = extents['NoPerDay'][0],
                        persistence=True,
                        clearable=False,
                        # style={'width': '60%'}
                    ),
                ], className='one column', style={'width': '40%'}),

                html.Div([
                    html.P(children='Show Value as', style={'color': 'RebeccaPurple', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id="percentile", #type="number", placeholder="input with range",
                        # options = [{'label': v, 'value': k} for k, v in percentile_options.items()],
                        # value='Avg',
                        options = [{'label': percentile_options[k], 'value': k} for k in extents['measure']],
                        value = extents['measure'][0],
                        persistence=True,
                        clearable=False,
                        # style={'width': '60%'}
                    ),
                ], className='one column', style={'width': '20%'}),

            ], className="row", style={ 'margin-left': '0px'}),

            # html.Div([html.Br()]),

            html.Div([
                html.Div([
                    html.H3(children='Expected performance', style={'color': 'RebeccaPurple'}),
                        html.Div(id='expected_performance'),
                ], className="one column", style={'width': '70%'}),
            ], className="row", style={ 'margin-left': '0px'}),

            # html.Div([html.Br()]),

        ], className="five columns", ),

    ], className="row", style={ 'border': '1px solid gray', 'border-radius': '5px', 'padding-top': '10px', 'padding-bottom': '40px', 'margin': '10px'}),

    html.Div([
        html.Div([
            html.H3(children='Performance targets', style={'color': 'brown'}),

            html.P(children='Seating Capacity at Registration', style={'color': 'brown'}),
            dcc.Dropdown(
                id="max_QueueOutside", #type="number", placeholder="input with range",
                options = [{'label': v, 'value': v} for v in range(60, 251, 10)],
                value=100,
                # min=10, max=100, step=5,
                persistence=True,
                clearable=False,
            ),
            html.Div([html.Br()]),

            html.P(id='sla_header', children='Avg Wait Time SLA for:', style={'color': 'brown'}),
            html.Div([

                html.Div([
                    html.P(children='Registration', style={'color': 'brown'}),
                    dcc.Dropdown(
                        id="max_wait_reg", #type="number", placeholder="input with range",
                        options = [{'label': v, 'value': v*60} for v in range(1, 31, 1)], # in 1 min buckets
                        value=5*60,
                        # min=0, max=10,
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '25%'}),
                    # html.Div([html.Br()]),

                html.Div([
                    html.P(children='Vaccination', style={'color': 'brown'}),
                    dcc.Dropdown(
                        id="max_wait_vac", #type="number", placeholder="input with range",
                        options = [{'label': v/2, 'value': v*60/2} for v in range(1, 11, 1)], # in 30 sec buckets
                        value=2*60/2,
                        # min=0, max=10,
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '25%'}),
                    # html.Div([html.Br()]),

                html.Div([
                    html.P(children='Observation', style={'color': 'brown'}),
                    dcc.Dropdown(
                        id="max_wait_obs", #type="number", placeholder="input with range",
                        options = [{'label': v/2, 'value': v*60/2} for v in range(1, 11, 1)], # in 30 sec buckets
                        value=1*60/2,
                        # min=0, max=10,
                        persistence=True,
                        clearable=False,
                    ),
                ], className='one column', style={'width': '25%'}),
                    # html.Div([html.Br()]),

            ], className='row', style={'margin-left': '0px'}),

            html.Div([html.Br()]),

            # html.P(children='Arrivals Per Day (11 hrs): Poisson', style={'color': 'brown'}),
            # dcc.Dropdown(
            #     id="NoPerDay", #type="number", placeholder="input with range",
            #     # min=q_manager.min_extents['NoPerDay'], max=q_manager.max_extents['NoPerDay'], step=25,
            #     options = [{'label': v, 'value': v} for v in q_manager.NoPerDay],
            #     value=q_manager.NoPerDay[0],
            #     persistence=True,
            # ),
            # html.Div([html.Br()]),

            dbc.Button('Recommended Actions', id='compute_recommendation', n_clicks=1, style={'font-size': '14px'}),
            html.Div([html.Br()]),

        ], className="three columns", style={'margin-left': '50px'}),

        html.Div([

            html.Div([
                html.H3(children='Recommended Actions'),
            ], className="row", style={'width': '80%', 'color': '#3D9970'}),
            html.Div([
                html.Div(id='recommendation_table'),
            ], className="row", style={'width': '80%'}),

            html.Div([
                html.H3(children='Alternate Options'),
            ], className="row", style={'width': '80%', 'color': 'DimGray'}),
            html.Div([
                html.Div(id='alternate_solutions'),
            ], className="row",),

        ], className="eight columns", style={'margin-left': '80px'}),

    ], className="row",),


])

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [State("modal-xl", "is_open")],
)(toggle_modal)

@app.callback([
        Output('expected_performance', 'children'),
        Output("sla_header", "children"),
    ],
    [
        Input('NoPerDay', 'value'),
        Input('RegistrationDesks', 'value'),
        Input('VaccineDesks', 'value'),
        Input('SeatingCap', 'value'),
        Input('RegistrationTime', 'value'),
        Input('VaccineTime', 'value'),
        Input('WaitingTime', 'value'),
        Input('percentile', 'value')
    ],

    )
def compute_expected_performance(
                            NoPerDay,
                            RegistrationDesks,
                            VaccineDesks,
                            SeatingCap,
                            RegistrationTime,
                            VaccineTime,
                            WaitingTime,
                            percentile,
                        ):

    scenario = {
        'NoPerDay': NoPerDay,
        # 'max_QueueOutside': max_QueueOutside,
        # 'max_wait': max_wait_reg,
        # 'max_wait_reg': max_wait_reg,
        # 'max_wait_vac': max_wait_vac,
        # 'max_wait_obs': max_wait_obs,
        'measure': percentile,
        'settings': {
            'RegistrationDesks': RegistrationDesks,
            'VaccineDesks': VaccineDesks,
            'SeatingCap': SeatingCap,
            'RegistrationTime': RegistrationTime,
            'VaccineTime': VaccineTime,
            'WaitingTime': WaitingTime,
        },
    }

    expected_performance = q_manager.expected_performance(scenario)

    # result, expected_performance_df, alternate_solutions_df = q_manager.evaluate_scenario(scenario)

    expected_performance = {column_names[k] if column_names.get(k) is not None else k: v for k, v in expected_performance.items()}

    expected_performance_df = pd.DataFrame(list(expected_performance.items()),columns = ['KPI', f'Expected Performance ({percentile_options[percentile]})'])
    # # for index, row in df.iterrows():
    # #     if type(row['Value']) is dict or type(row['Value']) is list:
    # #         row['Value'] = json.dumps(row['Value'])

    expected_performance_table = dash_table.DataTable(
        id='stats_table',
        style_header={
            'font-family':'sans-serif',
            'font-size': '16px',
            'whiteSpace': 'normal',
            'text-align': 'center',
            # 'font-weight': 'bold',
            'height': 'auto',
            'width': 'auto',
            'background-color': 'RebeccaPurple',
            'color': 'white',
            'padding-left': '10px',
            'padding-right': '10px',
        },
        style_data={
            'font-family':'sans-serif',
            'textAlign': 'center',
            'font-size': '16px',
            'whiteSpace': 'normal',
            # 'height': 'auto',
            'width': 'auto',
            'min-height': '80px',
            'padding-left': '10px',
            'padding-right': '10px',
        },
        style_data_conditional=[{
            'if': {
                'column_id': ['KPI'],
            },
            'textAlign': 'left',
            'width': '70%'
        }],
        columns=[{
            "name": i,
            "id": i,
            'type': 'numeric',
            'format': Format(nully='NA')} for i in expected_performance_df.columns],
        style_as_list_view=True,
        data=expected_performance_df.to_dict('records'),
        # row_selectable='multi',
    )

    sla_header = f'{percentile_options[percentile]} Waiting time SLA (Mins):'

    return [expected_performance_table, sla_header]



@app.callback([
        Output('recommendation_table', 'children'),
        # Output('expected_performance', 'children'),
        Output('alternate_solutions', 'children'),
        Output('compute_recommendation', 'n_clicks'),
    ],
    [
        Input('compute_recommendation', 'n_clicks'),
    ],
    [
        State('RegistrationDesks', 'value'),
        State('RegistrationDeskSearch', 'value'),
        State('VaccineDesks', 'value'),
        State('VaccineDeskSearch', 'value'),
        State('SeatingCap', 'value'),
        State('SeatingCapSearch', 'value'),
        State('RegistrationTime', 'value'),
        State('RegistrationTimeSearch', 'value'),
        State('VaccineTime', 'value'),
        State('VaccineTimeSearch', 'value'),
        State('WaitingTime', 'value'),
        State('WaitingTimeSearch', 'value'),
        State('max_QueueOutside', 'value'),
        State('max_wait_reg', 'value'),
        State('max_wait_vac', 'value'),
        State('max_wait_obs', 'value'),
        State('NoPerDay', 'value'),
        State('percentile', 'value'),
    ])
def compute_recommendation(n, RegistrationDesks, RegistrationDeskSearch,
                                VaccineDesks, VaccineDeskSearch,
                                SeatingCap, SeatingCapSearch,
                                RegistrationTime, RegistrationTimeSearch,
                                VaccineTime, VaccineTimeSearch,
                                WaitingTime, WaitingTimeSearch,
                                max_QueueOutside, max_wait_reg, max_wait_vac, max_wait_obs, NoPerDay,
                                percentile):

    if n > 0:
        ''' '''
        scenario = {
            'NoPerDay': NoPerDay,
            'max_QueueOutside': max_QueueOutside,
            'max_wait': max_wait_reg,
            'max_wait_reg': max_wait_reg,
            'max_wait_vac': max_wait_vac,
            'max_wait_obs': max_wait_obs,
            'measure': percentile,
            'settings': {
                'RegistrationDesks': RegistrationDesks,
                'VaccineDesks': VaccineDesks,
                'SeatingCap': SeatingCap,
                'RegistrationTime': RegistrationTime,
                'VaccineTime': VaccineTime,
                'WaitingTime': WaitingTime,
            },
            'search': {
                'RegistrationDesks': RegistrationDeskSearch,
                'VaccineDesks': VaccineDeskSearch,
                'SeatingCap': SeatingCapSearch,
                'RegistrationTime': RegistrationTimeSearch,
                'VaccineTime': VaccineTimeSearch,
                'WaitingTime': WaitingTimeSearch,
            },
        }

        # result, expected_performance_df, alternate_solutions_df = q_manager.evaluate_scenario(scenario)
        result, alternate_solutions_df = q_manager.evaluate_scenario(scenario)

        result = {column_names[k] if column_names.get(k) is not None else k: v for k, v in result.items()}

        results_df = pd.DataFrame(list(result.items()),columns = ['Option', 'Recommended Actions'])
        # for index, row in df.iterrows():
        #     if type(row['Value']) is dict or type(row['Value']) is list:
        #         row['Value'] = json.dumps(row['Value'])

        results_table = dash_table.DataTable(
            id='stats_table',
            style_header={
                'font-family':'sans-serif',
                'font-size': '16px',
                'whiteSpace': 'normal',
                'text-align': 'center',
                # 'font-weight': 'bold',
                'height': 'auto',
                'width': 'auto',
                'background-color': '#3D9970',
                'color': 'white',
                'padding-left': '10px',
                'padding-right': '10px',
            },
            style_data={
                'font-family':'sans-serif',
                'textAlign': 'left',
                'font-size': '16px',
                'whiteSpace': 'normal',
                'height': 'auto',
                'width': 'auto',
                'min-height': '80px',
                'padding-left': '10px',
                'padding-right': '10px',
            },
            style_data_conditional=[{
                'if': {
                    'column_id': ['Recommended Actions'],
                },
                'textAlign': 'center',
            }],
            # style_table={
            #     'width': '100%'
            # },
            columns=[{"name": i, "id": i} for i in results_df.columns],
            style_as_list_view=True,
            data=results_df.to_dict('records'),
            # row_selectable='multi',
        )

        # expected_performance_table = dash_table.DataTable(
        #     id='stats_table',
        #     style_header={
        #         'font-family':'sans-serif',
        #         'font-size': '16px',
        #         'whiteSpace': 'normal',
        #         'text-align': 'center',
        #         'font-weight': 'bold',
        #         'height': 'auto',
        #         # 'width': 'auto',
        #         'min-width': '80px',
        #         'background-color': 'saddlebrown',
        #         'color': 'white'
        #     },
        #     style_header_conditional=[
        #     {
        #         'if': {
        #             'column_id': ['W1', 'W2', 'W3', 'QueueOutside', 'score'],
        #         },
        #         'backgroundColor': 'RebeccaPurple',
        #         'color': 'white'
        #     },],
        #     style_data={
        #         'font-family':'sans-serif',
        #         'textAlign': 'center',
        #         'font-size': '16px',
        #         'whiteSpace': 'normal',
        #         # 'height': 'auto',
        #         # 'width': 'auto',
        #         'min-width': '80px',
        #         'min-height': '80px'
        #     },
        #     columns=[{"name": column_names[i] if column_names.get(i) is not None else i, "id": i} for i in expected_performance_df.columns],
        #     style_as_list_view=False,
        #     data=expected_performance_df.to_dict('records'),
        #     # row_selectable='multi',
        # )

        alternate_solutions_table = dash_table.DataTable(
            id='stats_table',
            style_header={
                'font-family':'sans-serif',
                'font-size': '16px',
                'whiteSpace': 'normal',
                'text-align': 'center',
                # 'font-weight': 'bold',
                'height': 'auto',
                # 'width': 'auto',
                'min-width': '80px',
                'background-color': 'DimGray',
                'color': 'white'
            },
            style_header_conditional=[
            {
                'if': {
                    'column_id': ['W1', 'W2', 'W3', 'QueueOutside', 'score'],
                },
                'backgroundColor': 'RebeccaPurple',
                'color': 'white'
            },],
            style_data={
                'font-family':'sans-serif',
                'textAlign': 'center',
                'font-size': '16px',
                'whiteSpace': 'normal',
                # 'height': 'auto',
                # 'width': 'auto',
                'min-width': '80px',
                'min-height': '80px'
            },
            # columns=[{"name": i, "id": i} for i in alternate_solutions_df.columns],
            columns=[{"name": column_names[i] if column_names.get(i) is not None else i, "id": i} for i in alternate_solutions_df.columns if column_names.get(i) is not None],
            style_as_list_view=False,
            data=alternate_solutions_df.to_dict('records'),
            page_current=0,
            page_size=25,
            page_action='native',
            # sort_action='native',
            # sort_mode='multi',
            # filter_action='native',

        )

        # return results_table, expected_performance_table, alternate_solutions_table, 0
        return results_table, alternate_solutions_table, 0

    return None, None, 0



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8100)
