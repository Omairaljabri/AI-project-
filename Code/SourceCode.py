import numpy as np
import time


# ---------------------------------------------- 9x9 board -------------------------------------------------------

#board = [
#        [0,7,0,0,0,0,4,0,0],
#        [0,0,0,4,0,0,5,0,3],
#        [0,4,0,0,0,0,0,0,0],
#        [0,2,0,0,0,3,0,0,4],
#        [0,0,4,0,0,0,9,0,0],
#        [0,0,0,0,5,0,0,6,0],
#        [0,3,2,0,9,1,0,7,8],
#        [6,8,0,0,0,2,1,0,0],
#        [0,0,0,8,0,6,0,0,0],       
#]

board = [
        [0,0,0,0,0,0,0,2,0],
        [7,0,0,0,0,2,6,0,0],
        [0,4,6,0,8,3,1,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,9,7,8,2,0,0],
        [0,0,0,0,3,0,4,1,0],
        [0,0,7,8,2,0,8,3,0],
        [0,0,4,8,0,0,0,0,5],
        [0,6,0,0,0,0,0,0,0],       
]

new_domains_AC3 = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],       
]

# ------------------------------------------------ Display -------------------------------------------------------

# 7th: display the game board.    
def display():
    print('Sudoku puzzle board:')
    sudoku_board = np.array(board)
    print(sudoku_board)

# ---------------------------------------------- Constraints -----------------------------------------------------

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
        
# ----------------------------------------------- Eliminate -------------------------------------------------------

# 6th: preprocessing method. AC3       7 , 4 , 6 , 2 --> [1, 3, 5, 8, 9]
#                                      2  ,  3  , 8 remove it from domain (0,5) --> [1,4,5,6,7,9]
def eliminate(x,y):# preprocessing or elimaniate.
    
    possible_value_for_cell = []
    for i in range(1,10): # (1,10), 1,2,3,4,5,6,7,8,9
        if constraints(x,y,i): # 1st time => (0,0,1) , 2nd times => (0,0,2) .. etc.
            possible_value_for_cell.append(i) 
    
    # now, possible_value_for_cell = [1, 3, 5, 8, 9]
    
    new_domains_AC3[x][y] = possible_value_for_cell # [1, 3, 5, 8, 9]
    return new_domains_AC3[x][y]

# ------------------------------------------------- AC-3 ---------------------------------------------------------

def AC3():
    print('\nif domain empty [] that means prefilled already.\n\nArc consistency (AC-3) reducing domains..')
    for x in range(9):
        for y in range(9):
            print('cell({1},{2}) domain after applied AC-3 {0}'.format(eliminate(x,y),x,y))
            
# ------------------------------------------------ bootup -------------------------------------------------------

def bootup():
    print('\nWelcome To Sudoku game:')
    print('1) print all domains after applied AC-3.')
    print('2) a domain for a specific cell after applied AC-3.\n')
    try:
        i = int(input('Choose between 1 or 2: '))
        if i == 1:
            AC3()# Applied Arc consistency to all cells.
        if i == 2:
            x = int(input('Enter row number: ')) # 1
            y = int(input('Enter column number: ')) # 0   
        if eliminate(x,y) == []: # Here, i mean if the cell given already prefilled then output the below print.
            print('\nThis cell already prefilled.')
        else: # otherwise, print the domain for the given cell. 
            print('\n domain for cell({1},{2}): {0} '.format(eliminate(x,y),x,y))
    except: # if wrong input happend such as excpect int came str or different datatype or even Null.
            print('\nSorry, wrong input')
 
# ------------------------------------------------- BT ---------------------------------------------------------

def BT(): # to solve ...
    flag = None
    
    for i in range(len(board)):
        for j in range(len(board[0])): 
            if board[i][j] == 0: 
                find_row = i
                find_col = j
                flag = True
                
    if not flag:
        return True  
    else:
        for k in range(1,10): # domain (1-9)
            if constraints(find_row,find_col,k): 
                board[find_row][find_col] = k 
                
                if BT():
                    return True 
                
                board[find_row][find_col] = 0
        
        return False 

# ------------------------------------------------- BT-AC ---------------------------------------------------------

def BT_AC():
    flag = None
     
    for i in range(len(board)):
        for j in range(len(board[0])): 
            if board[i][j] == 0:
                find_row = i
                find_col = j
                flag = True  
                
    if not flag: 
        return True 
    else:
        for k in new_domains_AC3[find_row][find_col]: # [1,3,5]
            if constraints(find_row,find_col,k):
                board[find_row][find_col] = k

                if BT():
                    return True 

                board[find_row][find_col] = 0

        return False   

# ------------------------------------------------- Performance ----------------------------------------------------------

StartTime = time.time()
AC3() 
EndTime = time.time()
print("Time taken to solve Sudoku board with Backtracking and AC-3 %f" % (EndTime - StartTime))

StartTime = time.time()
BT() 
EndTime = time.time()
print("Time taken to solve Sudoku board with Backtracking and AC-3 %f" % (EndTime - StartTime))

StartTime = time.time()
BT_AC() 
EndTime = time.time()
print("Time taken to solve Sudoku board with Backtracking and AC-3 %f" % (EndTime - StartTime))

# ----------------------------------------------------------------------------------------------------------------
   
