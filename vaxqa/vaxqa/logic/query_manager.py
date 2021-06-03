# from vaxqa.vaxqa.data_manager.data_manager import DataManager
from numpy import inf
import pandas as pd
import os, json, time

from pathlib import Path
from data_manager.data_handler import DataHandler


class QueryManager:
    ''' '''
    df = None
    # data_settings = {
    #     'NoPerDay': None,
    #     'measure': None
    # }

    # def __init__(self, filename=None):
    def __init__(self):

        # self.dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

        # if scenario is None:
        #     raise Exception('Missing Scenario')
        # else:
        #     self.scenario_path = f"{self.dir_path}/data/{scenario}"

        self.data_set = DataHandler()

    def get_extents(self):

        # with open(f'{self.scenario_path}/extents.json') as file:
        #     extents = json.load(file)

        # return extents
        return self.data_set.get_extents()


    # def refresh_df(self, NoPerDay, measure):
    #     if self.df is None:
    #         self.data_settings['NoPerDay'] = NoPerDay
    #         self.data_settings['measure'] = measure

    #         self.df = pd.read_csv(f'{self.scenario_path}//NoPerDay_{NoPerDay}_measure_{measure}.csv', dtype={'measure': 'str'})

    #     elif (self.data_settings['NoPerDay'] != NoPerDay) or (self.data_settings['measure'] != measure):
    #         self.data_settings['NoPerDay'] = NoPerDay
    #         self.data_settings['measure'] = measure

    #         self.df = pd.read_csv(f'{self.scenario_path}//NoPerDay_{NoPerDay}_measure_{measure}.csv', dtype={'measure': 'str'})


    def check_threshold(self, row, max_wait_reg, max_wait_vac, max_wait_obs, max_QueueOutside):
        return row['W1'] <= max_wait_reg and \
            row['W2'] <= max_wait_vac and \
            row['W3'] <= max_wait_obs and \
            row['QueueOutside'] <= max_QueueOutside

    def expected_performance(self, scenario):

        # self.refresh_df(scenario['NoPerDay'], scenario['measure'])
        self.df = self.data_set.refresh_df(scenario['NoPerDay'], scenario['measure'])

        settings = scenario['settings']

        all_cond = None
        for key, val in  settings.items():
            if all_cond is None:
                all_cond = (self.df[key] == val)
            else:
                all_cond = all_cond & (self.df[key] == val)

        expected_performance_df = self.df[all_cond & (self.df['NoPerDay']==scenario['NoPerDay']) & (self.df['measure']==scenario['measure'])]

        if len(expected_performance_df) == 0:
            retval = {
                'W1': 'NA',
                'W2': 'NA',
                'W3': 'NA',
                'QueueOutside': 'NA'
            }
        else:
            try:
                # print(expected_performance_df)
                expected_performance_df.reset_index(drop=True, inplace=True)
                resp = expected_performance_df.loc[0]
                retval = {
                    'W1': f"{resp.at['W1']} (~ {round(resp.at['W1']/60)} mins)", #f"{resp.at['W1']//60}:{resp.at['W1']%60}",
                    'W2': f"{resp.at['W2']} (~ {round(resp.at['W2']/60)} mins)", #f"{resp.at['W2']//60}:{resp.at['W2']%60}",
                    'W3': f"{resp.at['W3']} (~ {round(resp.at['W3']/60)} mins)", #f"{resp.at['W3']//60}:{resp.at['W3']%60}",
                    'QueueOutside': resp.at['QueueOutside'],
                }
            except:
                retval = {
                    'W1': 'NA',
                    'W2': 'NA',
                    'W3': 'NA',
                    'QueueOutside': 'NA'
                }

        return retval

    def evaluate_scenario(self, scenario):

        # self.refresh_df(scenario['NoPerDay'], scenario['measure'])
        self.df = self.data_set.refresh_df(scenario['NoPerDay'], scenario['measure'])

        settings = scenario['settings']
        search = scenario['search']
        recommendation = {}

        # now = time.time()

        all_cond = None
        for key, val in  settings.items():
            if all_cond is None:
                all_cond = (self.df[key] == val)
            else:
                all_cond = all_cond & (self.df[key] == val)

        search_cond = (self.df['measure']==scenario['measure']) & \
                        (self.df['NoPerDay']==scenario['NoPerDay']) & \
                        (self.df['W1'] <= scenario['max_wait_reg']) & \
                        (self.df['W2'] <= scenario['max_wait_vac']) & \
                        (self.df['W3'] <= scenario['max_wait_obs']) & \
                        (self.df['QueueOutside'] <= scenario['max_QueueOutside'])

        for key, val in  settings.items():
            if search[key] =='Fixed':
                search_cond = search_cond & (self.df[key] == val)

        alternate_solutions = self.df[search_cond]
        alternate_solutions['score'] = 0

        # print(len(alternate_solutions))

        # print(f"Prep: {time.time() - now}")
        # now = time.time()

        def distance_score(row):
            score = 0
            for k, v in settings.items():
                score += pow((row[k] - v), 2)

            return score

        alternate_solutions['score'] = alternate_solutions.apply(distance_score, axis=1)

        # print(f"Compute Score: {time.time() - now}")
        # now = time.time()

        alternate_solutions = alternate_solutions.sort_values('score').reset_index(drop=True)
        # print(f"Sort: {time.time() - now}")
        # now = time.time()

        if len(alternate_solutions) > 0:
            optimal = alternate_solutions.iloc[0]

            for k, v in settings.items():
                if optimal[k] == v:
                    recommendation[k] = 'Sufficient'
                elif optimal[k] < v:
                    recommendation[k] = f'Suggest to  Decrease {k} to {int(optimal[k])}'
                else:
                    recommendation[k] = f'Suggest to  Increase {k} to {int(optimal[k])}'
        else:
            recommendation['error'] = 'Unable to Find a feasible alternative within the bounds'


        return recommendation, alternate_solutions


