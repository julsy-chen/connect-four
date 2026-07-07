import random

MAX_COLUMN = 6
MAX_ROW = 5

class Connect4:
    def __init__(self, vsBot=False):
        # initialize state to get a new board
        self.board = [["." for _ in range(7)] for _ in range(6)]
        self.board.append(list(range(7)))
        self.nextRowForColumn = dict.fromkeys(range(7), 5)

        self.turn = 0
        self.disks = ["O", "X"]
        self.gameActive = True
        self.vsBot = vsBot
        self.botPlayerNumber = None
        self.botDisk = None
        self.humanDisk = None

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
    
    def getValidColumns(self, board=None):
        if board is None:
            board = self.board
        return [col for col in range(7) if self.nextRowForColumn[col] >= 0]

    def getPlayerInput(self, playerNumber):
        while True:
            try:
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

    def getBotInput(self):
        chosenColumn, alphabetaScore = self.alphabeta(self.board, 6, -float('inf'), float('inf'), True)
        print(f"Blitzcrank chooses column {chosenColumn}")
        return chosenColumn
    
    def getMove(self, playerNumber):
        if self.vsBot and playerNumber == self.botPlayerNumber:
            return self.getBotInput()
        else:
            return self.getPlayerInput(playerNumber)

    def checkDirection(self, board, diskRow, diskColumn, playerDisk, rowMod, columnMod):
        checkRow = diskRow+rowMod
        checkColumn = diskColumn+columnMod

        adjacentScore = 0
        while 0 <= checkColumn <= MAX_COLUMN and 0 <= checkRow <= MAX_ROW:
            if board[checkRow][checkColumn] == playerDisk:
                adjacentScore += 1
                checkRow += rowMod
                checkColumn += columnMod
            else:
                return adjacentScore            
        return adjacentScore

    def checkWin(self, board, diskRow, diskColumn, playerDisk):
        # check all directions for a win
        counterRow = 0
        counterDown = 0
        counterSlash = 0
        counterBackslash = 0

        counterRow += self.checkDirection(board, diskRow, diskColumn, playerDisk, 0, -1) # left
        counterRow += self.checkDirection(board, diskRow, diskColumn, playerDisk, 0, +1) # right
        counterDown += self.checkDirection(board, diskRow, diskColumn, playerDisk, +1, 0) # down
        counterSlash += self.checkDirection(board, diskRow, diskColumn, playerDisk, -1, +1) # NE
        counterSlash += self.checkDirection(board, diskRow, diskColumn, playerDisk, +1, -1) # SW
        counterBackslash += self.checkDirection(board, diskRow, diskColumn, playerDisk, -1, -1) # NW
        counterBackslash += self.checkDirection(board, diskRow, diskColumn, playerDisk, +1, +1) # SE
        
        return (counterRow >= 3 or counterDown >= 3 or counterSlash >= 3 or counterBackslash >= 3)
    
    def isTerminalNode(self, board):
        # Check for a win or draw
        for row in range(6):
            for col in range(7):
                if board[row][col] != ".":
                    if self.checkWin(board, row, col, board[row][col]):
                        return True
        if all(val < 0 for val in self.nextRowForColumn.values()):
            return True
        return False
    
    def getOpenRow(self, board, col):
        # Helper to find the actual open row for simulated boards
        for r in range(5, -1, -1):
            if board[r][col] == ".":
                return r
        return -1
    
    def evaluateWindow(self, window, piece):
        score = 0
        enemyPiece = self.humanDisk if piece == self.botDisk else self.botDisk

        if window.count(piece) == 4: # terminal position for the bot to win
            score += 100
        elif window.count(piece) == 3 and window.count(".") == 1: # 3 disks + an empty space
            score += 5
        elif window.count(piece) == 2 and window.count(".") == 2: # 2 disks + 2 empty spaces
            score += 2

        if window.count(enemyPiece) == 3 and window.count(".") == 1: # 3 enemy disks + an empty space (super bad for the bot)
            score -= 4

        return score

    def evaluateBoard(self, board): # function should evaluate the current board to give a score for the bot to use in decision
        # Return a tuple (None, score) to match the expected return type
        score = 0
        piece = self.botDisk

        centerArray = [board[r][3] for r in range(6)]
        centerCount = centerArray.count(piece)
        score += centerCount * 3

        # horizontal score
        for r in range(6):
            rowArray = [board[r][c] for c in range(7)]
            for c in range(4):
                window = rowArray[c:c+4]
                score += self.evaluateWindow(window, piece)
        
        # vertical score
        for c in range(7):
            colArray = [board[r][c] for r in range(6)]
            for r in range(3):
                window = colArray[r:r+4]
                score += self.evaluateWindow(window, piece)

        # positive diagonal score
        for r in range(3):
            for c in range(4):
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluateWindow(window, piece)

        # negative diagonal score
        for r in range (3):
            for c in range(4):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluateWindow(window, piece)

        return (None, score)

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        # given the current board state when the function is called
        validColumns = self.getValidColumns(board)
        isTerminal = self.isTerminalNode(board)
        
        # Base case
        if depth == 0 or isTerminal:
            if isTerminal: 
                # If maximizingPlayer is True, it means the minimizing player (human) just played and won.
                if maximizingPlayer:
                    return (None, -10000000000000)
                else:
                    return (None, 100000000000000)
            else: # Depth is zero
                return self.evaluateBoard(board)
                
        if maximizingPlayer: # maximizing player is the bot
            value = -float('inf')
            best_col = random.choice(validColumns) # Fallback
            
            for col in validColumns:
                row = self.getOpenRow(board, col)
                # MUST deep copy the 2D list so we don't ruin the real board
                boardCopy = [r.copy() for r in board]
                boardCopy[row][col] = self.botDisk
                
                # Recursive call: add [1] to extract the score from the tuple
                new_score = self.alphabeta(boardCopy, depth-1, alpha, beta, False)[1] # boardCopy is passed to the next level of recursion
                
                if new_score > value:
                    value = new_score
                    best_col = col
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                    
            return best_col, value
            
        else: # Minimizing player
            value = float('inf')
            best_col = random.choice(validColumns)
            
            for col in validColumns:
                row = self.getOpenRow(board, col)
                boardCopy = [r.copy() for r in board] 
                boardCopy[row][col] = self.humanDisk
                
                # Recursive call: add [1] to extract the score from the tuple
                new_score = self.alphabeta(boardCopy, depth-1, alpha, beta, True)[1]
                
                if new_score < value:
                    value = new_score
                    best_col = col
                    
                beta = min(beta, value)
                if alpha >= beta:
                    break
                    
            return best_col, value
        
    def chooseGameMode(self):
        while True:
            try:
                print("Choose a game mode")
                print("1) Player vs Player")
                print("2) Player vs Bot")
                gameMode = int(input("> ").strip())
                if gameMode == 1:
                    self.vsBot = False
                    self.botPlayerNumber = None
                    break
                elif gameMode == 2:
                    self.vsBot = True
                    self.choosePlayerNumber()
                    break
                else:
                    print("Invalid input, please choose 1 or 2.")
            except ValueError:
                print("Invalid input, please enter a number.")

    def choosePlayerNumber(self):
        while True:
            try:
                print("Choose your player number")
                print("1) Player 1 (O)")
                print("2) Player 2 (X)")
                playerNumber = int(input("> ").strip())
                if playerNumber == 1:
                    self.botPlayerNumber = 2
                    self.botDisk = 'X'
                    self.humanDisk = 'O'
                    break
                elif playerNumber == 2:
                    self.botPlayerNumber = 1
                    self.botDisk = 'O'
                    self.humanDisk = 'X'
                    break
                else:
                    print("Invalid input, please choose 1 or 2.")
            except ValueError:
                print("Invalid input, please enter a number.")
    
    def play(self):
        # game loop
        self.printBoard()

        while self.gameActive:
            playerNumber = (self.turn%2)+1
            playerDisk = self.disks[playerNumber-1]

            diskColumn = self.getMove(playerNumber)
            # updates & prints the game board, updates the nextRowForColumn dict, and returns the diskRow
            diskRow = self.insertChip(diskColumn, playerDisk)

            if self.checkWin(self.board, diskRow, diskColumn, playerDisk): # self.checkWin returns a boolean
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
    game.chooseGameMode()
    game.play()