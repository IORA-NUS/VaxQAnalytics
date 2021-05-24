from numpy import inf
import pandas as pd
import os

import time


class DataManager:
    ''' '''

    def __init__(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        # self.df = pd.read_csv(f'{self.dir_path}/data/final_results_cleaned.csv')
        # self.df = pd.read_csv(f'{self.dir_path}/data/results_20210504_11hrs.csv')
        self.df = pd.read_csv(f'{self.dir_path}/data/results_cleaned_20210521.csv', dtype={'measure': 'str'})

        self.min_extents = self.df.min().to_dict()
        self.max_extents = self.df.max().to_dict()

        self.RegistrationDesks = self.df['RegistrationDesks'].unique()
        self.VaccineDesks = self.df['VaccineDesks'].unique()
        self.SeatingCap = self.df['SeatingCap'].unique()
        self.NoPerDay = self.df['NoPerDay'].unique()

        self.RegistrationTime = self.df['RegistrationTime'].unique()
        self.VaccineTime = self.df['VaccineTime'].unique()
        self.WaitingTime = self.df['WaitingTime'].unique()
        self.measure = self.df['measure'].unique()


    def check_threshold(self, row, max_wait_reg, max_wait_vac, max_wait_obs, max_QueueOutside):
        return row['W1'] <= max_wait_reg and \
            row['W2'] <= max_wait_vac and \
            row['W3'] <= max_wait_obs and \
            row['QueueOutside'] <= max_QueueOutside

    def expected_performance(self, scenario):

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
            # print(expected_performance_df)
            expected_performance_df.reset_index(drop=True, inplace=True)
            retval = {
                'W1': expected_performance_df.at[0, 'W1'],
                'W2': expected_performance_df.at[0, 'W2'],
                'W3': expected_performance_df.at[0, 'W3'],
                'QueueOutside': expected_performance_df.at[0, 'QueueOutside'],
            }
        #     expected_performance_df = pd.DataFrame([settings])
        #     expected_performance_df['W1'] = 'NA'
        #     expected_performance_df['W2'] = 'NA'
        #     expected_performance_df['W3'] = 'NA'
        #     expected_performance_df['QueueOutside'] = 'NA'

        # expected_performance_df.fillna('inf', inplace=True)

        # return expected_performance_df
        # print(retval)
        return retval

    def evaluate_scenario(self, scenario):

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

        # expected_performance_df = self.df[all_cond & (self.df['NoPerDay']==scenario['NoPerDay'])]
        # if len(expected_performance_df) == 0:
        #     expected_performance_df = pd.DataFrame([settings])
        #     expected_performance_df['W1'] = 'NA'
        #     expected_performance_df['W2'] = 'NA'
        #     expected_performance_df['W3'] = 'NA'
        #     expected_performance_df['QueueOutside'] = 'NA'

        # expected_performance_df.fillna('inf', inplace=True)
        # print(expected_performance_df)

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


