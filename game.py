MAX_COLUMN = 6
MAX_ROW = 5

class Connect4:
    def __init__(self):
        # initialize state to get a new board
        self.board = [["." for _ in range(7)] for _ in range(6)]
        self.board.append(list(range(7)))
        self.nextRowForColumn = dict.fromkeys(range(7), 5)

        self.turn = 0
        self.disks = ["O", "X"]
        self.gameActive = True

    def printBoard(self):
        # displays the current state of the board for the players to see
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))

    def insertChip(self, column, playerDisk):
        # find row for where the disk falls to
        diskRow = self.nextRowForColumn[column]
        # update nextRowForColumnMap
        self.nextRowForColumn[column]-=1
        # update self.board
        self.board[diskRow][column] = playerDisk
        # output the row that the playerDisk has fallen to
        self.printBoard()
        return diskRow

    def getPlayerInput(self, playerNumber):
        while True:
            try:
                # get player input
                givenInput = int(input(f"Player {playerNumber}'s move: "))

                if 0 <= givenInput <= 6:
                    if self.nextRowForColumn[givenInput] < 0:
                        print("You dropped your disk onto a full column, it topples out pathetically. Try again")
                    else:
                        return givenInput # Valid input exits the function immediately
                else:
                    print(f"You dropped your disk outside of the gameboard, silly goose! Try again")
                    
            except ValueError:
                print("You seem a bit confused, try again, choosing a number between 0 and 6.")

    def checkDirection(self, diskRow, diskColumn, playerDisk, rowMod, columnMod):
        checkRow = diskRow+rowMod
        checkColumn = diskColumn+columnMod

        adjacentScore = 0
        while 0 <= checkColumn <= MAX_COLUMN and 0 <= checkRow <= MAX_ROW:
            if self.board[checkRow][checkColumn] == playerDisk:
                adjacentScore += 1
                checkRow += rowMod
                checkColumn += columnMod
            else:
                return adjacentScore            
        return adjacentScore

    def checkWin(self, diskRow, diskColumn, playerDisk):
        # check all directions for a win
        counterRow = 0
        counterDown = 0
        counterSlash = 0
        counterBackslash = 0

        counterRow += self.checkDirection(diskRow, diskColumn, playerDisk, 0, -1) # left
        counterRow += self.checkDirection(diskRow, diskColumn, playerDisk, 0, +1) # right
        counterDown += self.checkDirection(diskRow, diskColumn, playerDisk, +1, 0) # down
        counterSlash += self.checkDirection(diskRow, diskColumn, playerDisk, -1, +1) # NE
        counterSlash += self.checkDirection(diskRow, diskColumn, playerDisk, +1, -1) # SW
        counterBackslash += self.checkDirection(diskRow, diskColumn, playerDisk, -1, -1) # NW
        counterBackslash += self.checkDirection(diskRow, diskColumn, playerDisk, +1, +1) # SE
        
        return (counterRow >= 3 or counterDown >= 3 or counterSlash >= 3 or counterBackslash >= 3)
    
    def play(self):
        # game loop
        self.printBoard()

        while self.gameActive:
            playerNumber = (self.turn%2)+1
            playerDisk = self.disks[playerNumber-1]

            diskColumn = self.getPlayerInput(playerNumber)
            # updates & prints the game board, updates the nextRowForColumn dict, and returns the diskRow
            diskRow = self.insertChip(diskColumn, playerDisk)

            if self.checkWin(diskRow, diskColumn, playerDisk): # self.checkWin returns a boolean
                print(f"Player {playerNumber} Wins!")
                self.gameActive = False
                break

            if all(val < 0 for val in self.nextRowForColumn.values()): # when a column is full the value drops to -1; therefore if all the values are -1, the board is full and since no win condition has been detected, the game is a draw
                print("It's a draw!")
                self.gameActive = False
                break
            
            self.turn += 1

if __name__ == "__main__":
    game = Connect4()
    game.play()