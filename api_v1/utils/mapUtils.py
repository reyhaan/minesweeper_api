import random
import copy

def makeMove(move, map_state, map_original):

    intent = move['intent']
    cell = move['cell'].split("-")

    row = int(cell[0])
    col = int(cell[1])

    # print(row, col, map_original)

    def reveal(map_state, r, c):
        if (r < 0 or c < 0 or r >= len(map_state) or c >= len(map_state[0])):
            return map_state

        if map_state[r][c]['state'] == 2:
            return map_state


    cell_state = map_original[row][col]['state']
    print(cell_state)

    if intent == 'reveal':
        if cell_state == 0:
            return map_state
        elif cell_state == 1:
            reveal(map_original, row, col)
        elif cell_state == 2:
            pass
        elif cell_state == 3:
            pass
    elif intent == 'flag':
        if cell_state == 0 or cell_state == 2:
            map_state[row][col]['state'] = 3
        elif cell_state == 1 or cell_state == 3:
            return map_state

    return map_state


def getNewMap():
    row, col = 10, 15
    num_of_mines = 15

    new_map = []

    # create empty map
    for i in range(row):
        new_map.append([])
        for j in range(col):
            new_map[i].append({"adj": 0, "state": 0})
    
    map_state = copy.deepcopy(new_map)

    # populate map with mines
    rows_for_mines = random.randint(0, row)
    for i in range(rows_for_mines):
        rand_row = random.randint(0, row-1)
        cells_for_mines = random.randint(0, col)
        print(cells_for_mines)
        for j in range(cells_for_mines):
            rand_cell = random.randint(0, col-1)
            print(new_map[rand_row][rand_cell])
            new_map[rand_row][rand_cell]['state'] = 2

    map_original = copy.deepcopy(new_map)
    return map_state, map_original
