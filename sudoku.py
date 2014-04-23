#!/usr/bin/env python
import struct, string, math

#this will be the game object your player will manipulate
class SudokuBoard:

    #the constructor for the SudokuBoard
    def __init__(self, size, board):
      self.BoardSize = size #the size of the board
      self.CurrentGameboard= board #the current state of the game board

    #This function will create a new sudoku board object with
    #with the input value placed on the GameBoard row and col are
    #both zero-indexed
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added
    


# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements witha value of 0 are considered to be empty

def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    



#takes in an array representing a sudoku board and tests to
#see if it has been filled in correctly
def iscomplete( BoardArray ):
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        #check each cell on the board for a 0, or if the value of the cell
        #is present elsewhere within the same row, column, or square
        for row in range(size):
            for col in range(size):

                if BoardArray[row][col]==0:
                    return False
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                           and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                            return False
        return True

# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

#---------------------------------------------------------------------------------------------------------------#

# Backtracking Algorithm (in slides pretty much?)

# returns a solution, or false
def BacktrackingSearch( sudokuboard ):
    return RecursiveBacktrack(sudokuboard)

checks = 0

# returns a solution or false
def RecursiveBacktrack( sudokuboard ): 
    global checks
    board = sudokuboard.CurrentGameboard
    if(iscomplete( board )):
        return board
    
    #select unassigned variable (in board)
    size = len(board)
    subsquare = (int)(math.sqrt(size))
    
    for row in range(size):
        for col in range(size):

            if board[row][col] == 0:
                nextrow = row
                nextcol = col
    
    # try values at location [nextrow, nextcol] 
    for value in range(1,size+1):
#        print "Try location " , nextrow, ", " , nextcol , " with " , value
        test = True
        # check if value exists in row or column
        checks += 1
        for i in range(size):

            if(value == board[nextrow][i] or value == board[i][nextcol]):
                test = False
 #               print "Already exists in row or column"
                
            
            
        if(test):
            for i in range(size):
                # check the row and column of the selected entry to see if value already exists
                SquareRow = nextrow // subsquare
                SquareCol = nextcol // subsquare
                # check the subsquare to see if value is already present
                for k in range(subsquare):
                    for j in range(subsquare):
                        if((board[SquareRow*subsquare + k][SquareCol*subsquare + j] == value)
                           and (SquareRow*subsquare + k != row) and (SquareCol*subsquare + j != col)):
#                            print "Value " ,value ,  " exists"
                            test = False

                # if not present in either column/row or subsquare, add value to the assignment
                if(test):
                    #board[nextrow][nextcol] = value

                    sudokuboard.set_value(nextrow,nextcol,value)
  #                  PrintBoard(sudokuboard)
                    if(checks > 300000):
                        print "Taking too long..." 
                        PrintBoard(sudokuboard)
                        exit()

                    result = RecursiveBacktrack(sudokuboard)
                    if(result != False):
                        print "Number of checks: ", checks
                        PrintBoard(sudokuboard)
                        return result
                    sudokuboard.set_value(nextrow, nextcol, 0)
                
                if(checks > 300000):
                    print "Taking too long..." 
                    PrintBoard(sudokuboard)
                    exit()
                    
    return False
                        


#--------------------TESTING------------------#

def PrintBoard(sudokuboard):
    board = sudokuboard.CurrentGameboard
    size = len(board)
    for i in range(size):
        for j in range(size):
            print board[i][j],
            if(j == size-1):
                print ""
    print ""


sb = init_board("test1.txt")

b = init_board("test3.txt")

print "Testing backtracking"

PrintBoard(sb)

BacktrackingSearch(sb)

PrintBoard(b)

BacktrackingSearch(b)

# Forward Checking



# Minimum Remaining Values


