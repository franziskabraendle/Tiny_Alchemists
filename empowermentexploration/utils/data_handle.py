import json
import empowermentexploration.utils.helpers as helpers
import numpy as np
import pandas as pd


def get_combination_table(csv=True):
    """Returns a combination table with four columns:
        (1) first: element index
        (2) second: element index
        (3) success: 0 or 1
        (4) result: element index, if available

    Args:
        csv (bool, optional): True if csv version is to be returned, False for json file. Defaults to True.

    Returns:
        DataFrame or dict: Contains information about elements involved in combination.
    """

    if csv is True:
        combination_table = pd.read_csv('empowermentexploration/resources/littlealchemy/data/childrenalchemyCombinationTable.csv',
                                dtype={'first': int, 'second': int, 'success': int, 'result': int})
    else:
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyCombinationTable.json',
                  encoding='utf8') as infile:
            combination_table = json.load(infile, object_hook=helpers.jsonKeys2int)


    return combination_table


def get_wordvectors(vector_version='crawl300'):
    """Returns wordvectors.

    Args:
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on. Defaults to 'crawl300'.

    Returns:
        ndarray(dtype=float, ndim=2): Word vectors for elements of the given version.
    """

    if vector_version == 'ccen100' or vector_version == 'ccen300' or vector_version == 'crawl100' or vector_version == 'crawl300' or vector_version == 'wiki100' or vector_version == 'wiki300':
        vectors = np.loadtxt('empowermentexploration/resources/littlealchemy/data/childrenalchemyElementVectors-{}.txt'.format(vector_version))
    else:
        raise ValueError('Undefined vector_version: "{}". Use "ccen100", "ccen300", "crawl100", "crawl300", "wiki100" or "wiki300" instead.'.format(vector_version))

    return vectors

def get_gametree():
    """Returns the shortened childrenalchemy game tree.

    Returns:
        dict: Game tree information.
    """
    with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyShortenedGametree.json',
                  encoding='utf8') as infile:
            gametree = json.load(infile)
            gametree = {int(k):v for k,v in gametree.items()}

    return gametree

def get_parent_table():
    """Returns a parent table where each parent has its own dict entry consisting of all resulting children.

    Returns:
        dict: Parent table where each parent has its own dict entry consisting of all resulting children.
    """
    with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyParentTable.json',
                  encoding='utf8') as infile:
            parent_table = json.load(infile)
            parent_table = {int(k):v for k,v in parent_table.items()}

    return parent_table


def get_probability_table(split_version='data', vector_version='crawl300'):
    """Returns probability table from custom gametree.

    Args:
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.

    Returns:
        DataFrame: Probability table from custom gametree. Includes combination elements, true success and result,
                    predicted success and prediction for each element.
    """
    try:
        probability_table = pd.read_hdf('empowermentexploration/resources/customgametree/data/childrenalchemyGametreeTable-{}-{}.h5'.format(split_version, vector_version))

        return probability_table
    except:
        raise ValueError('Corresponding custom gametree table not found. Check if input was correct or create the needed table using "empowermentexploration.gametree"')

def get_empowerment_info(split_version='data', vector_version='crawl300'):
    """Returns empowerment info from custom gametree.

    Args:
        split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the empowerment info should be based on.
                    Defaults to 'crawl300'.

    Returns:
        DataFrame: Empowerment info from custom gametree. Includes combination elements, predicted success
                    and empowerment info for both calculation types (outgoing combination and children).
    """
    try:
        empowerment_info = pd.read_csv('empowermentexploration/resources/customgametree/data/childrenalchemyEmpowermentTable-{}-{}.csv'.format(split_version, vector_version),
                                  dtype={'first': int, 'second': int, 'predResult': int, 'empComb': float, 'empChild': float, 'binComb': float, 'binChild': float})

        return empowerment_info
    except:
        raise ValueError('Corresponding empowerment info not found. Check if input was correct or create the needed info using "empowermentexploration.resources.customgametree"')

def get_player_data(memory = True, group = 'children'):
    """Returns player data for given version. Player data is already cleansed of doubling combinations.

    Args:
        memory (boolean, optional): True if memory version of data is going to be used, False otherwise. Defaults to True.
        group (str, optional): 'children' or 'adults' or 'combined'. States what player data set set is going to be used. Defaults to 'children'.

    Returns:
        DataFrame: Player data.
    """
    if memory is True:
        memory = 'Memory'
    else:
        memory = ''
    if group == 'combined':
        player_data = pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanDataCombined{}.csv'.format(memory))
    else:
        player_data = pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanData{}Complemented{}.csv'.format(group.capitalize(), memory))

    return player_data


def get_simulation_data(model, memory_type):
    """Returns simulation data for given version.

    Args:
        model (str): Model type, which is either 'base', 'emp', 'bin', 'trueemp',
                    'truebin', 'cbv', 'sim' or 'cbu'.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)

    Returns:
        DataFrame: Simulation data.
    """
    try:
        simulation_data = pd.read_csv('empowermentexploration/resources/playerdata/data/reference/childrenalchemy{}Combinations-memory{}.csv'.format(model, memory_type))

        return simulation_data
    except:
        raise ValueError('Corresponding simulation data not found. Check if input was correct.')
