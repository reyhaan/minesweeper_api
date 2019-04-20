class GameBoard:

    def __init__(self, map_state, map_original):
        self.map_state = map_state
        self.map_original = map_original
        self.row = 10
        self.col = 10
        self.num_of_mines = 0


    def getState(self, cell):

        if cell['has_flag'] == True:
            return 3
        elif cell['has_flag'] == False and cell['is_revealed'] == False:
            return 0
        elif cell['is_revealed'] == True and cell['has_mine'] == True:
            return 2
        elif cell['is_revealed'] == True and not cell['has_mine']:
            return 1


    def createSolution(self):
        for row in range(self.row):
            for col in range(self.col):
                self.map_original[row][col]['adj'] = self.getMinesAround(row, col)
                self.map_original[row][col]['is_revealed'] = True
                self.map_original[row][col]['state'] = self.getState(self.map_original[row][col])


    def markCellVisited(self, r, c):
        self.map_original[r][c]['adj'] = self.getMinesAround(r, c)
        self.map_original[r][c]['is_revealed'] = True
        self.map_original[r][c]['state'] = self.getState(self.map_original[r][c])


    """
    Traverse the map safely in all directions while revealing the cells along the way until you find a mine
    """
    def reveal(self, r, c):

        # bound checks
        if (r < 0 or c < 0 or r >= len(self.map_original) or c >= len(self.map_original[0])):
            return

        # stop searching if found a mine
        if self.map_original[r][c]['has_mine'] == True or self.map_original[r][c]['is_revealed'] == True:
            return

        self.markCellVisited(r, c)

        # Dont search further if any of the next cells has a mine
        if self.map_original[r][c]['adj'] > 0:
            return

        self.reveal(r+1, c)
        self.reveal(r-1, c)
        self.reveal(r, c+1)
        self.reveal(r, c-1)
        self.reveal(r+1, c+1)
        self.reveal(r+1, c-1)
        self.reveal(r-1, c+1)
        self.reveal(r-1, c-1)


    def makeMove(self, move):

        intent = move['intent']
        cell_index = move['cell'].split("-")

        row = int(cell_index[0])
        col = int(cell_index[1])

        cell = self.map_original[row][col]
        
        cell_state = self.getState(cell)

        # Intent is to reveal the cell
        if intent == 'reveal':

            # found a mine already, finish the game
            if cell['has_mine']:
                self.createSolution()
                return self.syncAndReturn(True)
            else:
    
                mines_around = self.getMinesAround(row, col)

                if mines_around > 0:
                    
                    self.markCellVisited(row, col)
                    return self.syncAndReturn(False)

                if cell_state == 0:
                    self.reveal(row, col)
                    return self.syncAndReturn(False)

        # intent is to flag this cell
        elif intent == 'flag':

            if cell_state == 0:
                cell['has_flag'] = True
                cell['state'] = 3
            else:
                cell['has_flag'] = False

        return self.syncAndReturn(False)


    """
    Sync map current original state with the new state
    """
    def synchronize(self):
        for row in range(self.row):
            for col in range(self.col):
                self.map_state[row][col]['adj'] = self.map_original[row][col]['adj']
                self.map_state[row][col]['state'] = self.map_original[row][col]['state']


    """
    Sync map current original state with the new state and return new state with result
    """
    def syncAndReturn(self, result):
        self.synchronize()
        return self.map_state, result


    """
    Given a cell in the map, get number of mines around all 8 cells
    """
    def getMinesAround(self, row, col):
        mines = 0
        max_rows = self.row
        max_cols = self.col

        def findMine(row, col, max_rows, max_cols):
            if row >= 0 and row < max_rows and col >= 0 and col < max_cols:
                cell = self.map_original[row][col]
                if cell['has_mine'] == True:
                    return 1
            return 0

        mines = mines + findMine(row+1, col, max_rows, max_cols)        
        mines = mines + findMine(row-1, col, max_rows, max_cols)        
        mines = mines + findMine(row, col+1, max_rows, max_cols)        
        mines = mines + findMine(row, col-1, max_rows, max_cols)        
        mines = mines + findMine(row+1, col+1, max_rows, max_cols)        
        mines = mines + findMine(row+1, col-1, max_rows, max_cols)        
        mines = mines + findMine(row-1, col+1, max_rows, max_cols)        
        mines = mines + findMine(row-1, col-1, max_rows, max_cols)        
        
        return mines