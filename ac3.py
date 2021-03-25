# reader able to test and change the board
#

#Guides:
  #  * you want to play yours or defualt one
  #  1) enter row by row
  #  2) kdgkldg
  #  3) lkdgd
  #  4) FYI, 0 means empty cell


# 9x9 board:
board = [
        [0,0,0,0,0,0,0,2,0],
        [7,0,0,0,0,2,6,0,0],
        [0,4,6,0,8,3,1,0,0],
        [0,7,5,0,1,0,0,0,0],
        [0,0,1,9,7,8,2,0,0],
        [0,0,0,0,3,0,4,1,0],
        [0,0,7,4,2,0,8,3,0],
        [0,0,4,8,0,0,0,0,5],
        [0,6,0,0,0,0,0,0,0],
]

def constraints(x,y,z):
    #there is three constraints row, column and square should be uniqe value in each.

    # 1st: skip if prefilled
    val = board[x][y] #pick a cell
    if val != 0: # if not zero means, prefilled value so skip return false
        return False

    # 2nd: check if it in the rows
    if z in board[x]:
        return False

    # 3rd: check if its in columns.
    for row in board:
        if z == row[y]:
            return False

    # 4th: check 3x3 square.
    Root_x = x - x % 3
    Root_y = y - y % 3

    for rx in range(Root_x,Root_x+3):
        for ry in range(Root_y,Root_y+3):
            if z == board[rx][ry]:
                return False

    # 5th: finally, return true when the value fit which not violate the constraints.
    return True


# 6th: preprocessing method. AC3      # 7 , 4 , 6 , 2 --> [1, 3, 5, 8, 9]
#                                     # 2  ,  3  , 8 remove it from domain (0,5) --> [1,4,5,6,7,9]
def AC3(x,y):# preprocessing.

    possible_value_for_cell = []
    for i in range(1,10): # (1,10), 1,2,3,4,5,6,7,8,9

        if constraints(x,y,i):
            possible_value_for_cell.append(i)

    return possible_value_for_cell


# 7th: display the game board.
def display():
    sudoku_board = np.array(board)
    print(sudoku_board)


# Test:
print(constraints(3,3,2))
print(constraints(0,0,4))
print(constraints(0,0,2))

# preprocess function:
print(AC3(0,5)) # elimanite


display()
