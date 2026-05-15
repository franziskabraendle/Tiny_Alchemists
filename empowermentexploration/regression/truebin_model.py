import empowermentexploration.utils.data_handle as data_handle


class TrueBinModel():
    """Binary model based on true game tree.
    """
    def __init__(self):
        """Initializes a little alchemy binary model based on true game tree.
        """      
        # get combination table 
        self.combination_table = data_handle.get_combination_table(csv=False)
        
    def get_value(self, combination):
        """Returns value for given combination.

        Args:
            combination (list): List of element indices that are involved in combination.

        Returns:
            float: Value.
        """  
        utility = 0
        if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
            utility = 1
            
        return utility
