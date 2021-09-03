# from vaxqa.vaxqa.data_manager.data_manager import DataManager
import numpy as np
import pandas as pd
import os, json, time, math

from pathlib import Path
from vaxqa.data_manager.data_handler import DataHandler
from .simulate_q_approx import simulateQApprox


class QueryManager:
    ''' '''
    df = None
    servers = ['RegistrationDesks', 'VaccineDesks', 'SeatingCap']
    service_times = ['RegistrationTime', 'VaccineTime', 'WaitingTime']
    # data_settings = {
    #     'NoPerDay': None,
    #     'measure': None
    # }

    # def __init__(self, filename=None):
    def __init__(self):

        # self.dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

        self.ptile_multiplier = {
            'Avg': 1,
            '90': 2.645,
            '95': 2.960,
        }
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

    def compute_performance(self, scenario):

        N = scenario['NoPerDay']
        K1 = scenario['settings']['RegistrationDesks']
        K2 = scenario['settings']['VaccineDesks']
        K3 = scenario['settings']['SeatingCap']
        S1 = scenario['settings']['RegistrationTime']
        S2 = scenario['settings']['VaccineTime']
        S3 = scenario['settings']['WaitingTime']
        # print(N,S1,S2,S3,K1,K2,K3)

        result = simulateQApprox(N, S1, S2, S3, K1, K2, K3, 'Avg')

        performance = {
            'W1': result[7] if result[7] == 'NA' else result[7] * self.ptile_multiplier[scenario['measure']],
            'W2': result[8] if result[8] == 'NA' else result[8] * self.ptile_multiplier[scenario['measure']],
            'W3': result[9] if result[9] == 'NA' else result[9] * self.ptile_multiplier[scenario['measure']],
            'QueueOutside': result[10] if result[10] == 'NA' else result[10] * self.ptile_multiplier[scenario['measure']]
        }

        return performance


    def expected_performance(self, scenario):

        # N = scenario['NoPerDay']
        # K1 = scenario['settings']['RegistrationDesks']
        # K2 = scenario['settings']['VaccineDesks']
        # K3 = scenario['settings']['SeatingCap']
        # S1 = scenario['settings']['RegistrationTime']
        # S2 = scenario['settings']['VaccineTime']
        # S3 = scenario['settings']['WaitingTime']
        # # print(N,S1,S2,S3,K1,K2,K3)

        # result = simulateQApprox(N, S1, S2, S3, K1, K2, K3, 'Avg')

        # W1 = result[7]
        # W2 = result[8]
        # W3 = result[9]
        # QueueOutside = result[10]

        perf = self.compute_performance(scenario)

        retval = {
            'W1': perf['W1'] if perf['W1'] == 'NA' else f"{round(perf['W1'])} (~ {round(perf['W1']/60)} mins)",
            'W2': perf['W2'] if perf['W2'] == 'NA' else f"{round(perf['W2'])} (~ {round(perf['W2']/60)} mins)",
            'W3': perf['W3'] if perf['W3'] == 'NA' else f"{round(perf['W3'])} (~ {round(perf['W3']/60)} mins)",
            'QueueOutside': perf['QueueOutside'] if perf['QueueOutside'] == 'NA' else round(perf['QueueOutside'])
        }

        # self.df = self.data_set.refresh_df(scenario['NoPerDay'], scenario['measure'])

        # settings = scenario['settings']

        # all_cond = None
        # for key, val in  settings.items():
        #     if all_cond is None:
        #         all_cond = (self.df[key] == val)
        #     else:
        #         all_cond = all_cond & (self.df[key] == val)

        # expected_performance_df = self.df[all_cond & (self.df['NoPerDay']==scenario['NoPerDay']) & (self.df['measure']==scenario['measure'])]

        # if len(expected_performance_df) == 0:
        #     retval = {
        #         'W1': 'NA',
        #         'W2': 'NA',
        #         'W3': 'NA',
        #         'QueueOutside': 'NA'
        #     }
        # else:
        #     try:
        #         # print(expected_performance_df)
        #         expected_performance_df.reset_index(drop=True, inplace=True)
        #         resp = expected_performance_df.loc[0]
        #         retval = {
        #             'W1': f"{resp.at['W1']} (~ {round(resp.at['W1']/60)} mins)", #f"{resp.at['W1']//60}:{resp.at['W1']%60}",
        #             'W2': f"{resp.at['W2']} (~ {round(resp.at['W2']/60)} mins)", #f"{resp.at['W2']//60}:{resp.at['W2']%60}",
        #             'W3': f"{resp.at['W3']} (~ {round(resp.at['W3']/60)} mins)", #f"{resp.at['W3']//60}:{resp.at['W3']%60}",
        #             'QueueOutside': resp.at['QueueOutside'],
        #         }
        #     except:
        #         retval = {
        #             'W1': 'NA',
        #             'W2': 'NA',
        #             'W3': 'NA',
        #             'QueueOutside': 'NA'
        #         }

        return retval

    def evaluate_scenario(self, scenario):

        settings = scenario['settings']
        search = scenario['search']
        recommendation = {}

        perf = self.compute_performance(scenario)

        if perf['W1'] != 'NA':
            if (perf['W1'] <= scenario['max_wait_reg']) & \
                    (perf['W2'] <= scenario['max_wait_vac']) & \
                    (perf['W3'] <= scenario['max_wait_obs']) & \
                    (perf['QueueOutside'] <= scenario['max_QueueOutside']):

                for k, v in settings.items():
                    recommendation[k] = 'Sufficient'

                return recommendation, pd.DataFrame()

        multiplier = self.ptile_multiplier[scenario['measure']]

        # self.df = self.data_set.refresh_df(scenario['NoPerDay'], scenario['measure'])
        self.df = self.data_set.refresh_df(scenario['NoPerDay'], 'Avg')

        # search_cond = (self.df['measure']==scenario['measure']) & \
        search_cond = (self.df['measure']=='Avg') & \
                        (self.df['NoPerDay']==scenario['NoPerDay']) & \
                        (self.df['W1'] * multiplier <= scenario['max_wait_reg']) & \
                        (self.df['W2'] * multiplier <= scenario['max_wait_vac']) & \
                        (self.df['W3'] * multiplier <= scenario['max_wait_obs']) & \
                        (self.df['QueueOutside'] * multiplier <= scenario['max_QueueOutside'])

        # for key, val in  settings.items():
        #     if search[key] =='Fixed':
        #         search_cond = search_cond & (self.df[key] == val)


        for key, val in  settings.items():
            if key in self.servers:
                if search[key] =='Fixed':
                    valid_list = self.df[key].unique()
                    new_val = min(valid_list, key=lambda x:abs(val-x) if x <= val else np.Inf)
                    # print(new_val)
                    search_cond = search_cond & (self.df[key] == new_val)
                else:
                    search_cond = search_cond & (self.df[key] >= val)
            elif key in self.service_times:
                if search[key] =='Fixed':
                    valid_list = self.df[key].unique()
                    new_val = min(valid_list, key=lambda x:abs(x-val) if x >= val else np.Inf)
                    # print(new_val)
                    search_cond = search_cond & (self.df[key] == new_val)
                else:
                    search_cond = search_cond & (self.df[key] <= val)

            # if search[key] =='Fixed':
            #     valid_list = self.df[key].unique()
            #     if key in self.servers:
            #         new_val = min(valid_list, key=lambda x:abs(val-x) if x <= val else 99999)
            #         print(new_val)
            #         search_cond = search_cond & (self.df[key] == new_val)
            #     elif key in self.service_times:
            #         new_val = min(valid_list, key=lambda x:abs(x-val) if x >= val else 99999)
            #         print(new_val)
            #         search_cond = search_cond & (self.df[key] == new_val)


        alternate_solutions = self.df[search_cond]
        alternate_solutions['W1'] = alternate_solutions['W1'] * multiplier
        alternate_solutions['W2'] = alternate_solutions['W2'] * multiplier
        alternate_solutions['W3'] = alternate_solutions['W3'] * multiplier
        alternate_solutions['QueueOutside'] = alternate_solutions['QueueOutside'] * multiplier
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

        alternate_solutions = alternate_solutions.sort_values('score').reset_index(drop=True).head(100)
        # print(f"Sort: {time.time() - now}")
        # now = time.time()

        if len(alternate_solutions) > 0:
            optimal = alternate_solutions.iloc[0]
            alt_df = self.get_feasible_intermediates(scenario, optimal)
            alt_df['score'] = alt_df.apply(distance_score, axis=1)
            # print(alt_df)
            alternate_solutions = alternate_solutions.append(alt_df)

        alternate_solutions.drop_duplicates(inplace=True)

        alternate_solutions = alternate_solutions.sort_values('score').reset_index(drop=True)

        if len(alternate_solutions) > 0:
            optimal = alternate_solutions.iloc[0]

            for k, v in settings.items():
                if (k in self.servers) and (optimal[k] <= v):
                    recommendation[k] = 'Sufficient'
                elif (k in self.service_times) and (optimal[k] >= v):
                    recommendation[k] = 'Sufficient'
                else:
                    recommendation[k] = f'Suggest to Adjust {k} to {optimal[k]}'

            # for k, v in settings.items():
            #     if optimal[k] == v:
            #         recommendation[k] = 'Sufficient'
            #     elif optimal[k] < v:
            #         recommendation[k] = f'Suggest to  Decrease {k} to {int(optimal[k])}'
            #     else:
            #         recommendation[k] = f'Suggest to increase {k} to {int(optimal[k])}'
        else:
            recommendation['error'] = 'Unable to Find a feasible alternative within the bounds'

        # print(recommendation)

        return recommendation, alternate_solutions


    def get_feasible_intermediates(self, scenario, optimal):

        N0 = scenario['NoPerDay']
        ptile = scenario['measure']
        extents = self.get_extents()

        # K1_curr = scenario['settings']['RegistrationDesks']
        # K2_curr = scenario['settings']['VaccineDesks']
        # K3_curr = scenario['settings']['SeatingCap']
        # S1_curr = scenario['settings']['RegistrationTime']
        # S2_curr = scenario['settings']['VaccineTime']
        # S3_curr = scenario['settings']['WaitingTime']

        K1_opt = optimal['RegistrationDesks']
        K2_opt = optimal['VaccineDesks']
        K3_opt = optimal['SeatingCap']
        S1_opt = optimal['RegistrationTime']
        S2_opt = optimal['VaccineTime']
        S3_opt = optimal['WaitingTime']

        K1_vals = np.array(self.data_set.extents['RegistrationDesks'])
        K2_vals = np.array(self.data_set.extents['VaccineDesks'])
        K3_vals = np.array(self.data_set.extents['SeatingCap'])
        S1_vals = np.array(self.data_set.extents['RegistrationTime'])
        S2_vals = np.array(self.data_set.extents['VaccineTime'])
        S3_vals = np.array(self.data_set.extents['WaitingTime'])

        # print(K1_vals, K1_vals[(K1_vals>=K1_curr) * (K1_vals<=K1_opt)])
        # print(K2_vals, K2_vals[(K2_vals>=K2_curr) * (K2_vals<=K2_opt)])
        # print(K3_vals, K3_vals[(K3_vals>=K3_curr) * (K3_vals<=K3_opt)])
        # print(S1_vals, S1_vals[(S1_vals<=S1_curr) * (S1_vals>=S1_opt)])
        # print(S2_vals, S2_vals[(S2_vals<=S2_curr) * (S2_vals>=S2_opt)])
        # print(S3_vals, S3_vals[(S3_vals<=S3_curr) * (S3_vals>=S3_opt)])


        # for k10 in K1_vals[(K1_vals>=K1_curr) * (K1_vals<=K1_opt)]: # RegistrationDesks
        #     for k20 in K2_vals[(K2_vals>=K2_curr) * (K2_vals<=K2_opt)]: # VaccineDesks
        #         for k30 in  K3_vals[(K3_vals>=K3_curr) * (K3_vals<=K3_opt)]: # SeatingCap
        #             for s1 in S1_vals[(S1_vals<=S1_curr) * (S1_vals>=S1_opt)]: #range(12, 21): # range(6, 11): # RegistrationTime
        #                 for s2 in S2_vals[(S2_vals<=S2_curr) * (S2_vals>=S2_opt)]: # range(12, 21): # range(6, 11): # VaccineTime
        #                     for s3 in S3_vals[(S3_vals<=S3_curr) * (S3_vals>=S3_opt)]: # WaitingTime Observation area
        #                         x=simulateQApprox(N0,s1,s2,s3,k10,k20,k30, ptile)
        #                         print(x)

        # print(K1_vals, K1_vals[(K1_vals>=K1_opt-0) * (K1_vals<=K1_opt)])
        # print(K2_vals, K2_vals[(K2_vals>=K2_opt-0) * (K2_vals<=K2_opt)])
        # print(K3_vals, K3_vals[(K3_vals>=K3_opt-5) * (K3_vals<=K3_opt)])
        # print(S1_vals, S1_vals[(S1_vals<=S1_opt+0.5) * (S1_vals>=S1_opt)])
        # print(S2_vals, S2_vals[(S2_vals<=S2_opt+0.5) * (S2_vals>=S2_opt)])
        # print(S3_vals, S3_vals[(S3_vals<=S3_opt+0) * (S3_vals>=S3_opt)])

        columns = ['NoPerDay', 'RegistrationTime', 'VaccineTime', 'WaitingTime' ,'RegistrationDesks','VaccineDesks','SeatingCap','W1','W2','W3','QueueOutside','measure']

        alt_df = pd.DataFrame(columns=columns)

        for k10 in K1_vals[(K1_vals>K1_opt-extents['RegistrationDesks_search']) * (K1_vals<=K1_opt)]: # RegistrationDesks
            for k20 in K2_vals[(K2_vals>K2_opt-extents['VaccineDesks_search']) * (K2_vals<=K2_opt)]: # VaccineDesks
                for k30 in  K3_vals[(K3_vals>K3_opt-extents['SeatingCap_search']) * (K3_vals<=K3_opt)]: # SeatingCap
                    for s1 in S1_vals[(S1_vals<S1_opt+extents['RegistrationTime_search']) * (S1_vals>=S1_opt)]: #range(12, 21): # range(6, 11): # RegistrationTime
                        for s2 in S2_vals[(S2_vals<S2_opt+extents['VaccineTime_search']) * (S2_vals>=S2_opt)]: # range(12, 21): # range(6, 11): # VaccineTime
                            for s3 in S3_vals[(S3_vals<S3_opt+extents['WaitingTime_search']) * (S3_vals>=S3_opt)]: # WaitingTime Observation area
                                x=simulateQApprox(N0,s1,s2,s3,k10,k20,k30, ptile)
                                # print(x)
                                if (x[7] <= scenario['max_wait_reg']) & \
                                        (x[8] <= scenario['max_wait_vac']) & \
                                        (x[9] <= scenario['max_wait_obs']) & \
                                        (x[10] <= scenario['max_QueueOutside']):

                                    alt_df = alt_df.append(pd.DataFrame(
                                            [list(x) + ['Avg']],
                                            columns=columns
                                        )
                                    )

        return alt_df
