#!/Usr/bin/env python

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




#--------- BACKTRACKING ALGORITHM -----------

def BacktrackingSearch( sudokuboard ):
    """
    Returns a solution using a backtracking algorithm
    Returns false if no solution
    """
    return RecursiveBacktrack(sudokuboard)

checks1 = 0


def RecursiveBacktrack( sudokuboard ):
    """
    Backtracking algorithm
    """
    global checks1
    board = sudokuboard.CurrentGameboard
    if(iscomplete( board )):
        print "Backtracking Finished!" 
        print "Checks: " , checks1
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
        # check if value exists in row or column
        checks1 += 1
        test = CheckConstraints(board, nextrow, nextcol, value) 
        if(test):
            sudokuboard.set_value(nextrow,nextcol,value)
            result = RecursiveBacktrack(sudokuboard)
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

checks2 = 0

class Empty:
	"""
	Square that hasn't been assigned a value yet
	"""
	def __init__(self, row, col):
		self.coordinate = [row, col]
		self.num_possibles = 0
		self.possibles = []

	def add_possible(self, value):
		self.possibles.append(value)
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

	def get_possibles(self, row, col):
		key = self.get_key(row, col)
		return self.list[key].possibles

	def add_empty(self, row, col):
		key = self.get_key(row, col)
		if key not in self.list:
			val = Empty(row, col)
			self.list[key] = val
			return True
		else:
			return False # already in list

	def remove_empty(self, row, col):
		key = self.get_key(row, col)
		if key in self.list:
			self.list.remove(key)
		else:
			return False # not in list

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

	def find_first_empty(self, board, size):
		row = 0
		col = 0
		while True:
			if board[row][col] == 0:
				return [row, col]
			elif col < size-1:
				col += 1
			elif row < size-1:
				row += 1
				col = 0
			else:
				return False


	def calculate_possibles(self, board, size):
		# For each empty square
		for e in self.list.values():

			# Initialize possibles to all values
			possibles = []
			for i in range(1, size+1):
				possibles.append(i)

			# Square's coordinates
			row = e.coordinate[0]
			col = e.coordinate[1]
			subsquare = (int)(math.sqrt(size))
			squareRow = row // subsquare
			squareCol = col // subsquare

			# Remove possible values that appear in same row
			for col_i in range(0, size):
				val = board[row][col_i]
				if val != 0 and col_i != col:
					if val in possibles:
						possibles.remove(val)

			# Remove possible values that appear in same column
			for row_i in range(0, size):
				val = board[row_i][col]
				if val != 0 and row_i != row:
					if val in possibles:
						possibles.remove(val)

			# Remove possible values that appear in same subsquare
			for x in range(subsquare):
				for y in range(subsquare):
					val = board[squareRow * subsquare + x][squareCol * subsquare + y]
					if val in possibles:
						possibles.remove(val)

			# Add possible values to empty squares
			if possibles:
				for p in possibles:
					self.add_possible_to_empty(row, col, p)
			else:
				return False # No possibles

		return True

	def print_all(self):
		print "------------------"
		print "Empty squares: \n"
		for key in self.list:
			print "(" + key + ")"


def forwardCheckConstraints(board, size, row, col, val):
	# Assign value to square
	board[row][col] = val

	# Find all empty squares
	loe = List_Of_Empties()
	for row in range(size):
		for col in range(size):
			if board[row][col] == 0:
				loe.add_empty(row, col)

	# Determine if assignment yields possibilities for rest of empties
	valid = loe.calculate_possibles(board, size)
	if valid:
		return True
	else:
		return False



def forward_checking(sudokuboard):
	"""
	Forward Checking algorithm
	"""
	global checks2

	# Check if complete
	board = sudokuboard.CurrentGameboard
	if iscomplete(board):
		print "Forward Checking Finished!"
		print "Checks: ", checks2
		PrintBoard(sudokuboard)
		return board

	# Value initializations
	size = len(board)
	subsquare = (int)(math.sqrt(size))

	# Find all empty squares
	loe = List_Of_Empties()
	for row in range(size):
		for col in range(size):
			if board[row][col] == 0:
				loe.add_empty(row, col)

	# Find all possible values or each empty square
	loe.calculate_possibles(board, size)

	# Start with first empty square
	first_empty = loe.find_first_empty(board, size)
	nextrow = first_empty[0]
	nextcol = first_empty[1]
	key = loe.get_key(nextrow, nextcol)
	empty = loe.list[key]

	# Try a value for that square out of the possibles
	for value in empty.possibles:
		checks2 += 1
		test = forwardCheckConstraints(board, size, nextrow, nextcol, value)

		# If that value is valid, assign it
		if(test):
			sudokuboard.set_value(nextrow, nextcol, value)
			result = forward_checking(sudokuboard)

			# Next level down doesn't work, revert square to 0
			if not result:
				sudokuboard.set_value(nextrow, nextcol, 0)

			# Next level down works, return
			else:
				return result
		else:
			board[nextrow][nextcol] = 0

	# No values work for the square
	return False




#------------- Minimum Remaining Values + Most Constraining Variable ---------


# Go through all cells, create lists of all possible values empty cells can take
# Determine the cell with the fewest possiblilties, assign each in turn
# - If tie:
# figure out which has the most blank squares in its row+col+subsquare

checks3 = 0

def MRV_MCV(sudokuboard):

    global checks3

    # Check if complete
    board = sudokuboard.CurrentGameboard
    if iscomplete(board):
        print "MRV_MCV Finished!"
        print "Checks: ", checks3
        PrintBoard(sudokuboard)
        return board


 
    # Value initializations
    size = len(board)
    subsquare = (int)(math.sqrt(size))
    nextrow = -1
    nextcol = -1
    
    # Find all empty squares
    loe = List_Of_Empties()
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                loe.add_empty(row, col)
                
    # Find all possible values for each empty square
    loe.calculate_possibles(board, size)

    rem = size

    minVals = []

    # Finds cells with least remaining values
    
    for cell in loe.list:
        if(len(loe.list[cell].possibles) < rem):
            rem = len(loe.list[cell].possibles)

    for cell in loe.list:
        if(len(loe.list[cell].possibles) == rem):
            minVals.append(loe.list[cell])
    
    nextrow = -1
    nextcol = -1

    if(len(minVals) == 1):
        # No tie-breaker needed
        nextrow = minVals[0].coordinate[0]
        nextcol = minVals[0].coordinate[1]
        #nextcell = minValues[0]
    else:
        # Need to use MCV to determine what next cell is
        tmprow = -1
        tmpcol = -1

        maxcount = -1

        # Calculate the most constraining variable as the cell influencing the most empty cells in its row, column and subsquare
        # (most cells equal to 0)

        for cell in minVals:
            count = 0
            tmprow = cell.coordinate[0]
            tmpcol = cell.coordinate[1]
            for i in range(size):
                if(board[tmprow][i] == 0):
                    count += 1
                if(board[i][tmpcol] == 0):
                    count += 1


            SquareRow = tmprow // subsquare
            SquareCol = tmpcol // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if(board[SquareRow*subsquare + i][SquareCol*subsquare + j] == 0):
                        count += 1
            if(count > maxcount):
                maxcount = count
                nextrow = tmprow
                nextcol = tmpcol
                #nextcell = cell

    # should have the cell with minimum remaining values and most constrained

    key = loe.get_key(nextrow, nextcol)
    next = loe.list[key]

    
    for value in next.possibles:
        sudokuboard.set_value(nextrow, nextcol, value)
        checks3 += 1

        result = MRV_MCV(sudokuboard)

        if(not result):
            sudokuboard.set_value(nextrow, nextcol, 0)
        else:
            return result
            
        
    return False





#----------------MRV+MCV+LCV---------------------

checks4 = 0

def MRV_MCV_LCV(sudokuboard):

    global checks4

    # Check if complete
    board = sudokuboard.CurrentGameboard
    if iscomplete(board):
        print "MRV+MCV+LCV Finished!"
        print "Checks: ", checks4
        PrintBoard(sudokuboard)
        return board


 
    # Value initializations
    size = len(board)
    subsquare = (int)(math.sqrt(size))
    nextrow = -1
    nextcol = -1
    
    # Find all empty squares
    loe = List_Of_Empties()
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                loe.add_empty(row, col)
                
    # Find all possible values for each empty square
    loe.calculate_possibles(board, size)

    rem = size

    minVals = []

    # Finds cells with least remaining values
    
    for cell in loe.list:
        if(len(loe.list[cell].possibles) < rem):
            rem = len(loe.list[cell].possibles)

    for cell in loe.list:
        if(len(loe.list[cell].possibles) == rem):
            minVals.append(loe.list[cell])
    
    nextrow = -1
    nextcol = -1

    if(len(minVals) == 1):
        # No tie-breaker needed
        nextrow = minVals[0].coordinate[0]
        nextcol = minVals[0].coordinate[1]
        #nextcell = minValues[0]
    else:
        # Need to use MCV to determine what next cell is
        tmprow = -1
        tmpcol = -1

        maxcount = -1

        # Calculate the most constraining variable as the cell influencing the most empty cells in its row, column and subsquare
        # (most cells equal to 0)

        for cell in minVals:
            count = 0
            tmprow = cell.coordinate[0]
            tmpcol = cell.coordinate[1]
            for i in range(size):
                if(board[tmprow][i] == 0):
                    count += 1
                if(board[i][tmpcol] == 0):
                    count += 1


            SquareRow = tmprow // subsquare
            SquareCol = tmpcol // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if(board[SquareRow*subsquare + i][SquareCol*subsquare + j] == 0):
                        count += 1
            if(count > maxcount):
                maxcount = count
                nextrow = tmprow
                nextcol = tmpcol
                #nextcell = cell

    # should have the cell with minimum remaining values and most constrained

    key = loe.get_key(nextrow, nextcol)
    next = loe.list[key]


    # Have cell we want
    # Get list of possible values for the cell
    # Count number of times each value appears in the lists of possible values of the cells in the row/col/subsquare 


    lop = next.possibles
    if (lop == []):
        return False
    app = {}
    for i in lop:
        app[i] = 0
        for j in range(size):
            if(j != nextcol and board[nextrow][j] == 0):
                tmpkey = loe.get_key(nextrow, j)
                tmp = loe.list[tmpkey]
                for k in tmp.possibles:
                    if k == i:
                        app[i] += 1

            if(j != nextrow and board[j][nextcol] == 0):
                tmpkey = loe.get_key(j, nextcol)
                tmp = loe.list[tmpkey]
                
                for k in tmp.possibles:
                    if k == i:
                        app[i] += 1

            SquareRow = nextrow // subsquare
            SquareCol = nextcol // subsquare
            for y in range(subsquare):
                for z in range(subsquare):
                    if(board[SquareRow*subsquare + y][SquareCol*subsquare + z] == 0):
                        tmpkey = loe.get_key(SquareRow * subsquare + y, SquareCol * subsquare + z)
                        tmp = loe.list[tmpkey]
                        for a in tmp.possibles:
                            if (a == i and SquareRow * subsquare + y != nextrow and SquareCol * subsquare + z != nextcol):
                                app[i] += 1


    cont = True
    while(cont):
        minapp = size * size
        for key in app:
            if(app[key] < minapp):
                minapp = app[key]
                usekey = key

        if(minapp == size * size):
            return False

        
        sudokuboard.set_value(nextrow, nextcol, usekey)
        
        checks4 += 1

        del app[usekey]
        
        result = MRV_MCV_LCV(sudokuboard)
        
        

        if(not result):
            cont = True
            sudokuboard.set_value(nextrow, nextcol, 0)
            if(app == {}):
                return False
        else:
            return result
        
    return False





#------ TESTING ------

def PrintBoard(sudokuboard):
    board = sudokuboard.CurrentGameboard
    size = len(board)
    for i in range(size):
        for j in range(size):
            print board[i][j],
            if(size != 25):
                print "\t",
            if(j == size-1):
                print ""
    print ""

'''
print "\n-------------------------"
print "Testing forward checking\n"
b = init_board("test2.txt")
PrintBoard(b)
print forward_checking(b)



print "\n--------------------------"
print "Testing MRV_MCV_LCV\n"
d = init_board("test25x25.txt")
PrintBoard(d)
MRV_MCV_LCV(d)


print "\n-------------------"
print "Testing MRV_MCV\n"
c = init_board("test25x25.txt")
MRV_MCV(c)
'''


def TestSolvers(filename):

    test = init_board(filename)
    print "Solving Board: \n"
    PrintBoard(test)
    global checks

    board = test.CurrentGameboard
    
    if(len(board) < 16):
        
        BacktrackingSearch(test)

        test = init_board(filename)
        forward_checking(test)


    else:
        print "Size bigger than 16, backtracking and forward checking not run\n"


    test = init_board(filename)
    MRV_MCV(test)

    test = init_board(filename)
    MRV_MCV_LCV(test)


TestSolvers("test4x4.txt")
TestSolvers("test9x9.txt")
TestSolvers("test16x16.txt")
TestSolvers("test25x25.txt")
