gameBoard = [["." for _ in range(7)] for _ in range(6)]
gameBoard.append(list(range(7)))

nextRowForColumnMap = dict.fromkeys(range(7), 5)

print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in gameBoard]))

turn = 0
disks = ["O", "X"]

diskColumn = 0
diskRow = 0

game=True

# input: column that we want to insert, player putting disk
# output: diskRow
def insertChip(column, playerDisk):
    # find row for where the disk falls to
    diskRow = nextRowForColumnMap[column]
    # update nextRowForColumnMap
    nextRowForColumnMap[column]-=1
    # update gameBoard
    gameBoard[diskRow][column] = playerDisk
    # output the row that the playerDisk has fallen to
    return diskRow

def playerInput(playerNumber):
    while True:
        try:
            # get player input
            givenInput = int(input(f"Player {playerNumber}'s move: "))

            if 0 <= givenInput <= 6:
                return givenInput # Valid input exits the function immediately
            else:
                print(f"You dropped your disk outside of the gameboard, silly guy! Try again, choosing a number between 0 and 6.")
                
        except ValueError:
            print("You seem a bit confused, try again, choosing a number between 0 and 6.")

while game: #game loop
    playerNumber = (turn%2)+1
    playerDisk = disks[int(playerNumber)-1]
    diskColumn = playerInput(playerNumber)
    diskRow = insertChip(diskColumn, playerDisk) # --> updated the game board + set row and column that the disk has fallen into
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in gameBoard]))

    c = 1
    counterRow = 0
    counterDown = 0
    counterSlash = 0
    counterBackslash = 0

    while 0<=diskColumn - c: #check left side
        if gameBoard[diskRow][diskColumn-c] == playerDisk:
            counterRow += 1
            c+=1
        else:
            break
    c=1
    while diskColumn + c <=6: #check right side
        if gameBoard[diskRow][diskColumn+c] == playerDisk:
            counterRow += 1
            c+=1
        else:
            break
    
    c=1
    while diskRow + c <=5: #checking down
        if gameBoard[diskRow+c][diskColumn] == playerDisk:
            counterDown +=1
            c+=1
        else:
            break

    c=1
    while 0<=diskRow-c and diskColumn+c <=6: #checking NE
        if gameBoard[diskRow-c][diskColumn+c] == playerDisk:
            counterSlash +=1
            c+=1
        else:
            break

    c=1
    while diskRow+c<=5 and 0<=diskColumn-c: #checking SW
        if gameBoard[diskRow+c][diskColumn-c]== playerDisk:
            counterSlash +=1
            c+=1
        else:
            break
    
    c=1
    while 0<=diskRow-c and 0<=diskColumn-c: #checking NW
        if gameBoard[diskRow-c][diskColumn-c]== playerDisk:
            counterBackslash +=1
            c+=1
        else:
            break

    c=1
    while diskRow+c<=5 and diskColumn+c<=6: #checking SE
        if gameBoard[diskRow+c][diskColumn+c]== playerDisk:
            counterBackslash +=1
            c+=1
        else:
            break

    if counterRow >= 3 or counterDown >= 3 or counterSlash >= 3 or counterBackslash >= 3:
        print(f"Player {playerNumber} Wins!")
        break

    turn +=1