import empowermentexploration.utils.data_handle as data_handle
import json
from pickle import FALSE, TRUE
import csv
import os
from csv import writer
from csv import reader
import pandas as pd
import ast

class PlayerData():
    """Class functions generate Children Alchemy playerdata and preparing it for analysis.
    """
    def __init__(self, group="children", memory=True):
        """Initializes playerdata class.
        
        Args:
            group (str): 'children' or 'adults'. States the group of participants from which the data will be used. 
                    Defaults to 'children'.
            memory (bool): True or False. States whether repeated combinations are excluded or not.
                    Defaults to True.

        Note: The ID of adults participants is prefixed with 'A-' and the ID of children participants is prefixed with 'C-'.
        """

        self.group = group
        self.memory = memory

        if self.memory:
            self.suffix = "Memory"
        else:
            self.suffix = ""
  
        # Excluded participants from the analysis (ID-1, since original data start with ID=1):
        self.excluded = ["A-20", "A-21", "C-14", "C-22", "C-46", "C-62", "C-63", "C-64", "C-65", "C-108"]

        # Put in directory of data files
        self.path = 'empowermentexploration/resources/playerdata/data/raw/{}'.format(self.group.capitalize())
        self.directory = os.fsencode(self.path)

        # Print info for user
        print('\nProcess player data from {}.'.format(self.group))
        if self.memory:
            print('\nVersion: Memory (Repeated combinations are excluded).')
        else:
            print('\nVersion: No Memory (Repeated combinations are not excluded).')

    # Converting the individual raw data .json files into an all-encompassing .csv file
    def create_csv_file(self):

        # Categories: Counter, id, trial, first element, second element, resulting element
        header = ["","id","trial","n1","n2","out"]

        # Create csv file
        with open('empowermentexploration/resources/playerdata/data/raw/childrenalchemy{}.csv'.format(self.group.capitalize()), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            # Initialize counter data entries 
            i = 1
            # Starting with first player (id = 1)
            id = 1 

            # Iterate over the data json files of all players by accessing each file out of the directory
            for file in os.listdir(self.directory):
                filename = os.fsdecode(file)
                with open(os.path.join(self.path, filename)) as json_file:
                    player = json.load(json_file)

                # Starting with first trial
                trial = 1 

                # Add data of combinations successively
                for combination in player["collect"]:

                    n1 = combination[0]
                    n2 = combination[1]
                    out = combination[2]
                    data = [i, id, trial, n1, n2, out]

                    writer.writerow(data)

                    # Continue with next trial
                    trial += 1
                    # Count entries
                    i += 1

                # Continue with next player
                id += 1

    # Add number of trials to Data Collection
    # Note: Age was added afterwards via Excel Date Function
    def add_trials(self):

        # Collect Data of trials
        trials = []

        # Iterate over the data json files of all players by accessing each file out of the directory
        for file in os.listdir(self.directory):
            filename = os.fsdecode(file)
            with open(os.path.join(self.path, filename)) as json_file:
                player = json.load(json_file)

                trials.append(len(player["collect"]))

        # Create Data frame of 'trials'
        d = {'trials': trials}
        df = pd.DataFrame(data=d)

        # # Add Dataframe to excel file and save group saparated
        # excel_file_path = 'empowermentexploration/resources/playerdata/data/raw/childrenalchemyDataCollection.xlsx'
        # xls = pd.ExcelFile(excel_file_path)
        # if self.group == "children":
        #     sheet = xls.sheet_names[0]
        # elif self.group == "adults":
        #     sheet = xls.sheet_names[1]
        # file = pd.read_excel(excel_file_path, sheet_name=sheet)
        # # Drop column with mean in it
        # file.drop(file.columns[9], axis=1, inplace=True)
        # file['trials'] = df['trials']
        # file.to_csv('empowermentexploration/resources/playerdata/data/childrenalchemyDataCollection{}Edited.csv'.format(self.group.capitalize()), index=False)

    # Convert the data into a more suitable format for the analysis
    def transform(self):

        # Get gametree
        gametree = data_handle.get_gametree()

        # Set categories: id,trial,inventory,first element,second element,success (0/1), resulting element
        header = ["id","trial","inventory","first","second", "success", "results"]

        # Create csv file
        file = 'empowermentexploration/resources/playerdata/data/childrenalchemyHumanData{}{}'.format(self.group.capitalize(), self.suffix)
 
        with open('{}.csv'.format(file), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            # Starting with first player (id = 0)
            id = 0 

            # Iterate over the data json files of all players by accessing each file out of the directory
            for file in os.listdir(self.directory):
                filename = os.fsdecode(file)
                with open(os.path.join(self.path, filename)) as json_file:
                    player = json.load(json_file)

                # Initializing Inventory (amount of elements)
                inventory = 4

                # Initializing used combinations
                usedCombinations = []

                # Collect Results
                results = []

                # Starting with first trial
                trial = 0 

                alreadyCreated = False

                # Add data of combinations successively
                for combination in player["collect"]:
                
                    first = int([k for k, v in gametree.items() if v["name"] == combination[0]][0])
                    second = int([k for k, v in gametree.items() if v["name"] == combination[1]][0])

                    # If the combination results in a new created element, it is successful
                    if combination[2] != 'none':
                        result = [int([k for k, v in gametree.items() if v["name"] == combination[2]][0])]
                        success = 1
                        if result not in results:
                            inventory += 1
                            results.append(result)
                        else:
                            alreadyCreated = True
                    else:        
                        result = -1
                        success = 0

                    data = [id, trial, inventory, first, second, success, result]

                    if not self.memory:
                        writer.writerow(data)
                        # Continue with next trial
                        trial += 1
                    else: 
                        # If combination was already used, do not write it down again
                        used = False
                        if [first, second] in usedCombinations or [second, first] in usedCombinations:
                            used = True
                        if not used:
                            writer.writerow(data)
                            # Continue with next trial
                            trial += 1
                            # Store chosen elements in used combinations
                            usedCombinations.append([first, second])
                        else: 
                            # Do not write down trial and set inventory back (as it was increased before)
                            if result != -1 and not alreadyCreated:
                                inventory -= 1


                # Continue with next player
                id += 1

    # Add age, group and empowerment to 'HumanData' csv files, as well as a prefix to distinguish between groups
    def add_parameters(self):

        # Read in data
        data_collection= pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyDataCollection{}Edited.csv'.format(self.group.capitalize()))
        human_data = pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanData{}{}.csv'.format(self.group.capitalize(), self.suffix))

        # Read in empowerment values
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyEmpowerment.json') as json_file:
            empowerment = json.load(json_file)

        human_data['id'] = human_data['id'].astype(object)
        # Iterate over Data Collection
        for index, row in data_collection.iterrows():
            # Get age of player
            age = row['age']
            # Get id of player
            id = index
            # Add Prefix to ID to distinguish between groups
            if self.group == "adults":
                prefix = "A-"
            elif self.group == "children":
                prefix = "C-"
            # Iterate over Human Data
            for index, row in human_data.iterrows():
                if row['id'] == id:
                    human_data.at[index, 'id'] = prefix + str(row['id'])
                    # Exclusion of selected participants
                    if row['results'] == "-1":
                        human_data.at[index, 'emp_value'] = 0
                    else:
                        human_data.at[index, 'emp_value'] = empowerment[str(ast.literal_eval(row['results'])[0])]["empowerment"]
                    human_data.at[index, 'group'] = self.group.capitalize()
                    human_data.at[index, 'age'] = age
        # Exclusion of selected participants
        human_data = human_data[~human_data['id'].isin(self.excluded)]

        human_data.to_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanData{}Complemented{}.csv'.format(self.group.capitalize(), self.suffix), index=False)

    # Combine the 'HumanData' csv files of the different groups
    def combine_groups(self):
    
        # Read in data
        data_children = pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanDataChildrenComplemented{}.csv'.format(self.suffix))
        data_adults = pd.read_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanDataAdultsComplemented{}.csv'.format(self.suffix))
        # Combine data
        combined_data = pd.concat([data_children, data_adults], axis=0)
        combined_data.to_csv('empowermentexploration/resources/playerdata/data/childrenalchemyHumanDataCombined{}.csv'.format(self.suffix), index=False)

