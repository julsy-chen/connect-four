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
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))
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
                    print(f"You dropped your disk outside of the gameboard, silly guy! Try again")
                    
            except ValueError:
                print("You seem a bit confused, try again, choosing a number between 0 and 6.")

    def checkWin(self, diskRow, diskColumn, playerDisk):
        # check all directions for a win
        counterRow = 0
        counterDown = 0
        counterSlash = 0
        counterBackslash = 0

        c = 1
        while 0<=diskColumn - c: #check left side
            if self.board[diskRow][diskColumn-c] == playerDisk:
                counterRow += 1
                c+=1
            else:
                break
        c=1
        while diskColumn + c <=6: #check right side
            if self.board[diskRow][diskColumn+c] == playerDisk:
                counterRow += 1
                c+=1
            else:
                break
        
        c=1
        while diskRow + c <=5: #checking down
            if self.board[diskRow+c][diskColumn] == playerDisk:
                counterDown +=1
                c+=1
            else:
                break

        c=1
        while 0<=diskRow-c and diskColumn+c <=6: #checking NE
            if self.board[diskRow-c][diskColumn+c] == playerDisk:
                counterSlash +=1
                c+=1
            else:
                break

        c=1
        while diskRow+c<=5 and 0<=diskColumn-c: #checking SW
            if self.board[diskRow+c][diskColumn-c]== playerDisk:
                counterSlash +=1
                c+=1
            else:
                break
        
        c=1
        while 0<=diskRow-c and 0<=diskColumn-c: #checking NW
            if self.board[diskRow-c][diskColumn-c]== playerDisk:
                counterBackslash +=1
                c+=1
            else:
                break

        c=1
        while diskRow+c<=5 and diskColumn+c<=6: #checking SE
            if self.board[diskRow+c][diskColumn+c]== playerDisk:
                counterBackslash +=1
                c+=1
            else:
                break
        return (counterRow >= 3 or counterDown >= 3 or counterSlash >= 3 or counterBackslash >= 3)
    
    def play(self):
        # game loop
        self.printBoard()

        while self.gameActive:
            playerNumber = (self.turn%2)+1
            playerDisk = self.disks[playerNumber-1]

            diskColumn = self.getPlayerInput(playerNumber)
            diskRow = self.insertChip(diskColumn, playerDisk)

            self.printBoard

            if self.checkWin(diskRow, diskColumn, playerDisk):
                print(f"Player {playerNumber} Wins!")
                self.gameActive = False
                break

            if all(val < 0 for val in self.nextRowForColumn.values()):
                print("It's a draw!")
                self.gameActive = False
                break
            
            self.turn += 1

if __name__ == "__main__":
    game = Connect4()
    game.play()