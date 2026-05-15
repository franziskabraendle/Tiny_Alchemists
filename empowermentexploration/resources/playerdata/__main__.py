from empowermentexploration.resources.playerdata.playerdata import PlayerData
from empowermentexploration.resources.playerdata.summary import Summary
from empowermentexploration.resources.playerdata.behavior import Behavior
from empowermentexploration.resources.playerdata.elementcount import Elementcount

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: CHOOSE APPROPRIATE METHOD AND METHOD ARGUMENTS

    # Preprocessing 
    playerdata = PlayerData(group="children", memory=True)
    playerdata.create_csv_file() # Convert the individual raw data json files into an all-encompassing csv file
    playerdata.add_trials() # Add trials to participant overview and save it as a new csv file group separated
    playerdata.transform() # Transform the data into a more readable format
    playerdata.add_parameters() # Add age, group and empowerment values to data files
    playerdata.combine_groups() # Combine the data files of the two groups, note: make sure, you run the previous functions for both groups first


    # Sample summary 
    summary = Summary()
    summary.age_distribution() # Plot age distribution of children

    # Behavior
    behavior = Behavior(memory=True, trials=100, model_type='base', group = "children") # Select 'None' for all trials
    behavior.plot_final_inventory_sizes() # Plots distribution of final inventory sizes
    behavior.plot_final_inventory_sizes_agegroups() # Plots performance of children in terms of the final number of elements in the inventory in age groups
    behavior.plot_final_inventory_sizes_comparison() # Plots comparison of final inventory size children vs. adults
    behavior.plot_inventory_over_time() # Plots average inventory over time
    behavior.plot_trials() # Plots distribution of trials
    behavior.plot_trials_agegroups() # Plots the number of trials the children played the game for in age groups
    behavior.plot_trials_comparison() # Plots comparison of trials children vs. adults
    behavior.plot_success_probability() # Plots probabilty of trying a successful combinations in relation to number of trials/invenotory size
    behavior.plot_average_empowerment() # Plots average empowerment of the first 15 created elements. Note: select group='combined'

    # Elementcount
    elementcount = Elementcount(group='adults', style='Relative', trials = None) # Select 'None' for all trials
    elementcount.count_elements() # Count the elements found by the players
    elementcount.count_combinations() # Count the combinations tried by the players
    elementcount.count_combinations_per_element() # Count the combinations with each element
    elementcount.count_used_elements() # Count the elements that were actually used by the players


    # YOUR ACTION IS NOT RECQUIRED ANYMORE
