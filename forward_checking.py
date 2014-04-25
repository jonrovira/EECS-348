#!/usr/bin/env python




#------ STARTER CODE ------

import struct, string, math


class SudokuBoard:
    '''
    Game object that player manipulates 
    '''

    def __init__(self, size, board):
	    '''
	    Constructor for SudokuBoard
	    '''
	    self.BoardSize = size #the size of the board
	    self.CurrentGameboard= board #the current state of the game board

    def set_value(self, row, col, value):
    	'''
    	Creates a new SudokuBoard object with input value
    	placed on the GameBoard, row and col zero-indexed
    	'''
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added


def parse_file(filename):
    '''
    Parses a sudoku text file into a BoardSize and a 2d array
    [row, col] which holds the value of each cell. Array
    elements with a value of 0 are considered to be empty
    '''
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


def iscomplete( BoardArray ):
	"""
	Takes in an array representing a sudoku board and
	tests to see if it has been filled in correctly
	"""
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        #check that there are no 0s, or if the value of the cell
        #check if double values in row, column, or subsquare
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


def init_board( file_name ):
    """
    Creates a SudokuBoard object initialized with values from
    a text file like those found on the course website
    """
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)




#------ BACKTRACKING ALGORITHM ------

def BacktrackingSearch( sudokuboard ):
    """
    Returns a solution using a backtracking algorithm
    Returns false if no solution
    """
    return RecursiveBacktrack(sudokuboard)

checks = 0


def RecursiveBacktrack( sudokuboard ):
    """
    Backtracking algorithm
    """
    global checks
    board = sudokuboard.CurrentGameboard
    if(iscomplete( board )):
        print "Finished!" 
        print "Checks: " , checks
        PrintBoard(sudokuboard)
        return board
    
    #select unassigned variable (in board)
    size = len(board)
    subsquare = (int)(math.sqrt(size))
    nextrow = -1
    nextcol = -1
    
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                nextrow = row
                nextcol = col

    # try values at location [nextrow, nextcol] 
    for value in range(1,size+1):
#        print "Try location " , nextrow, ", " , nextcol , " with " , value
        # check if value exists in row or column
        checks += 1
#        print value
                                
#        if(checks > 1000000):
#            print "Taking too long..." 
#            PrintBoard(sudokuboard)
#            checks = 0
#            exit()
        

        test = CheckConstraints(board, nextrow, nextcol, value) 

        if(test):
            sudokuboard.set_value(nextrow,nextcol,value)
            result = RecursiveBacktrack(sudokuboard)
#            print result
            if(not result):

                sudokuboard.set_value(nextrow,nextcol,0)

            else:
                return result
            
    return False

def CheckConstraints(bd, row, col, val):

    # checks that value does not appear in row, col or the subsquare containing [row,col]
    size = len(bd)
    subsquare = (int)(math.sqrt(size))

    for i in range(size):
        if(bd[row][i] == val or bd[i][col] == val):
            return False

    SquareRow = row // subsquare
    SquareCol = col // subsquare
    # check the subsquare to see if value is already present

    for k in range(subsquare):
        for j in range(subsquare):
            if(bd[SquareRow * subsquare + k][SquareCol * subsquare + j] == val):
#                print "Value " , val, " exists in subsquare " , SquareRow, SquareCol
                return False

    return True


#------ FORWARD CHECKING ALGORITHM ------

class Empty:
	"""
	Square that hasn't been assigned a value yet
	"""
	def __init__(self, row, col):
		self.coordinate = [row, col]
		self.num_possibles = 0
		self.possibles = []

	def add_possible(self, value):
		self.possibles[self.num_possibles] = value
		self.num_possibles += 1

	def remove_possible(self, value):
		self.possibles.remove(value) # mmmm python



class List_Of_Empties:
	"""
	List of all squares that haven't been assigned values yet
	"""
	def __init__(self):
		self.list = {}

	def get_key(self, row, col):
		key = str(row) + ", " + str(col)
		return key

	def add_empty(self, row, col):
		key = self.get_key(row, col)
		if key not in self.list:
			val = Empty(row, col)
			self.list[key] = val
			return True
		else:
			return False # already in list

	def add_possible_to_empty(self, row, col, value):
		key = self.get_key(row, col)
		if key in self.list:
			self.list[key].add_possible(value)
			return True
		else:
			return False # empty not in list of empties

	def remove_possible_from_empty(self, row, col, value):
		key = self.get_key(row, col)
		if key in self.list:
			self.list[key].remove_possible(value)
			return True
		else:
			return False # empty not in list of empties

	def print_all(self):
		print "------------------"
		print "Empty squares: \n"
		for key in self.list:
			print "(" + key + ")"


def forward_checking(sudokuboard):
	"""
	Forward Checking algorithm
	"""
	board = sudokuboard.CurrentGameboard

	# Already done
	if iscomplete(board):
		print "Done!"
		PrintBoard(sudokuboard)
		return board

	size = len(board)
	subsquare = math.sqrt(size)
	loe = List_Of_Empties()

	# Find all empty squares
	for row in range(size):
		for col in range(size):
			if board[row][col] == 0:
				loe.add_empty(row, col)
	loe.print_all()

	# Assign possible values to all empty squares




#------ TESTING ------

def PrintBoard(sudokuboard):
    board = sudokuboard.CurrentGameboard
    size = len(board)
    print size
    for i in range(size):
        for j in range(size):
            print board[i][j], "\t",
            if(j == size-1):
                print ""
    print ""


print "\n-------------------------"
print "Testing backtracking\n"
b = init_board("test2.txt")
PrintBoard(b)
forward_checking(b)


