import pandas as pd
import os

class DataManager:
    ''' '''

    def __init__(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.df = pd.read_csv(f'{dir_path}/data/final_results_cleaned.csv')

        self.min_extents = self.df.min().to_dict()
        self.max_extents = self.df.max().to_dict()

        self.RegistrationDesks = self.df['RegistrationDesks'].unique()
        self.VaccineDesks = self.df['VaccineDesks'].unique()
        self.SeatingCap = self.df['SeatingCap'].unique()
        self.NoPerDay = self.df['NoPerDay'].unique()

        self.RegistrationTime = self.df['RegistrationTime'].unique()
        self.VaccineTime = self.df['VaccineTime'].unique()
        self.Waitingtime = self.df['Waitingtime'].unique()


    def check_threshold(self, row, max_wait, max_QueueOutside):
        return row['W1'] <= max_wait and \
            row['W2'] <= max_wait and \
            row['W3'] <= max_wait and \
            row['QueueOutside'] <= max_QueueOutside


    def evaluate_scenario(self, scenario):

        settings = scenario['settings']
        recommendation = {}
        # overall = ''

        for k, v in settings.items():
            cond = None
            for key, val in  settings.items():
                if key == k:
                    continue

                if cond is None:
                    cond = (self.df[key] == val)
                else:
                    cond = cond & (self.df[key] == val)

            filtered_df = self.df[cond & (self.df['NoPerDay']==scenario['NoPerDay'])]

            if (len(filtered_df) == 0) or len(filtered_df[filtered_df[k]==v]) == 0:
                recommendation[k] = 'Scenario not available'
            else:
                filtered_base_df = filtered_df[(filtered_df[k]==v)].reset_index()
                filtered_alt_df = filtered_df[~(filtered_df[k]==v)].reset_index()

                if self.check_threshold(filtered_base_df.loc[0], scenario['max_wait'], scenario['max_QueueOutside']):
                    recommendation[k] = 'Sufficient'
                else:
                    found_solution = False
                    for index, row in filtered_alt_df.sort_values(k).iterrows():
                        if self.check_threshold(row, scenario['max_wait'], scenario['max_QueueOutside']):
                            found_solution = True
                            recommendation[k] = f"Must Increase {k} to {int(row[k])}"
                            break
                    if found_solution == False:
                        recommendation[k] = f'Increasing {k} up to max ({int(self.max_extents[k])}) has No Impact'




        return recommendation



