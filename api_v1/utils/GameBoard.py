class GameBoard:

    def __init__(self, map_state, map_original):
        self.map_state = map_state
        self.map_original = map_original
        self.hasLost = False
        self.hasWon = False
        self.row = 10
        self.col = 10

    def getHasLost(self):
        return self.hasLost
    

    def getHasWon(self):
        return self.hasWon

    
    def getMapState(self):
        return self.map_state
    

    def getMapOriginal(self):
        return self.map_original


    """
    Creates the final solution map
    """
    def createSolution(self):
        for row in range(self.row):
            for col in range(self.col):
                if self.map_original[row][col]['has_mine']:
                    self.map_original[row][col]['adj'] = self.getMinesAround(row, col)
                    self.map_original[row][col]['is_revealed'] = True
                    if self.map_original[row][col]['has_flag']:
                        self.map_original[row][col]['state'] = 4
                    else:
                        self.map_original[row][col]['state'] = 2


    """
    Updates cell properties in original map when it is visited during search
    """
    def markCellVisited(self, r, c):
        self.map_original[r][c]['adj'] = self.getMinesAround(r, c)
        self.map_original[r][c]['is_revealed'] = True
        self.map_original[r][c]['state'] = 1


    """
    Find out if player has won/lost after a move
    """
    def hasPlayerWon(self):
        hasWon = True
        for row in range(self.row):
            for col in range(self.col):
                cell = self.map_original[row][col]
                if not cell['has_mine'] and not cell['is_revealed']:
                    hasWon = False
        return hasWon 


    """
    Traverse the map safely in all directions while revealing the cells along the way until you find a mine
    """
    def reveal(self, r, c):


        # bound checks
        if (r < 0 or c < 0 or r >= len(self.map_original) or c >= len(self.map_original[0])):
            return

        cell = self.map_original[r][c]

        # stop searching if found a mine
        if cell['has_mine'] == True or cell['is_revealed'] == True:
            return

        if not cell['has_flag']:
            self.markCellVisited(r, c)

        # Dont search further if any of the next cells has a mine
        if cell['adj'] > 0:
            return

        self.reveal(r+1, c)
        self.reveal(r-1, c)
        self.reveal(r, c+1)
        self.reveal(r, c-1)
        self.reveal(r+1, c+1)
        self.reveal(r+1, c-1)
        self.reveal(r-1, c+1)
        self.reveal(r-1, c-1)


    """
    Calculates the new map state based on the move sent by the user
    """
    def makeMove(self, move):

        intent = move['intent']
        cell_index = move['cell'].split("-")

        row = int(cell_index[0])
        col = int(cell_index[1])

        cell = self.map_original[row][col]
        
        # Intent is to reveal the cell
        if intent == 'reveal':

            if cell['has_flag']:
                return self.syncAndReturn()

            # found a mine already, finish the game
            if cell['has_mine']:
                self.createSolution()
                return self.syncAndReturn(True)
            else:
    
                mines_around = self.getMinesAround(row, col)

                if mines_around > 0:
                    
                    self.markCellVisited(row, col)
                    return self.syncAndReturn()

                if cell['state'] == 0:
                    self.reveal(row, col)
                    return self.syncAndReturn()

        # intent is to flag this cell
        elif intent == 'flag':

            if cell['state'] == 0:
                cell['has_flag'] = True
                cell['state'] = 3
            elif cell['state'] == 3:
                cell['has_flag'] = False
                cell['state'] = 0

        return self.syncAndReturn()


    """
    Sync map current original state with the new state
    """
    def synchronize(self):
        for row in range(self.row):
            for col in range(self.col):
                self.map_state[row][col]['adj'] = self.map_original[row][col]['adj']
                self.map_state[row][col]['state'] = self.map_original[row][col]['state']
                self.map_state[row][col]['has_mine'] = self.map_original[row][col]['has_mine']


    """
    Sync map current original state with the new state and return new state with result
    """
    def syncAndReturn(self, hasLost=False):
        hasWon = self.hasPlayerWon()
        if hasWon:
            self.createSolution()
        self.synchronize()
        self.hasLost = hasLost
        self.hasWon = hasWon
        return


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