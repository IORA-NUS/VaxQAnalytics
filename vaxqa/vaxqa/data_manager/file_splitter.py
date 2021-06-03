import json, os
import pandas as pd
from pathlib import Path

def split_file(scenario):
    '''
    Split into smaller files by Arrival rate and Percentile
    '''
    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

    Path(f"{dir_path}/data/{scenario}").mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(f'{dir_path}/data/{scenario}.csv', dtype={'measure': 'str'})

    arrival_rate_list = df['NoPerDay'].unique()
    percentile_list = df['measure'].unique()

    for NoPerDay in arrival_rate_list:
        for measure in percentile_list:
            df2 = df[(df['NoPerDay'] == NoPerDay) & (df['measure'] == measure)]

            df2.to_csv(f"{dir_path}/data/{scenario}/NoPerDay_{NoPerDay}_measure_{measure}.csv", index=False)

    extents = {
        "RegistrationDesks": df['RegistrationDesks'].unique().tolist(),
        "VaccineDesks": df['VaccineDesks'].unique().tolist(),
        "SeatingCap": df['SeatingCap'].unique().tolist(),
        "NoPerDay": df['NoPerDay'].unique().tolist(),
        "RegistrationTime": df['RegistrationTime'].unique().tolist(),
        "VaccineTime": df['VaccineTime'].unique().tolist(),
        "WaitingTime": df['WaitingTime'].unique().tolist(),
        "measure": df['measure'].unique().tolist(),
    }

    with open(f'{dir_path}/data/{scenario}/extents.json', 'w') as file:
        json.dump(extents, file)



if __name__ == "__main__":
    # DataManagerSplit.split_file('results_cleaned_20210527')
    split_file('results_cleaned_20210521')

