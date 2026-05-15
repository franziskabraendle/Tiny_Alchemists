import numpy as np
import pandas as pd

def store_regression_data(data, time, z_score, model_type, memory_type, group, stepsused):
    """Writes player utilities for later regression to csv file.

    Args:
        data (DataFrame): Data holding information on (1) player id, (2) decision between two arms,
                    (3)-(6) differences for values of model strategies
        time (str): Timestamp.
        z_score (boolean): True if z score for model differences should be caculated, False otherwise.
        model_type (str): Model type, which is either 'human' or any selection from 'base', 'emp', 'bin', 'trueemp',
                    'truebin', 'cbv', 'sim' or 'cbu' if data is generated for simulated data.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)
        group (str): 'children' or 'adults'.
                    States what player data set is going to be used.
        stepsused (int): Number of trials that were considered.
    """
    if z_score is True:
        z_score = '-scaled'
    else:
        z_score = ''
    if stepsused is None:
        stepsused = ''
    else:
        stepsused = str(stepsused)

    filename = 'empowermentexploration/data/regression/{}-childrenalchemy-valuedifferences-{}{}-{}-{}{}.csv'.format(time, model_type, z_score, memory_type, group, stepsused)
    data.to_csv(filename, index=False)
    unique_players = data['id'].unique()
    print("Number of players: {}".format(len(unique_players)))
