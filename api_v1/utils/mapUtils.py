import random
import copy
import numpy as np

def getState(cell):
    if cell['has_flag'] == True:
        return 3
    elif cell['has_flag'] == False and cell['is_revealed'] == False:
        return 0
    elif cell['is_revealed'] == True and cell['has_mine'] == True:
        return 2
    elif cell['is_revealed'] == True and not cell['has_mine']:
        return 1


def createSolution(map_state):
    for row in map_state:
        for col in row:
            map_state[row][col]['adj'] = getMinesAround(map_state, row, col)
            map_state[row][col]['is_revealed'] = True
            map_state[row][col]['state'] = getState(map_state[row][col])
    return map_state


def markCellVisited(map_original, r, c):

    map_original[r][c]['adj'] = getMinesAround(map_original, r, c)
    map_original[r][c]['is_revealed'] = True
    map_original[r][c]['state'] = getState(map_original[r][c])

    return map_original


def makeMove(move, map_state, map_original):

    intent = move['intent']
    cell_index = move['cell'].split("-")

    row = int(cell_index[0])
    col = int(cell_index[1])

    def reveal(map_original, r, c):

        # bound checks
        if (r < 0 or c < 0 or r >= len(map_original) or c >= len(map_original[0])):
            return

        # stop searching if found a mine
        if map_original[r][c]['has_mine'] == True or map_original[r][c]['is_revealed'] == True:
            return

        map_original = markCellVisited(map_original, r, c)

        reveal(map_original, r+1, c)
        reveal(map_original, r-1, c)
        reveal(map_original, r, c+1)
        reveal(map_original, r, c-1)
        reveal(map_original, r+1, c+1)
        reveal(map_original, r+1, c-1)
        reveal(map_original, r-1, c+1)
        reveal(map_original, r-1, c-1)

        return map_original


    cell = map_original[row][col]
    
    cell_state = getState(cell)

    # Intent is to reveal the cell
    if intent == 'reveal':
    
        mines_around = getMinesAround(map_original, row, col)

        if mines_around > 0 and cell_state == 0:
            return markCellVisited(map_original, row, col)

        if cell_state == 0:
            return reveal(map_original, row, col)
        elif cell_state == 1:
            return map_state
        elif cell_state == 2:
            return createSolution(map_original)
        elif cell_state == 3:
            return map_state

    # intent is to flag this cell
    elif intent == 'flag':

        if cell_state == 0:
            cell['has_flag'] = True
            cell['state'] = 3
        else:
            cell['has_flag'] = False

    return map_original


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


def getMinesAround(map_state, row, col):
    mines = 0
    max_rows = len(map_state)
    max_cols = len(map_state[0])

    def findMine(row, col, max_rows, max_cols, map_state):
        if row >= 0 and row < max_rows and col >= 0 and col < max_cols:
            cell = map_state[row][col]
            if cell['has_mine'] == True:
                return 1
        return 0

    mines = mines + findMine(row+1, col, max_rows, max_cols, map_state)        
    mines = mines + findMine(row-1, col, max_rows, max_cols, map_state)        
    mines = mines + findMine(row, col+1, max_rows, max_cols, map_state)        
    mines = mines + findMine(row, col-1, max_rows, max_cols, map_state)        
    mines = mines + findMine(row+1, col+1, max_rows, max_cols, map_state)        
    mines = mines + findMine(row+1, col-1, max_rows, max_cols, map_state)        
    mines = mines + findMine(row-1, col+1, max_rows, max_cols, map_state)        
    mines = mines + findMine(row-1, col-1, max_rows, max_cols, map_state)        
    
    return mines