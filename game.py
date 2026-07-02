gameBoard = [["." for _ in range(7)] for _ in range(6)]
gameBoard.append(list(range(7)))

rowDetermine = dict.fromkeys(range(7), 5)

print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in gameBoard]))

turn = 0
disks = ["O", "X"]

diskColumn = 0
diskRow = 0

game=True

def insertChip(column, playerDisk):
    global diskColumn
    global diskRow
    diskColumn = column
    diskRow = rowDetermine[column]
    rowDetermine[column]-=1
    gameBoard[diskRow][diskColumn] = playerDisk

while game: #game loop
    playerNumber = str((turn%2)+1)
    playerDisk = disks[int(playerNumber)-1]
    playerInput = int(input("Player " + playerNumber + "'s move: "))
    insertChip(playerInput, playerDisk) # --> updated the game board + set row and column that the disk has fallen into
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
        print("Player " + playerNumber + " Wins!")
        break

    turn +=1