import random
import copy
import numpy as np

def getNewMap():
    row, col = 10, 10
    num_of_mines = 15

    new_map = []

    matrix = np.random.randint(2, size=(row, col))

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

    # for r in range(row):
    #     for c in range(col):
    #         if matrix[r][c] == 1:
    #             new_map[r][c]['has_mine'] = True    

    # populate map with mines
    rows_for_mines = random.randint(0, row)
    for i in range(rows_for_mines):
        rand_row = random.randint(0, row-1)
        cells_for_mines = random.randint(0, col)
        for j in range(cells_for_mines):
            rand_cell = random.randint(0, col-1)
            new_map[rand_row][rand_cell]['has_mine'] = True

    map_original = copy.deepcopy(new_map)
    return map_state, map_original