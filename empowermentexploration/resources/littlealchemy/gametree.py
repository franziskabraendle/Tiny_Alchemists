import json

class Gametrees():
    """Class functions generate Little Alchemy game trees.
    """
    def __init__(self):
        """Initializes game tree class.
        """

    def get_children_gametree(self):
        """Gets game tree of Tiny Alchemy (based on 'Little Alchemy 1') used in Braendle et al. (2022).
        """
        # print info for user
        print('\nGet childrenalchemy game tree.')

        # load raw gametree
        with open('empowermentexploration/resources/littlealchemy/data/raw/rawTinyGametree.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # load elements
        with open('empowermentexploration/resources/littlealchemy/data/raw/tinyalchemyElements.json', encoding='utf8') as infile:
            elements = json.load(infile)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        # initialize memory storing previous combinations
        memory = list()

        # fill game tree
        for element_combinations in old_gametree:
            for combination in element_combinations[1]:
                # when combinations yield more than one element, keep only the first
                if sorted(combination) not in memory:
                    gametree[element_combinations[0]]['parents'].append(sorted(combination))
                    memory.append(sorted(combination))

        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyGametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyElements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)
            
    
    def get_clean_gametree(self):
        """Removes all combinations from the game tree that entail elements that cannot be created due to the adaptation of the original game tree.
        """
        # print info for user
        print('\nClean childrenalchemy game tree.')

        # load gametree
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyGametree.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # Collect all elements with no parents
        nonexisting_elements = []
        for key in old_gametree:
            parents = old_gametree[str(key)]["parents"]
            if parents == []:
                nonexisting_elements.append(key) 

        # Ignore first 4 elements {water, fire, earth, wind} as they have no parents
        nonexisting_elements[:4] = []

        # Search for and delete combinations with nonexisting element

        # Iterating over all nonexisting elements
        for nonexisting_element in nonexisting_elements:
            # Iterating over all elements in gametree (ignoring the first 4 elements)
            for element in range(4,540): # the tiny alchemy game tree contains 540 elements 
                # All combinations to create one element
                combinations = old_gametree[str(element)]["parents"]
                # Iterate over list of combinations and search for nonexisting element
                combination = 0
                while (combination < len(combinations)) and (len(combinations) > 0):
                    # When nonexisting element is part of the combination: delete combination
                    if int(nonexisting_element) in combinations[combination]:
                        combinations.remove(combinations[combination])
                    else:
                        combination += 1
                # Check, if the only combination left is recursive, if so: delete combination (e.g., '520': 'Werewolf')
                if (len(combinations) == 1) and (element in combinations[0]):
                    combinations.remove(combinations[0])
                # If an element cannot be created anymore and is not already on the list, add it to nonexisting elements
                if (combinations == []) and (str(element) not in nonexisting_elements):
                    nonexisting_elements.append(str(element))

        # New clean gametree
        clean_gametree = old_gametree

        # Convert clean gametree to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyCleanGametree.json', 'w') as filehandle:
            json.dump(clean_gametree, filehandle, indent=4)


    def get_shortened_gametree(self):
        """Shortens game tree to only contain elements that can be created + list of elements that cannot be created anymore.
        """
        # print info for user
        print('\nShorten childrenalchemy game tree.')

        # load clean gametree
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyCleanGametree.json', encoding='utf8') as infile:
            gametree = json.load(infile)

        # Remove all elements from the dictionary that cannot be created
        nonexisting_elements = []
        for element in range(4,540):
            if gametree[str(element)]["parents"] == []:
                nonexisting_elements.append(gametree[str(element)]["name"])
                del gametree[str(element)]

        # Convert shortened gametree to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyShortenedGametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4)
        
        # List of elements that cannot be created
        with open('empowermentexploration/resources/littlealchemy/data/childrenalchemyNonexistingElements.json', 'w') as filehandle:
            json.dump(nonexisting_elements, filehandle, indent=4)