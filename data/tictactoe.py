class GameBoard:
    def __init__(self) -> None:
        self.gameBoard = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.emptyTiles = [(0, 0), (0, 1), (0, 2),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1), (2, 2)]
        self.currPlayer = 0
        self.gameOver = False

    def moveTo(self, x: int, y: int) -> int:
        if self.gameBoard[x][y] != 0:
            return -1

        if self.currPlayer == 0: self.gameBoard[x][y] = 'O'
        else: self.gameBoard[x][y] = 'X'
        
        self.emptyTiles.remove((x, y))
        self.currPlayer = not self.currPlayer
        return not self.currPlayer
    
    def checkWin(self) -> int:
        ## check for all the rows
        for x in range(3):
            if self.gameBoard[0][x] == self.gameBoard[1][x] == self.gameBoard[2][x] != 0:
                self.gameOver = True
                return int(not self.currPlayer)

        ## check for all the row
        for y in range(3):
            if self.gameBoard[y][0] == self.gameBoard[y][1] == self.gameBoard[y][2] != 0:
                self.gameOver = True
                return int(not self.currPlayer)

        ## check for both the diagonals
        if self.gameBoard[0][0] == self.gameBoard[1][1] == self.gameBoard[2][2] != 0:
            self.gameOver = True
            return int(not self.currPlayer)
        if self.gameBoard[0][2] == self.gameBoard[1][1] == self.gameBoard[2][0] != 0:
            self.gameOver = True
            return int(not self.currPlayer)
        
        ## check for draw
        if len(self.emptyTiles) == 0:
            self.gameOver = True
            return -1
        
    def resetGB(self):
        self.__init__()