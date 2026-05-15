import json
import time as ti
import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

mpl.use('Agg')

class Behavior():
    """Class functions generate behavioral plots for playerdata.
    """
    def __init__(self, memory=True, trials=100, model_type='base', group = 'children'):
        """Initializes playerdata tiny class.

        Args:
            memory (boolean, optional): True if memory version of data is going to be used, False otherwise.
                        Defaults to True.
            trials (int, optional): Number of trials that will be plotted. Defaults to 100.
            model_type (str, optional): Model type, which is either 'base', 'emp', 'bin', 'trueemp',
                        'truebin', 'cbv', 'sim' or 'cbu' and is going to be used as a second data set. Defaults to 'base'.
            group (str, optional): Group of participants, either 'adults' or 'children', or 'combined' for both children and adults.
        """
        # Print info for user
        print('\nPlot player data statistics.')

        # Set attributes
        self.memory = ''
        if memory is True:
            self.memory = 'Memory'
        self.trials = trials
        self.model_type = model_type
        if group == 'combined':
            self.group = 'All'
        else:
            self.group = group.capitalize()

        # Get number of elements
        self.n_elements = 540

        # Read in data
        self.data = data_handle.get_player_data(memory, group)
        self.grouped_data = self.data.groupby('id')
        self.n_players = self.grouped_data.ngroups

        # Set general settings for plotting
        sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth':0.6, 'grid.color': '#9d9d9d',
                                                                                      'axes.linewidth': 0.6, 'axes.edgecolor': '#9d9d9d'})

    def plot_final_inventory_sizes(self):
        """ Plots distribution of final inventory sizes.
        """
        # Print info
        print('\nPlot inventory sizes of {}.'.format(self.group))

        # Set figure size
        plt.figure(figsize=(5,4))

        # Get inventory sizes
        inventory_sizes = self.grouped_data['inventory'].max()

        # Plot data as histogram (density)
        ax = sns.histplot(data=inventory_sizes, kde=False, log_scale=True, bins=10, color='#82cafc')
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        plt.minorticks_off()

        # Plot mean
        ax.axvline(inventory_sizes.mean(), ls='dashed', color='#444444', linewidth=1)
        print('Maximum inventory size: {}'.format(inventory_sizes.max()))
        print('Minimum inventory size: {}'.format(inventory_sizes.min()))
        print('Mean inventory size: {}'.format(inventory_sizes.mean()))
        print('Confidence Intervals: {}'.format(sm.stats.DescrStatsW(inventory_sizes).tconfint_mean(alpha = 0.05)))


        # Set titles, labels
        plt.ylim(bottom=0, top=25)
        plt.xlim(left=8, right=330)
        plt.xlabel('Final inventory')
        plt.ylabel('Count')

        # Add label for mean
        # _, max_ylim = plt.ylim()
        # plt.text(inventory_sizes.mean()*1.3, max_ylim*0.85, 'Mean:\n{:.1f}'.format(inventory_sizes.mean()))
        plt.tight_layout()

        # Save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalInventorySizes{}{}.pdf'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalInventorySizes{}{}.png'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalInventorySizes{}{}.svg'.format(self.memory, self.group))
        plt.close()

    def plot_final_inventory_sizes_agegroups(self):
        """ Plots performance of children in terms of the final number of elements in the inventory in age groups.
        """

        # Print info for user
        print('\nPlot final inventory size of children in age groups.')

        # Get children data
        self.data_children = data_handle.get_player_data(memory=True, group='children')

        ## Descriptive analysis of children in age groups

        # Preparing data
        idx = self.data_children.groupby('id')['inventory'].idxmax()
        result_children = self.data_children.loc[idx]

        # Define the age groups
        bins = [5, 6, 7, 8, 9, 10, 13]
        labels = ['5-6', '7', '8', '9', '10', '11-13']

        # Group the data by age group and calculate the average inventory value
        result_children['age_group'] = pd.cut(result_children['age'], bins=bins, labels=labels)
        grouped_data = result_children.groupby('age_group')['inventory'].mean().reset_index()

        # n
        group_len = result_children.groupby('age_group')["inventory"].size()
        agg_groups = pd.DataFrame({'n' : group_len})

        # mean
        agg_groups["mean"] = result_children.groupby('age_group')["inventory"].mean()

        # standard deviation
        agg_groups["std"] = result_children.groupby('age_group')["inventory"].std()

        # SEM
        agg_groups["sem"] = agg_groups["std"]/np.sqrt(agg_groups["n"])

        # 95% CI 
        agg_groups["under"] = agg_groups["mean"]- 1.96*agg_groups["sem"]
        agg_groups["upper"] = agg_groups["mean"]+ 1.96*agg_groups["sem"]
        agg_groups['95% CI'] = agg_groups[['under', 'upper']].apply(tuple, axis=1)
        agg_groups.drop(columns=["under","upper"], inplace=True)
        
        print("\nDescriptive analysis of children's performance in age groups:\n{}".format(agg_groups))

        ## Point plot

        # Setting style
        sns.set_style("whitegrid")
        plt.rcParams["axes.edgecolor"] = "0.15"
        plt.rcParams["axes.linewidth"] = 1.25

        plt.figure(figsize=(8, 6))
        sns.pointplot(data=result_children, x= "age_group", y="inventory",  color='#E1812C', errorbar=None)

        # Add 95% CIs
        i = 0
        for row in agg_groups.index:
            plt.errorbar(i, agg_groups["mean"][row], yerr=1.96*agg_groups['sem'][row], c='#E1812C', lw= 3, capsize = 10, capthick=3)
            i += 1

        # Setting Axes
        plt.title('Final Inventory Children', fontsize = 18)
        plt.xlabel('Age group [years]', fontsize = 14)
        plt.ylabel('Final inventory size', fontsize = 14)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryChildrenAgegroups{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryChildrenAgegroups{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryChildrenAgegroups{}.svg'.format(self.memory))

    def plot_final_inventory_sizes_comparison(self):
        """ Plots comparison of final inventory size children vs. adults.
        """

        # Print info for user
        print('\nPlot comparison of final inventory size children vs. adults.')

        # Preparing data
        self.data = data_handle.get_player_data(memory=True, group='combined')
        idx = self.data.groupby('id')['inventory'].idxmax()
        result = self.data.loc[idx]

        print('\nComparison children and adults:\n{}'.format(result.groupby('group')["inventory"].describe()))

        ## Box Plot
        
        # Setting style
        sns.set_style("whitegrid")
        plt.rcParams["axes.edgecolor"] = "0.15"
        plt.rcParams["axes.linewidth"] = 1.25

        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.data, x='group', y='inventory', showmeans=True, meanprops = {"marker" :"x"})

        # Setting Axes
        plt.ylabel('Final inventory size', fontsize = 16)
        plt.xlabel('', fontdict={'fontsize': 16})
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryComparison{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryComparison{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyFinalInventoryComparison{}.svg'.format(self.memory))
    
    def plot_inventory_over_time(self):
        """ Plots average inventory over time.
        """
        # Print info
        print('\nPlot game progress for {}.'.format(self.group))

        # Set figure size
        plt.figure(figsize=(12,5))

        # Get average inventory over time, means and stds or sems
        trial_sizes = self.grouped_data['trial'].max()
        steps = range(0,trial_sizes.to_numpy().max()+1)

        # Get human average inventory over time
        inventory_over_time_mean = self.data.groupby('trial')['inventory'].mean()
        inventory_over_time_sem = self.data.groupby('trial')['inventory'].sem()

        # Plot line
        plt.plot(inventory_over_time_mean, color='#82cafc')

        # Set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=trial_sizes.max())
        plt.ylim(bottom=0)
        plt.title('Game progress averaged over {} players'.format(self.n_players), loc='center', wrap=True)
        plt.tight_layout()

        # Save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}.pdf'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}.png'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}.svg'.format(self.memory, self.group))
        plt.close()

        # Set figure size
        plt.figure(figsize=(6,5))

        # Get average inventory over time, means and stds or sems
        steps = range(0, self.trials)

        # Get player subset
        trial_sizes = trial_sizes.loc[trial_sizes > self.trials-2]
        idx = trial_sizes.index
        player_subset = self.data.query('id in @idx & trial < @self.trials')

        # Get human average inventory over time
        inventory_over_time_mean = player_subset.groupby('trial')['inventory'].mean()
        inventory_over_time_sem = player_subset.groupby('trial')['inventory'].sem()

        # Plot line
        plt.plot(inventory_over_time_mean, color='#82cafc')

        # Plot std
        plt.fill_between(steps, inventory_over_time_mean - inventory_over_time_sem,
                         inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color='#cfeafe')

        # Set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=self.trials+1)
        # TODO: adjust top accordingly to datasets
        plt.ylim(bottom=0, top=55)
        plt.title('Game progress averaged over {} players'.format(len(trial_sizes.index)), loc='center', wrap=True)
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}{}.pdf'.format(self.memory, self.trials, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}{}.png'.format(self.memory, self.trials, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanAverageGameProgress{}{}{}.svg'.format(self.memory, self.trials, self.group))
        plt.close()

    def plot_trials(self):
        """ Plots distribution of trials.
        """
        # Print info
        print('\nPlot trial numbers of {}.'.format(self.group))

        # Set figure size
        plt.figure(figsize=(5,4))

        # Get trial sizes
        trial_sizes = self.grouped_data['trial'].max().to_numpy()

        # Plot data as histogram (density)
        ax = sns.histplot(data=trial_sizes + 1 , kde=False, log_scale=True, bins=10, color='#82cafc')
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        plt.minorticks_off()

        # Plot mean
        ax.axvline(trial_sizes.mean(), ls='dashed', color='#444444', linewidth=1)
        print('Maximum trial size: {}'.format(trial_sizes.max()))
        print('Minimum trial size: {}'.format(trial_sizes.min()))
        print('Mean trial size: {}'.format(trial_sizes.mean()))
        print('Confidence Intervals:{}'.format(sm.stats.DescrStatsW(trial_sizes).tconfint_mean(alpha = 0.05)))


        # Set titles, labels
        plt.ylim(bottom=0, top=25)
        plt.xlim(left=6, right=2277)
        plt.xlabel('Total trials')
        plt.ylabel('Count')

        # Add label for mean
        # _, max_ylim = plt.ylim()
        # plt.text(trial_sizes.mean()*1.3, max_ylim*0.85, 'Mean:\n{:.1f}'.format(trial_sizes.mean()))
        plt.tight_layout()

        # Save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalTrialSizes{}{}.pdf'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalTrialSizes{}{}.png'.format(self.memory, self.group))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyHumanFinalTrialSizes{}{}.svg'.format(self.memory, self.group))
        plt.close()
    
    def plot_trials_agegroups(self):
        """ Plots the number of trials the children played the game for in age groups.
        """

        # Print info for user
        print('\nPlot number of trials the children played the game for in age groups.')

        ## Descriptive analysis of children in age groups

        # Preparing data
        self.data_children = data_handle.get_player_data(memory=True, group='children')
        idx = self.data_children.groupby('id')["trial"].idxmax()
        result_children = self.data_children.loc[idx]

        # define the age groups
        bins = [5, 6, 7, 8, 9, 10, 13]
        labels = ['5-6', '7', '8', '9', '10', '11-13']

        # group the data by age group and calculate the average trial value
        result_children['age_group'] = pd.cut(result_children['age'], bins=bins, labels=labels)
        grouped_data = result_children.groupby('age_group')["trial"].mean().reset_index()

        # n
        group_len = result_children.groupby('age_group')["trial"].size()
        agg_groups = pd.DataFrame({'n' : group_len})

        # mean
        agg_groups["mean"] = result_children.groupby('age_group')["trial"].mean()

        # standard deviation
        agg_groups["std"] = result_children.groupby('age_group')["trial"].std()

        # SEM
        agg_groups["sem"] = agg_groups["std"]/np.sqrt(agg_groups["n"])

        # 95% CI 
        agg_groups["under"] = agg_groups["mean"]- 1.96*agg_groups["sem"]
        agg_groups["upper"] = agg_groups["mean"]+ 1.96*agg_groups["sem"]
        agg_groups['95% CI'] = agg_groups[['under', 'upper']].apply(tuple, axis=1)
        agg_groups.drop(columns=["under","upper"], inplace=True)

        print("\nDescriptive analysis of children's trials in age groups:\n{}".format(agg_groups))

        ## Point plot

        # Setting style
        sns.set_style("whitegrid")
        plt.rcParams["axes.edgecolor"] = "0.15"
        plt.rcParams["axes.linewidth"] = 1.25

        plt.figure(figsize=(8, 6))
        sns.pointplot(data=result_children, x= "age_group", y="trial",  color='#E1812C', errorbar=None)

        # Add 95% CIs
        i = 0
        for row in agg_groups.index:
            plt.errorbar(i, agg_groups["mean"][row], yerr=1.96*agg_groups['sem'][row], c='#E1812C', lw= 3, capsize = 10, capthick=3)
            i += 1

        # Setting Axes
        plt.title('Trials Children', fontsize = 18)
        plt.xlabel('Age group [years]', fontsize = 16)
        plt.ylabel('Trials', fontsize = 16)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsChildrenAgegroups{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsChildrenAgegroup{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsChildrenAgegroups{}.svg'.format(self.memory))

    def plot_trials_comparison(self):
        """ Plots comparison of trials children vs. adults.
        """

        # Print info for user
        print('\nPlot comparison of trials children vs. adults.')

        # Preparing data
        self.data = data_handle.get_player_data(memory=True, group='combined')
        idx = self.data.groupby('id')['trial'].idxmax()
        result = self.data.loc[idx]

        print('\nComparison of trials children and adults:\n{}'.format(result.groupby('group')["trial"].describe()))

        ## Box plot

        # Setting style
        sns.set_style("whitegrid")
        plt.rcParams["axes.edgecolor"] = "0.15"
        plt.rcParams["axes.linewidth"] = 1.25

        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.data, x='group', y='trial', showmeans=True, meanprops = {"marker" :"x"})

        # Setting Axes
        plt.ylabel('Trials', fontsize = 16)
        plt.xlabel('', fontdict={'fontsize': 16})
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsComparison{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsComparison{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyTrialsComparison{}.svg'.format(self.memory))



    def plot_success_probability(self):
        """ Plots probabilty of trying a successful combinations in relation to number of trials/invenotory size.
        """

        # Get data
        self.data_children = data_handle.get_player_data(memory=True, group='children')
        self.data_adults = data_handle.get_player_data(memory=True, group='adults')

        ## Plot success probability in relation to number of trials

        # Print info for user
        print('\nPlot success probability in relation to number of trials.')

        # Exluding participants with less than 100 trials

        # group by 'id' and count the number of trials
        trial_countsB = self.data_children.groupby('id').size()
        trial_countsA = self.data_adults.groupby('id').size()

        # filter out the 'id's with less than 100 trials
        valid_idsB = trial_countsB[trial_countsB >= 100].index
        valid_idsA = trial_countsA[trial_countsA >= 100].index

        # filter the original dataframe by the valid 'id's
        df_children = self.data_children[self.data_children['id'].isin(valid_idsB)]
        df_adults = self.data_adults[self.data_adults['id'].isin(valid_idsA)]

        # Setting figure size
        plt.figure(figsize=(20, 10))

        sns.lineplot(x='trial', y= 'success', label = "Adults", data = df_adults)
        sns.lineplot(x='trial', y= 'success', label = "Children", data = df_children)

        # Setting Axes
        plt.xlabel('Trial', fontsize = 36)
        plt.ylabel('P(Success)', fontsize = 36)
        plt.xlim(0, 100)
        plt.tick_params(axis='both', which='major', labelsize=24)
        plt.legend(loc='upper right', fontsize = 28)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityTrials{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityTrials{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityTrials{}.svg'.format(self.memory))

        ## Plot success probability in relation to inventory size

        # Print info for user
        print('\nPlot success probability in relation to inventory size.')

        # Exluding participants with more than inventory size 20

        # group by 'id' and get the max inventory size
        inventory_sizeB = self.data_children.groupby('id')['inventory'].max()
        inventory_sizeA = self.data_adults.groupby('id')['inventory'].max()

        # filter out the 'id's with less than 20 inventory size
        valid_idsB = inventory_sizeB[inventory_sizeB <= 20].index
        valid_idsA = inventory_sizeA[inventory_sizeA <= 20].index

        # filter the original dataframe by the valid 'id's
        df_children = self.data_children[self.data_children['id'].isin(valid_idsB)]
        df_adults = self.data_adults[self.data_adults['id'].isin(valid_idsA)]

        # Setting figure size
        plt.figure(figsize=(20, 10))

        sns.lineplot(x='inventory', y= 'success', label = "Adults", data = df_adults)
        sns.lineplot(x='inventory', y= 'success', label = "Children", data = df_children)

        # Setting Axes
        plt.xlabel('Inventory Size', fontsize = 36)
        plt.ylabel('P(Success)', fontsize = 36)
        plt.xlim(5, 20)
        plt.tick_params(axis='both', which='major', labelsize=24)
        plt.legend(loc='upper right', fontsize = 28)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityInventory{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityInventory{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemySuccessprobabilityInventory{}.svg'.format(self.memory))

    def plot_average_empowerment(self):
        """ Plots average empowerment of the first 15 created elements.
        """

        # Get data
        self.data = data_handle.get_player_data(memory=True, group='combined')

        # Print info for user
        print('\nPlot average empowerment of the first 15 created elements.')

        # Excluding every participant with a final inventory size < 15
        df = self.data[self.data['success'] != 0] # Exclude unsuccessful trials

        # exclude 'id's with less than 15 rows
        df = df.groupby('id').filter(lambda x: len(x) >= 15)

        df = df.groupby('id').head(15) # Only take the first 15 trials

        # Setting style
        sns.set_style("white")
        plt.rcParams["axes.edgecolor"] = "0.15"
        plt.rcParams["axes.linewidth"] = 1.25
        plt.figure(figsize=(8, 6))
        sns.barplot(data=df, x='group', y='emp_value')

        # Setting Axes
        plt.title('Average Empowerment of the First 15 Created Elements', fontsize = 18)
        plt.ylabel('Empowerment', fontsize = 16)
        plt.xlabel('', fontsize = 16)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAverageEmpowerment{}.pdf'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAverageEmpowerment{}.png'.format(self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAverageEmpowerment{}.svg'.format(self.memory))
