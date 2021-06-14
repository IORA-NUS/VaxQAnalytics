
import os, shutil
from logic.simulate_q_approx import simulateQApprox
import csv

import multiprocessing as mp
from multiprocessing import Pool

def generate_data(N0):

    data_path = f'{os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))}/data'
    scenario = 'results_cleaned_20210612'

    fields = ['NoPerDay', 'RegistrationTime', 'VaccineTime', 'WaitingTime' ,'RegistrationDesks','VaccineDesks','SeatingCap','W1','W2','W3','QueueOutside','measure']

    # for N0 in range(1500, 4001, 50): # NoPerDay
    for ptile in ['Avg']: #['Avg', 90, 95]: # percentile response
        with open(f'{data_path}/{scenario}/NoPerDay_{N0}_measure_{ptile}.csv', 'w+') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(fields)

            for k10 in range (7, 21, 1): # RegistrationDesks
                for k20 in range(8, 21, 1): # VaccineDesks
                    for k30 in range(40, 251, 2): # SeatingCap
                        for s1 in range(12, 21): # range(6, 11): # RegistrationTime
                            s1_adj = s1/4 # s1/2
                            for s2 in range(12, 21): # range(6, 11): # VaccineTime
                                s2_adj = s2/4 # s2/2 #
                                for s3 in range(15, 31, 5): # WaitingTime Observation area
                                    try:
                                        x=simulateQApprox(N0,s1_adj,s2_adj,s3,k10,k20,k30, ptile)
                                        if x[-1] != 'nan':
                                            row = [f'{val:0.2f}' if type(val)==float else f'{val}' for val in x]
                                            row.extend([ptile])
                                            csv_writer.writerow(row)
                                    except Exception as e:
                                        print(e)
                                        print(N0,s1_adj,s2_adj,s3,k10,k20,k30, ptile)
                                        raise e

    print(f"N0: {N0}")


if __name__ == '__main__':
    p = Pool(8)

    N0_list = list(range(1500, 4001, 50))
    with p:
        p.map(generate_data, N0_list)



