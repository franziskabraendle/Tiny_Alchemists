import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pickle import FALSE, TRUE
import empowermentexploration.utils.data_handle as data_handle

class Summary():
    """Class functions generate summary for playerdata.
    """
    def __init__(self):
        """Initializes playerdata childrenalchemy.
        """
        # Print info for user
        print('\nGet sample summary.')

        # Reading in Data
        self.data = self.data = data_handle.get_player_data(memory=True, group='combined') # Data from children and adults
        self.data_children = data_handle.get_player_data(memory=True, group='children') # Data from children
        self.data_adults = data_handle.get_player_data(memory=True, group='adults') # Data from adults
    
        # Overview of data sample
        print('\nNumber of participants: {}'.format(len(self.data['id'].unique())))
        print('- children: {}'.format(len(self.data_children['id'].unique())))
        print('- adults: {}'.format(len(self.data_adults['id'].unique())))

    def age_distribution(self):
        """ Plots age distribution of children.
        """

        # Print info for user
        print('\nPlot age distribution of children.')

        # Only keep first entry of each child
        self.data_children.drop_duplicates(subset='id', keep='first', inplace=True)
        
        # Descriptive Analysis
        print('\nDescriptive Analysis:\n{}'.format(self.data_children.describe()['age'])) # summary

        # Histogram
        sns.histplot(data=self.data_children['age'], kde = True)

        # Add mean
        age_mean = self.data_children['age'].mean() # mean
        plt.axvline(age_mean, ls='dashed', color='black', linewidth=1, label= "mean")

        # Setting Axes
        plt.title("Age Distribution Children", fontsize = 18)
        plt.xlabel("Age [years]", fontsize = 14)
        plt.ylabel("Count", fontsize = 14)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()  

        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAgedistribution.pdf')
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAgedistribution.png')
        plt.savefig('empowermentexploration/resources/playerdata/figures/childrenalchemyAgedistribution.svg')

    

   