import empowermentexploration.utils.data_handle as data_handle


class TrueEmpModel():
    """Empowerment model based on true game tree.
    """
    def __init__(self):
        """Initializes a little alchemy empowerment model based on true game tree.
        """
        # get parent table to check for resulting elements
        self.parent_table = data_handle.get_parent_table()
        
        # get combination table 
        self.combination_table = data_handle.get_combination_table(csv=False)
                
    def get_value(self, combination):
        """Returns empowerment value for given combination.

        Args:
            combination (list): List of element indices that are involved in combination.

        Returns:
            float: Value.
        """            
        # check results of combination
        if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
            results = self.combination_table[combination[0]][combination[1]]
        else:
            results = list()
        
        # initialize empowerment depending on how it is calculated
        empowerment = set()
        
        # calculate empowerment value iteratively for each result
        for r in results: 
            if r in self.parent_table:
                empowerment.update(self.parent_table[r])

        return len(empowerment)
