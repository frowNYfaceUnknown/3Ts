class GameBoard:
    def __init__(self) -> None:
        self.gameBoard = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.emptyTiles = [(0, 0), (0, 1), (0, 2),
                           (1, 0), (1, 1), (1, 2),
                           (2, 0), (2, 1), (2, 2)]
        self.currPlayer = 0 ## 0 means |, 1 means -, and 2 means +.
        self.lastStep = 0
        self.gameOver = False

    def moveTo(self, x: int, y: int) -> int:
        if self.gameBoard[x][y] == '+' or (self.gameBoard[x][y] == '|' and self.currPlayer == 0) or (self.gameBoard[x][y] == '-' and self.currPlayer == 1):
            return -1

        if (x, y) == self.lastStep:
            return -1

        if self.gameBoard[x][y] == '|' or self.gameBoard[x][y] == '-':
            self.gameBoard[x][y] = '+'
            self.emptyTiles.remove((x, y))

        if self.currPlayer == 0 and self.gameBoard[x][y] != '+': ## second condition is to make sure the value
            self.gameBoard[x][y] = '|'                           ## wasn't changed in this instance itself
        
        if self.currPlayer == 1 and self.gameBoard[x][y] != '+': ## second condition is to make sure the value
            self.gameBoard[x][y] = '-'                           ## wasn't changed in this instance itself
        
        self.lastStep = (x, y)
        self.currPlayer = not self.currPlayer
        return not self.currPlayer
    
    def checkWin(self) -> int:
        ## check for all the rows
        for x in range(3):
            if self.gameBoard[0][x] == self.gameBoard[1][x] == self.gameBoard[2][x] == '+':
                self.gameOver = True
                return int(not self.currPlayer)

        ## check for all the row
        for y in range(3):
            if self.gameBoard[y][0] == self.gameBoard[y][1] == self.gameBoard[y][2] == '+':
                self.gameOver = True
                return int(not self.currPlayer)

        ## check for both the diagonals
        if self.gameBoard[0][0] == self.gameBoard[1][1] == self.gameBoard[2][2] == '+':
            self.gameOver = True
            return int(not self.currPlayer)
        if self.gameBoard[0][2] == self.gameBoard[1][1] == self.gameBoard[2][0] == '+':
            self.gameOver = True
            return int(not self.currPlayer)
        
    def resetGB(self) -> None:
        self.__init__()

    def printBoard(self) -> None:
        for i in self.gameBoard:
            print(i)