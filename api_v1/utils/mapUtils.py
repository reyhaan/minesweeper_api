import random

def makeMove(move, map):
    return move

def getNewMap():
    row, col = 10, 15
    num_of_mines = 15

    new_map = []

    # create empty map
    for i in range(row):
        new_map.append([])
        for j in range(col):
            new_map[i].append({"adj": 0, "state": 0})

    # populate map with mines
    rows_for_mines = random.randint(0, row)
    for i in range(rows_for_mines):
        rand_row = random.randint(0, row-1)
        cells_for_mines = random.randint(0, col)
        for j in range(cells_for_mines):
            rand_cell = random.randint(0, col-1)
            new_map[rand_row][rand_cell]['state'] = 2

    return new_map
