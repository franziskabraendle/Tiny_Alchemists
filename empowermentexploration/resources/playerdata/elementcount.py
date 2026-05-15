import pandas as pd
import ast
import json
from pickle import FALSE, TRUE
import matplotlib.pyplot as plt
import csv
import scipy.stats as stats
import empowermentexploration.utils.data_handle as data_handle

class Elementcount():
    """Class functions generate statistical data and plots for the elements found by the players and the combinations of elements."""
   
    # Set number of players
    n_children = 112
    n_adults = 58

    def __init__(self, group='children', style='Absolute', trials = None):
        """Initialize the class with the game version, group and style of values.
        
        Args: 
            game_version (str, optional): "The game version. Defaults to 'childrenalchemy'.
            group (str, optional): "The group of players. Can be 'adults', 'children' or 'both'.
            style (str, optional): "The style of values. Can be 'Absolute' (= Absolute numbers) or 'Relative' (= values in %).
        """
        # print info for user
        print('\nPlot player statistics for group {}.'.format(group))


        # read in data
        if group == "both":
            self.data = data_handle.get_player_data(True, 'combined')
        else:
            self.data = data_handle.get_player_data(True, group)

        # get gametree
        self.gametree = data_handle.get_gametree()

        # set attributes
        self.group = group.capitalize()
        self.style = style
        self.trials = trials

        # select trials
        if self.trials != None:
            # Group the data by 'id'
            df_grouped = self.data.groupby('id').filter(lambda x: len(x) >= 50)
            # Keep only the first 50 trials within each group
            df_grouped = df_grouped.groupby('id').head(50)
            # Reset the index
            self.data = df_grouped.reset_index(drop=True)
            # print info for user
            print('\nConsidering the first {} trials.'.format(self.trials))
        else:
            self.trials = ""
            print('\nConsidering all trials.')
        

    def count_elements(self):
        """Function to count the number of elements found by the players."""

        # get the number of players
        num_unique_ids = self.data['id'].nunique()

        unsuccessful = 0 # number of unsuccessful trials

        # add a new column 'new_id' to mark the rows where a new id starts
        self.data['new_id'] = self.data['id'].ne(self.data['id'].shift()).astype(int)

        # create dictionary 
        found_elements_overview = {}

        ## Create an overview of the elements found by the players and the ratio children:adults
        if self.group == 'Both':

            # iterate through dataframe and add elements to dictionary
            for index, row in self.data.iterrows():
                if row["new_id"] == 1:
                    visited = []
                if row["results"] == "-1":
                    unsuccessful += 1
                    continue
                else:
                    element = self.gametree[ast.literal_eval(row["results"])[0]]["name"]
                    if element not in visited:
                        if element not in found_elements_overview:
                            if row["group"] == "Children":
                                found_elements_overview[element] = {"total": 1, "children": 1, "adults": 0}
                            elif row["group"] == "Adults":
                                found_elements_overview[element] = {"total": 1, "children": 0, "adults": 1}
                        else:
                            found_elements_overview[element]["total"] += 1 
                            if row["group"] == "Children":
                                found_elements_overview[element]["children"] += 1
                            elif row["group"] == "Adults":
                                found_elements_overview[element]["adults"] += 1
                        visited.append(element)

            # sort the dictionary by the absolute value of the difference between children and adults
            sorted_elements = sorted(found_elements_overview.items(), key=lambda x: (x[1]['children']/x[1]['total']*100 - x[1]['adults']/x[1]['total']*100))

            # open a new csv file for writing
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyElementcountOverview{}.csv'.format(self.trials), mode='w', newline='') as csvfile:
            
                # create a csv writer object
                writer = csv.writer(csvfile, delimiter=',')

                # write the header row
                writer.writerow(['element', 'ratio', 'total', 'children', 'adults'])

                # write each row of data
                for element, values in sorted_elements:
                    adults = values['adults']
                    children = values['children']
                    total = values['total']
                    ratio = f"{round(children/total*100)}:{round(adults/total*100)}"
                    writer.writerow([element, ratio, total, children, adults])


        ## Collect the elements found by the players
        
        # create dictionary 
        found_elements = {}

        # iterate through dataframe and add elements to dictionary
        for index, row in self.data.iterrows():
            if row["new_id"] == 1:
                visited = []
            if row["results"] == "-1":
                unsuccessful += 1
                continue
            else:
                element = self.gametree[ast.literal_eval(row["results"])[0]]["name"]
                if element not in visited:
                    if element not in found_elements:
                        found_elements[element] = 1
                    else:
                        found_elements[element] += 1 
                    visited.append(element)

        # Convert dictionary to JSON file
        if self.style == "Absolute":
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyElementcount{}Absolute{}.json'.format(self.group, self.trials), 'w') as filehandle:
                json.dump(found_elements, filehandle, indent=4)
        
        # sort dictionary
        sorted_found_elements = sorted(found_elements.keys())

        ## Overlap of elements
        if self.group == "Both":
            elements_children = []
            elements_adults = []
            for index, row in self.data.iterrows():
                if row["results"] == "-1":
                    continue
                else:
                    element = self.gametree[ast.literal_eval(row["results"])[0]]["name"]
                    if row["group"] == "Children" and element not in elements_children:
                        elements_children.append(element)
                    elif row["group"] == "Adults" and element not in elements_adults:
                        elements_adults.append(element)
            intersection = set(elements_children).intersection(elements_adults)
            difference_children = set(elements_children).difference(elements_adults)
            difference_adults = set(elements_adults).difference(elements_children)

        ### Print messages
        print("In total,", len(self.gametree), "elements could have been found.")
        if self.style == "Absolute":
            print(num_unique_ids, self.group, "played the game for a total of", len(self.data), "trials, of which", len(self.data)-unsuccessful, "were successful.")
            print(len(found_elements), "different elements were found.")
            if self.group == "Both":
                print("The overlap of elements found by children and adults is", len(intersection))
                print(len(difference_children), "elements were only found by children.")
                print(len(difference_adults), "elements were only found by adults:")
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)
        elif self.style == "Relative":
            print(num_unique_ids, self.group, "played the game for a total of", len(self.data), "trials, of which", round((len(self.data)-unsuccessful)/len(self.data)*100, 1), "% were successful.")
            print(len(found_elements), "different elements were found, which is", round(len(found_elements)/len(self.gametree)*100, 1), "% of all elements that could have been found.")
            if self.group == "Both":
                print("The overlap of elements found by children and adults is", round(len(intersection)/len(found_elements)*100, 1), "%.")
                print("That is", round(len(intersection)/len(self.gametree)*100, 1), "% of all elements that could have been found.")
                print(round(len(difference_children)/len(found_elements)*100, 1), "% of the found elements were only found by children.")
                print("That is", round(len(difference_children)/len(self.gametree)*100, 1), "% of all elements that could have been found.")
                print(round(len(difference_adults)/len(found_elements)*100, 1), "% of the found elements only found by adults.")
                print("That is", round(len(difference_adults)/len(self.gametree)*100, 1), "% of all elements that could have been found.")
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)

        ### Create a list of lists to represent the table
        if self.style == "Absolute":
            table = [['Element', 'Amount of Players']]
            for key in sorted_found_elements:
                table.append([key, found_elements[key]])
        elif self.style == "Relative":
            table = [['Element', 'Percentage of Players']]
            for key in sorted_found_elements:
                table.append([key, round(found_elements[key]/num_unique_ids*100, 1)])

        # write the table to a CSV file
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyElementcount{}{}{}.csv'.format(self.group, self.style, self.trials), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(table)
        

        ### Create a Histogram 

        # only show elements that were found more than once
        found_elements_filtered = {k: v for k, v in found_elements.items() if v > num_unique_ids/3}

        # create a list of keys and a list of values from the dictionary
        keys = sorted(found_elements_filtered.keys())
        values = [found_elements_filtered[key] for key in keys]
        if self.style == "Relative":
            values = [round(value/num_unique_ids*100, 1) for value in values]

        # create a histogram using matplotlib
        if self.group == "Adults":
            plt.bar(keys, values, color="#e1812c")
        if self.group == "Children":
            plt.bar(keys, values, color="#3274a1")
        if self.group == "Both":
            plt.bar(keys, values, color="#228B22")

        # set the title and axis labels
        plt.title('Found Elements {}' .format(self.group), fontsize = 16)
        plt.xlabel('Element', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        if self.style == "Absolute":
            plt.ylabel('Amount of Players', fontsize=14)
        elif self.style == "Relative":
            plt.ylabel('Amount of Players (%)', fontsize=14)
        plt.tight_layout()

        # save the plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFoundElements{}{}{}.png'.format(self.group, self.style, self.trials))

    def count_combinations(self):
        """Function to count the combinations tried by the players."""

        # get the number of players
        num_unique_ids = self.data['id'].nunique()
        unsuccessful = 0 # number of unsuccessful combinations

        # create dictionary 
        tried_combinations = {}

        # Add a new column 'new_id' to mark the rows where a new id starts
        self.data['new_id'] = self.data['id'].ne(self.data['id'].shift()).astype(int)

        ## Create an overview of the combinations tried by the players, the ratio children:adults and success
        if self.group == 'Both': 
            tried_combinations_both = {}
            # iterate through dataframe and add elements to dictionary
            for index, row in self.data.iterrows():
                if row["new_id"] == 1:
                    visited = []
                first_element = self.gametree[row["first"]]["name"]
                second_element = self.gametree[row["second"]]["name"]
                combination = (first_element, second_element)
                combination_reversed = (second_element, first_element)
                if combination not in visited and combination_reversed not in visited:
                    if combination not in tried_combinations and combination_reversed not in tried_combinations:
                        if row["group"] == "Children":
                            tried_combinations_both[combination] = {"total used": 1, "children used": 1, "adults used": 0, "total found": 0, "children found": 0, "adults found": 0, "success": False}
                        if row["group"] == "Adults":
                            tried_combinations_both[combination] = {"total used": 1, "children used": 0, "adults used": 1, "total found": 0, "children found": 0, "adults found": 0, "success": False}
                        if row["success"] == 1:
                            tried_combinations_both[combination]["success"] = True
                    elif combination in tried_combinations_both:
                        tried_combinations_both[combination]["total used"] += 1
                        if row["group"] == "Children":
                            tried_combinations_both[combination]["children used"] += 1
                        elif row["group"] == "Adults":
                            tried_combinations_both[combination]["adults used"] += 1
                    elif combination_reversed in tried_combinations_both:
                        tried_combinations_both[combination_reversed]["total used"] += 1
                        if row["group"] == "Children":
                            tried_combinations_both[combination_reversed]["children used"] += 1
                        elif row["group"] == "Adults":
                            tried_combinations_both[combination_reversed]["adults used"] += 1
                    visited.append(combination)
   
            
            # Collect the inventory of each player
            inventories = {}
            # iterate through dataframe and add elements to dictionary
            for index, row in self.data.iterrows():
                if row["new_id"] == 1:
                    inventories[row["id"]] = {"group": row["group"], "inventory": ["water", "fire", "earth", "air"]}
                if row["results"] != "-1":
                    result_element = self.gametree[ast.literal_eval(row["results"])[0]]["name"]
                    inventories[row["id"]]["inventory"].append(result_element)

            ## Check who could have tried the combinations
            for combination, values1 in tried_combinations_both.items():
                for player, values2 in inventories.items():
                    if combination[0] in values2["inventory"] and combination[1] in values2["inventory"]:
                        tried_combinations_both[combination]["total found"] += 1
                        if values2["group"] == "Children":
                            tried_combinations_both[combination]["children found"] += 1
                        elif values2["group"] == "Adults":
                            tried_combinations_both[combination]["adults found"] += 1

            # open a new csv file for writing
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyCombinationcountOverview{}.csv'.format(self.trials), mode='w', newline='') as csvfile:
            
                # create a csv writer object
                writer = csv.writer(csvfile, delimiter=',')

                # write the header row
                writer.writerow(['Combination', '# Total used', '# Children used', '# Adults used', '# Total found', '# Children found', '# Adults found', 'Total used (%)', 'Children used (%)', 'Adults used (%)', "Difference", "Ratio Children:Adults used(%)", "Fisher's Exact Test", "p-Value", 'Success'])

                # write each row of data
                for combination, values in tried_combinations_both.items():
                    name = combination[0] + " + " + combination[1]
                    total_used = values['total used']
                    children_used = values['children used']
                    adults_used = values['adults used']
                    total_found = values['total found']
                    children_found = values['children found']
                    adults_found = values['adults found']
                    if total_found == 0:
                        total_ratio = 0
                    else:
                        total_ratio = round(total_used/total_found*100)
                    if children_found == 0:
                        children_ratio = 0
                    else:
                        children_ratio = round(children_used/children_found*100)
                    if adults_found == 0:
                        adults_ratio = 0
                    else:
                        adults_ratio = round(adults_used/adults_found*100)
                    contingency_table = [[children_used, adults_used], [children_found-children_used, adults_found-adults_used]]
                    oddsratio, pvalue = stats.fisher_exact(contingency_table)
                    difference = abs(round(children_ratio - adults_ratio))
                    success = values['success']
                    ratio = f"{round(children_used/total_used*100)}:{round(adults_used/total_used*100)}"
                    writer.writerow([name, total_used, children_used, adults_used, total_found, children_found, adults_found, total_ratio, children_ratio, adults_ratio, difference, ratio, round(oddsratio, 2), round(pvalue,2), success])
       

        ## Collect combinations tried by children or adults              
        # iterate through dataframe and add elements to dictionary
        for index, row in self.data.iterrows():
            if row["new_id"] == 1:
                visited = []
            first_element = self.gametree[row["first"]]["name"]
            second_element = self.gametree[row["second"]]["name"]
            combination = first_element + " + " + second_element
            combination_reversed = second_element + " + " + first_element
            if combination not in visited and combination_reversed not in visited:
                if combination not in tried_combinations and combination_reversed not in tried_combinations:
                    tried_combinations[combination] = 1
                    if row["success"] == 0:
                        unsuccessful += 1
                elif combination in tried_combinations:
                    tried_combinations[combination] += 1
                elif combination_reversed in tried_combinations:
                    tried_combinations[combination_reversed] += 1
                visited.append(combination)
        sorted_tried_combinations = sorted(tried_combinations.keys())

        ### Overlap of combinations found by children and adults
        if self.group == "Both":
            combinations_children = []
            combinations_adults = []
            for index, row in self.data.iterrows():
                first_element = self.gametree[row["first"]]["name"]
                second_element = self.gametree[row["second"]]["name"]
                combination = [first_element, second_element]
                reversed_combination = [second_element, first_element]
                if row["group"] == "Children" and combination not in combinations_children and reversed_combination not in combinations_children:
                    combinations_children.append(combination)
                elif row["group"] == "Adults" and combination not in combinations_adults and reversed_combination not in combinations_adults:
                    combinations_adults.append(combination)
            difference_children = []
            difference_adults = []
            intersection = []
            for combination in combinations_children:
                first, second = combination
                if combination not in combinations_adults and [second, first] not in combinations_adults:
                    difference_children.append(combination)
                elif combination not in intersection and [second, first] not in intersection:
                    intersection.append(combination)
            for combination in combinations_adults:
                first, second = combination
                if combination not in combinations_children and [second, first] not in combinations_children:
                    difference_adults.append(combination)
                elif combination not in intersection and [second, first] not in intersection:
                    intersection.append(combination)
            
            # Successful combinations in the intersection
            successful_intersection = []
            for combination in intersection:
                first = int({i for i in self.gametree if self.gametree[i]['name'] == combination[0]}.pop())
                second = int({i for i in self.gametree if self.gametree[i]['name'] == combination[1]}.pop())
                for index, row in self.data.iterrows():
                    if (row["first"] == first and row["second"] == second) or (row["first"] == second and row["second"] == first):
                        if row["success"] == 1:
                            successful_intersection.append(combination)
                        break
            # write the successful combinations to a CSV file
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyCombinationcountSuccessfulOverlap{}{}.csv'.format(self.groupself.trials), mode='w', newline='') as file:
                writer = csv.writer(file)
                for combination in successful_intersection:
                    # Convert set to list to be written in CSV
                    combination_list = list(combination)
                    writer.writerow(combination_list)

            # write the overlap  to a CSV file
            overlap = [['Intersection', 'Difference Children', 'Difference Adults']]
            for item1, item2, item3 in zip(intersection, difference_children, difference_adults):
                overlap.append([item1, item2, item3])
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyCombinationcountOverlap{}.csv'.format(self.trials), mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(overlap)
                
        ### Print messages
        if self.style == "Absolute":
            print(num_unique_ids, self.group, "tried a total of", len(tried_combinations), "different combinations.")
            print(len(tried_combinations)-unsuccessful, "combinations were successful.")
            if self.group == "Both":
                print("The overlap of combinations tried by children and adults is", len(intersection))
                print(len(successful_intersection), "combinations were successful in the overalp.")
                print(len(difference_children), "combinations were only tried by children.")
                print(len(difference_adults), "combinations were only tried by adults.")
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)
        elif self.style == "Relative":
            print(num_unique_ids, self.group, "tried a total of", len(tried_combinations), "different combinations.")
            print(round((len(tried_combinations)-unsuccessful)/len(tried_combinations)*100, 1), "% of all tried combinations were successful.")
            if self.group == "Both":
                print("The overlap of combinations tried by children and adults is", round(len(intersection)/len(tried_combinations)*100, 1), "%.")
                print(round(len(difference_children)/len(tried_combinations)*100, 1), "% of the tried combinations were tried by children.")
                print(round(len(difference_adults)/len(tried_combinations)*100, 1), "% of the tried combinations were tried by adults.") 
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)

        ### Create a list of lists to represent the table
        if self.style == "Absolute":
            table = [['Combinations', 'Amount of Players']]
            for key in sorted_tried_combinations:
                table.append([key, tried_combinations[key]])
        elif self.style == "Relative":
            table = [['Combinations', 'Percentage of Players']]
            for key in sorted_tried_combinations:
                table.append([key, round(tried_combinations[key]/num_unique_ids*100, 1)])

        # write the table to a CSV file
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyCombinationcount{}{}{}.csv'.format(self.group, self.style, self.trials), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(table)

        ### Create a Histogram 
        # only show elements that were found more than once
        tried_combinations_filtered = {k: v for k, v in tried_combinations.items() if v > num_unique_ids/3}
        # create a list of keys and a list of values from the dictionary
        keys = sorted(tried_combinations_filtered.keys())
        values = [tried_combinations_filtered[key] for key in keys]
        if self.style == "Relative":
            values = [round(value/num_unique_ids*100, 1) for value in values]
        # create a histogram using matplotlib
        if self.group == "Adults":
            plt.bar(keys, values, color="#e1812c")
        if self.group == "Children":
            plt.bar(keys, values, color="#3274a1")
        if self.group == "Both":
            plt.bar(keys, values, color="#228B22")
        # set the title and axis labels
        plt.title('Tried Combinations {}' .format(self.group), fontsize = 16)
        plt.xlabel('Combinations', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        if self.style == "Absolute":
            plt.ylabel('Amount of Players', fontsize=14)
        elif self.style == "Relative":
            plt.ylabel('Amount of Players (%)', fontsize=14)
        plt.tight_layout()
        # save the plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTriedCombinations{}{}{}.png'.format(self.group, self.style, self.trials))

    def count_combinations_per_element(self):
        """Function to count the combinations with each element."""
        
        # get the number of players
        num_unique_ids = self.data['id'].nunique()

        unsuccessful = 0 # number of unsuccessful combinations

        # create dictionary 
        combinations_per_element = {}

        # iterate through dataframe and add elements to dictionary
        visited = []
        for index, row in self.data.iterrows():
            first_element = self.gametree[row["first"]]["name"]
            second_element = self.gametree[row["second"]]["name"]
            combination = {first_element, second_element}
            if combination not in visited:
                if row["results"] == "-1":
                    unsuccessful += 1
                if first_element not in combinations_per_element:
                    combinations_per_element[first_element] = 1
                else:
                    combinations_per_element[first_element] += 1
                if second_element != first_element:
                    if second_element not in combinations_per_element:
                        combinations_per_element[second_element] = 1
                    else:
                        combinations_per_element[second_element] += 1
                visited.append(combination)
        sorted_combinations_per_element = sorted(combinations_per_element.keys())

        # Save used elements to a CSV file
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyUsedElements{}{}.csv'.format(self.group, self.trials), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(sorted_combinations_per_element)
        
        # Overlap
        if self.group == "Both":
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyUsedElementsChildren{}.csv'.format(self.trials)) as file:
                reader = csv.reader(file)
                children = list(reader)[0]
            with open('empowermentexploration/resources/playerdata/data/childrenalchemyUsedElementsAdults{}.csv'.format(self.trials)) as file:
                reader = csv.reader(file)
                adults = list(reader)[0]

            intersection = set(children).intersection(adults)
            difference_children = set(children).difference(adults)
            difference_adults = set(adults).difference(children)

        # check which elements were not used
        not_used_elements = []
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyElementcount{}Absolute{}.json'.format(self.group, self.trials)) as json_file:
            inventory = json.load(json_file)

        # Add base elements
        inventory["water"] = 1
        inventory["fire"] = 1
        inventory["earth"] = 1
        inventory["air"] = 1
        for key in inventory.keys():
            if key not in sorted_combinations_per_element:
                not_used_elements.append(key)
        for key in sorted_combinations_per_element:
            if key not in inventory.keys():
                print(key)
 
    

        ### Print messages
        if self.style == "Absolute":
            print(num_unique_ids, self.group, "tried out", len(visited), "different combinations of which", len(visited)-unsuccessful, "were successful.")
            print(len(sorted_combinations_per_element), "different elements were used for those combinations.")
            print(len(not_used_elements), "of the base elements/found elements were not used at all.")
            print("The following elements were not used:", not_used_elements)
            if self.group == "Both":
                print("The overlap of elements used by children and adults is", len(intersection))
                print(len(difference_children), "elements were only used by children.")
                print(len(difference_adults), "elements were only used by adults:")
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)
        elif self.style == "Relative":
            print(num_unique_ids, self.group, "tried out", len(visited), "different combinations of which", round((len(visited)-unsuccessful)/len(visited)*100, 1), "% were successful.")
            print(len(sorted_combinations_per_element), "different elements were used for those combinations, which is", round(len(sorted_combinations_per_element)/len(inventory)*100, 1), "% of all elements that could have been used.")
            if self.group == "Both":
                print("The overlap of elements used by children and adults is", round(len(intersection)/len(combinations_per_element)*100, 1), "%.")
                print(round(len(difference_children)/len(combinations_per_element)*100, 1), "% of the used elements were only used by children.")
                print(round(len(difference_adults)/len(combinations_per_element)*100, 1), "% of the used elements only used by adults.")
                print("Intersection:", intersection)
                print("Difference Children:", difference_children)
                print("Difference Adults:", difference_adults)


        ### Create a list of lists to represent the table
        if self.style == "Absolute":
            table = [['Element', 'Amount of Combinations']]
            for key in sorted_combinations_per_element:
                table.append([key, combinations_per_element[key]])
        elif self.style == "Relative":
            table = [['Element', 'Percentage of Combinations']]
            for key in sorted_combinations_per_element:
                table.append([key, round(combinations_per_element[key]/len(sorted_combinations_per_element)*100, 1)])

        # write the table to a CSV file
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyCombinationsPerElementCount{}{}{}.csv'.format(self.group, self.style, self.trials), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(table)

        ### Create a Histogram 

        # only show elements that were found more than once
        combinations_per_element_filtered = {k: v for k, v in combinations_per_element.items() if v > 30}

        # create a list of keys and a list of values from the dictionary
        keys = sorted(combinations_per_element_filtered.keys())
        values = [combinations_per_element_filtered[key] for key in keys]
        if self.style == "Relative":
           values = [round(value/len(visited)*100, 1) for value in values]

        # create a histogram using matplotlib
        if self.group == "Adults":
            plt.bar(keys, values, color="#e1812c")
        if self.group == "Children":
            plt.bar(keys, values, color="#3274a1")
        if self.group == "Both":
            plt.bar(keys, values, color="#228B22")

        # set the title and axis labels
        plt.title('Combinations per Element {}' .format(self.group), fontsize = 16)
        plt.xlabel('Combinations', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        if self.style == "Absolute":
            plt.ylabel('Number of Combinations', fontsize=14)
        elif self.style == "Relative":
            plt.ylabel('Number of Combinations (%)', fontsize=14)
        plt.tight_layout()

        # save the plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyCombinationsPerElement{}{}{}.png'.format(self.group, self.style, self.trials))

    def count_used_elements(self):
        """Function to count the elements that were actually used by the players."""
        
        # get the number of players
        num_unique_ids = self.data['id'].nunique()

        # create dictionary 
        used_elements = {}

        # Add base elements
        base_elements = ["water", "fire", "earth", "air"]
        for element in base_elements:
            used_elements[element] = {"found total": Elementcount.n_adults + Elementcount.n_children, "found children": Elementcount.n_children, "found adults": Elementcount.n_adults, "used total": 0, "used children": 0, "used adults": 0,  '# uses total': 0, "# uses children": 0, "# uses adults": 0}

        # Add a new column 'new_id' to mark the rows where a new id starts
        self.data['new_id'] = self.data['id'].ne(self.data['id'].shift()).astype(int)

        # Iterate through dataframe and add elements to dictionary
        for index, row in self.data.iterrows():
            if row["new_id"] == 1:
                visited_results = base_elements.copy()
                visited_uses = []
            first_element = self.gametree[row["first"]]["name"]
            second_element = self.gametree[row["second"]]["name"]
            elements = [first_element, second_element]
            for element in elements:
                if element not in visited_uses:
                    if first_element not in used_elements:
                        if row["group"] == "Children":
                            used_elements[element] = {"found total": 0, "found children": 0, "found adults": 0, "used total": 1, "used children": 1, "used adults": 0, '# uses total': 1, "# uses children": 1, "# uses adults": 0}
                        elif row["group"] == "Adults":
                            used_elements[element] = {"found total": 0, "found children": 0, "found adults": 0, "used total": 1, "used children": 0, "used adults": 1, '# uses total': 1, "# uses children": 0, "# uses adults": 1}
                    else:
                        used_elements[element]["used total"] += 1
                        used_elements[element]["# uses total"] += 1
                        if row["group"] == "Children":
                            used_elements[element]["used children"] += 1
                            used_elements[element]["# uses children"] += 1
                        elif row["group"] == "Adults":
                            used_elements[element]["used adults"] += 1
                            used_elements[element]["# uses adults"] += 1
                else: 
                    used_elements[element]["# uses total"] += 1
                    if row["group"] == "Children":
                        used_elements[element]["# uses children"] += 1
                    elif row["group"] == "Adults":
                        used_elements[element]["# uses adults"] += 1
                visited_uses.append(element)
            if row["results"] != "-1":
                result_element = self.gametree[ast.literal_eval(row["results"])[0]]["name"]
                if result_element not in visited_results:
                    if result_element not in used_elements:
                        if row["group"] == "Children":
                            used_elements[result_element] = {"found total": 1, "found children": 1, "found adults": 0, "used total": 0, "used children": 0, "used adults": 0, '# uses total': 0, "# uses children": 0, "# uses adults": 0}
                        elif row["group"] == "Adults":
                            used_elements[result_element] = {"found total": 1, "found children": 0, "found adults": 1, "used total": 0, "used children": 0, "used adults": 0,  '# uses total': 0, "# uses children": 0, "# uses adults": 0}
                    else:
                        used_elements[result_element]["found total"] += 1
                        if row["group"] == "Children":
                            used_elements[result_element]["found children"] += 1
                        elif row["group"] == "Adults":
                            used_elements[result_element]["found adults"] += 1
                    visited_results.append(result_element)

        # open a new csv file for writing
        with open('empowermentexploration/resources/playerdata/data/childrenalchemyUsedelementcountOverview{}.csv'.format(self.trials), mode='w', newline='') as csvfile:
        
            # create a csv writer object
            writer = csv.writer(csvfile, delimiter=',')
            # write the header row
            writer.writerow(['Element', '# Total used', '# Children used', '# Adults used', '# Total found', '# Children found', '# Adults found', 'Total used (%)', 'Children used (%)', 'Adults used (%)', 'Difference of ratios', 'Ratio Children:Adults used (%)', "Fisher's Exact Test", "p-Value", "# Uses total", "# Uses children", "# Uses adults", "Average uses total", "Average uses children", "Average uses adults", "Difference of ratios", "T-test", "p-Value"])

            # write each row of data
            for element, values in used_elements.items():
                name = element
                used_total = values['used total']
                used_children = values['used children']
                used_adults = values['used adults']
                found_total = values['found total']
                found_children = values['found children']
                found_adults = values['found adults']
                uses_total = values["# uses total"]
                uses_children = values["# uses children"]
                uses_adults = values["# uses adults"]
                if found_total == 0:
                    used_found_total = 0
                    uses_found_total = 0
                else:
                    used_found_total = round(used_total/found_total*100)
                    uses_found_total = round(uses_total/found_total)
                if found_children == 0:
                    used_found_children = 0
                    uses_found_children = 0
                else:
                    used_found_children = round(used_children/found_children*100)
                    uses_found_children = round(uses_children/found_children)
                if found_adults == 0:
                    used_found_adults = 0
                    uses_found_adults = 0
                else:
                    used_found_adults = round(used_adults/found_adults*100)
                    uses_found_adults = round(uses_adults/found_adults)
                difference_ratios = abs(round(used_found_children - used_found_adults,2))
                if used_total == 0:
                    ratio = "0:0"
                else:
                    ratio = f"{round(used_children/used_total*100)}:{round(used_adults/used_total*100)}"
                contingency_table = [[used_children, used_adults], [found_children-used_children, found_adults-used_adults]]
                oddsratio, pvalue = stats.fisher_exact(contingency_table)
                t_statistic, p_value = stats.ttest_ind([uses_found_children]*found_children, [uses_found_adults]*found_adults, equal_var=False) 
                writer.writerow([name, used_total, used_children, used_adults, found_total, found_children, found_adults, used_found_total, used_found_children, used_found_adults, difference_ratios, ratio, round(oddsratio,2), round(pvalue,2), uses_total, uses_children, uses_adults, uses_found_total, uses_found_children, uses_found_adults, abs(round(uses_found_children - uses_found_adults,2)), round(t_statistic,2), round(p_value,2)])




