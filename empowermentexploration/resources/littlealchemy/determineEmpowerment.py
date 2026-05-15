import empowermentexploration.utils.data_handle as data_handle
import json
from pickle import FALSE, TRUE
import csv

class Empowerment():
    """Class function determines the empowerment value of each element. 
    (empowerment = amount of elements that are directly created by the respective element)
    """

    def __init__(self):

        # print user info
        print('\nDetermine empowerment values for all elements in childrenalchemy.')

        # get gametree
        gametree = data_handle.get_gametree()

        # Create dictionary 
        emp_values = {}
        # Determine empowerment value for each element
        for emp_element in gametree: 
            emp_value = 0
            # Iterate over each element and check, whether it is directly created by the current element
            for element in gametree: 
                combinations = gametree[element]["parents"]
                i = 0
                while i < len(combinations):
                    if int(emp_element) in combinations[i]:
                        emp_value += 1
                        break
                    else:
                        i += 1
            # Add element and its empowerment value to dictionary
            emp_values.update({emp_element: {"name": gametree[emp_element]["name"], "empowerment": emp_value}})
    
    
        # Convert dictionary to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyEmpowerment.json', 'w') as filehandle:
            json.dump(emp_values, filehandle, indent=4)
    
        # Create csv file
        csv_columns = ["element", "name", "empowerment"]
    
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyEmpowerment.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = csv_columns)
            writer.writeheader()
            for key, val in emp_values.items():
                row = {"element": key}
                row.update(val)
                writer.writerow(row)
    