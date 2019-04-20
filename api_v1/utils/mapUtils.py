import random
import copy
import scipy.sparse as sparse
import scipy.stats as stats
import numpy as np

def getNewMap():
    row, col = 10, 10
    num_of_mines = 15

    new_map = []

    matrix = sparse.random(10, 10, density=0.15, data_rvs=np.ones).toarray()

    # create empty map
    for i in range(row):
        new_map.append([])
        for j in range(col):
            new_map[i].append({
                "adj": 0, 
                "state": 0,
                "has_mine": False,
                "is_revealed": False,
                "has_flag": False
            })
    
    map_state = copy.deepcopy(new_map)

    # populate map with mines
    for r in range(row):
        for c in range(col):
            if matrix[r][c] == 1:
                new_map[r][c]['has_mine'] = True    


    map_original = copy.deepcopy(new_map)
    return map_state, map_original