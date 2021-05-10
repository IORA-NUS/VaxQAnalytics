from numpy import inf
import pandas as pd
import os

import time


class DataManager:
    ''' '''

    def __init__(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        # self.df = pd.read_csv(f'{self.dir_path}/data/final_results_cleaned.csv')

        self.df = pd.read_csv(f'{self.dir_path}/data/results_20210504_11hrs.csv')

        self.min_extents = self.df.min().to_dict()
        self.max_extents = self.df.max().to_dict()

        self.RegistrationDesks = self.df['RegistrationDesks'].unique()
        self.VaccineDesks = self.df['VaccineDesks'].unique()
        self.SeatingCap = self.df['SeatingCap'].unique()
        self.NoPerDay = self.df['NoPerDay'].unique()

        self.RegistrationTime = self.df['RegistrationTime'].unique()
        self.VaccineTime = self.df['VaccineTime'].unique()
        self.WaitingTime = self.df['WaitingTime'].unique()


    def check_threshold(self, row, max_wait_reg, max_wait_vac, max_wait_obs, max_QueueOutside):
        return row['W1'] <= max_wait_reg and \
            row['W2'] <= max_wait_vac and \
            row['W3'] <= max_wait_obs and \
            row['QueueOutside'] <= max_QueueOutside

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

        expected_performance_df = self.df[all_cond & (self.df['NoPerDay']==scenario['NoPerDay'])]
        if len(expected_performance_df) == 0:
            expected_performance_df = pd.DataFrame([settings])
            expected_performance_df['W1'] = 'NA'
            expected_performance_df['W2'] = 'NA'
            expected_performance_df['W3'] = 'NA'
            expected_performance_df['QueueOutside'] = 'NA'

        expected_performance_df.fillna('inf', inplace=True)
        # print(expected_performance_df)

        search_cond = (self.df['NoPerDay']==scenario['NoPerDay']) & \
                        (self.df['W1'] <= scenario['max_wait_reg']) & \
                        (self.df['W2'] <= scenario['max_wait_vac']) & \
                        (self.df['W3'] <= scenario['max_wait_obs']) & \
                        (self.df['QueueOutside'] <= scenario['max_QueueOutside'])

        for key, val in  settings.items():
            if search[key] =='Fixed':
                search_cond = search_cond & (self.df[key] == val)

        alternate_solutions = self.df[search_cond]
        alternate_solutions['score'] = 0

        print(len(alternate_solutions))

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



        # for k, v in settings.items():
        #     cond = None
        #     for key, val in  settings.items():
        #         if key == k:
        #             continue

        #         if cond is None:
        #             # cond = (self.df[key] == val)
        #             cond = (alternate_solutions[key] == val)
        #         else:
        #             # cond = cond & (self.df[key] == val)
        #             cond = cond & (alternate_solutions[key] == val)

        #     # filtered_df = self.df[cond & (self.df['NoPerDay']==scenario['NoPerDay'])]
        #     filtered_df = alternate_solutions[cond]

        #     # if (len(filtered_df) == 0) or len(filtered_df[filtered_df[k]==v]) == 0:
        #     if (len(filtered_df) == 0):
        #         recommendation[k] = 'Unable to evaluate Scenario'
        #     else:
        #         filtered_base_df = filtered_df[(filtered_df[k]==v)].reset_index()
        #         filtered_alt_df = filtered_df[~(filtered_df[k]==v)].reset_index()

        #         if (len(filtered_base_df) > 0) and (self.check_threshold(filtered_base_df.loc[0], scenario['max_wait_reg'], scenario['max_wait_vac'], scenario['max_wait_obs'], scenario['max_QueueOutside'])):
        #             recommendation[k] = 'Sufficient'
        #         else:
        #             found_solution = False
        #             for index, row in filtered_alt_df[filtered_alt_df[k] > v].sort_values(k).iterrows():
        #                 if self.check_threshold(row, scenario['max_wait_reg'], scenario['max_wait_vac'], scenario['max_wait_obs'], scenario['max_QueueOutside']):
        #                     found_solution = True
        #                     recommendation[k] = f"Suggest to Increase {k} to {int(row[k])}"
        #                     break
        #                     # if int(row[k]) > v:
        #                     #     recommendation[k] = f"Suggest to Increase {k} to {int(row[k])}"
        #                     # else:
        #                     #     recommendation[k] = f"Suggest to  Decrease {k} to {int(row[k])}"
        #                     # break
        #             if not found_solution:
        #                 for index, row in filtered_alt_df[filtered_alt_df[k] < v].sort_values(k, ascending=False).iterrows():
        #                     if self.check_threshold(row, scenario['max_wait_reg'], scenario['max_wait_vac'], scenario['max_wait_obs'], scenario['max_QueueOutside']):
        #                         found_solution = True
        #                         recommendation[k] = f"Suggest to  Decrease {k} to {int(row[k])}"
        #                         break
        #                         # if int(row[k]) > v:
        #                         #     recommendation[k] = f"Suggest to Increase {k} to {int(row[k])}"
        #                         # else:
        #                         #     recommendation[k] = f"Suggest to  Decrease {k} to {int(row[k])}"
        #                         # break

        #             if found_solution == False:
        #                 recommendation[k] = f'Adjusting {k} between ({int(self.min_extents[k])}, {int(self.max_extents[k])}) has No Impact'

        # # print(recommendation)

        return recommendation, expected_performance_df, alternate_solutions



