import math
class Wiese_Malinowski_Rovira:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]

		
		self.legalmoves = []


	def eval_board(self, player, opp):
		board_sum = 0
		k = 1
		t = 10
		mine = 0
		theirs = 0
		for i in range(self.size):
			for j in range(self.size):
				square = self.get_square(i,j)
				if square == player:
					mult = 1
					mine += 1
				elif square == opp:
					mult = -1
					theirs += 1
				else:
					mult = 0
					
				board_sum += mult * k * math.floor(math.sqrt(((i - 3.5)**2 + (j-3.5)**2)))

		#print("Value of board: ", board_sum)
		return board_sum + t * (mine - theirs)


#prints the boards
	def PrintBoard(self):

		# Print column numbers
		print("  ",end=" ")
		for i in range(self.size):
			print(i+1,end=" ")
		print()

		# Build horizontal separator
		linestr = " " + ("+-" * self.size) + "+"

		# Print board
		for i in range(self.size):
			print(linestr)					   # Separator
			print(i+1,end="|")				   # Row number
			for j in range(self.size):
				print(self.board[i][j],end="|")  # board[i][j] and pipe separator 
			print()							  # End line
		print(linestr)

#checks every direction from the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.	
	def islegal(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		for Dir in self.directions:
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row + i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						return True
		return False
		
#returns true if the square was played, false if the move is not allowed
	def place_piece(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		
		if(player == opp):
			print("player and opponent cannot be the same")
			return False
		
		legal = False
		#for each direction, check to see if the move is legal by seeing if the adjacent square
		#in that direction is occuipied by the opponent. If it isnt check the next direction.
		#if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
		#if the chain of opponents pieces is flanked on both ends by the players pieces, flip
		#the opponents pieces 
		for Dir in self.directions:
			#look across the length of the board to see if the neighboring squares are empty,
			#held by the player, or held by the opponent
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						legal = True
						self.flip_tiles(row, col, Dir, i, player)
						break

		return legal

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
	def play_square(self, row, col, playerColor, oppColor):		
		# Place a piece of the opponent's color at (row,col)
		if (row,col) != (-1,-1):
			self.place_piece(row,col,oppColor,playerColor)
		#print("In play_square, new board is: ")
		#self.PrintBoard()
		
		# Determine best move and and return value to Matchmaker
		return self.make_move(playerColor, oppColor)

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
	def flip_tiles(self, row, col, Dir, dist, player):
		for i in range(dist):
			self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
		return True
	
#returns the value of a square on the board
	def get_square(self, row, col):
		return self.board[row][col]

	def FindMoves(self, playerColor, oppColor):
		for row in range(self.size):
			for col in range(self.size):
				if self.islegal(row, col, playerColor, oppColor):
					self.legalmoves.append((row,col))
										
		self.legalmoves = list(set(self.legalmoves))


#Search the game board for a legal move, and play the first one it finds
	def make_move(self, playerColor, oppColor):
		return MiniMaxDecision(self, playerColor, oppColor)




def copy_board(board):
	retboard = Wiese_Malinowski_Rovira()
	for row in range(board.size):
		for col in range(board.size):
			retboard.board[row][col] = board.get_square(row, col)
	return retboard



			
MAXDEPTH = 7
START = 0

def MinValue(board, player, opp, alpha, beta, depth):
	# play square, call max with new board
	# if board full or depth reached, return evaluation of board
	board.FindMoves(player, opp)
	listofmoves = board.legalmoves
	testDone = len(listofmoves)

	#print("Moves found: " , listofmoves)
	if testDone == 0:
		#print("No legal moves found")
		return board.eval_board(player, opp)

	board.FindMoves(player, opp)


	for move in board.legalmoves:

		
		newboard = copy_board(board)

		newboard.place_piece(move[0], move[1], player, opp)
		depth += 1

		#print("Depth (Min): " , depth)

		if depth > MAXDEPTH:
			val = newboard.eval_board(player, opp)
			#print("Value of board: ", val, "\tValue of beta: ", beta)
			if(val < beta):
				return val
			return beta
		
		nextval = MaxValue(newboard, opp, player, alpha, beta, depth)

		if(nextval < beta):
			beta = nextval

		if(beta <= alpha):
			return beta
		
	return beta
		
def MaxValue(board, player, opp, alpha, beta, depth):
	board.FindMoves(player, opp)
	listofmoves = board.legalmoves
	testDone = len(listofmoves)

	#print("Moves found: " , listofmoves)
	if testDone == 0:
		#print("No legal moves found")
		return board.eval_board(player, opp)

	board.FindMoves(player, opp)

	

	for move in board.legalmoves:
		newboard = copy_board(board)
		
		newboard.place_piece(move[0], move[1], player, opp)
		depth += 1

		#print("Depth (Max): " , depth)

		if depth > MAXDEPTH:
			val = newboard.eval_board(player, opp)
			if(val > alpha):
				return val
			return alpha
		
		nextval = MinValue(newboard, opp, player, alpha, beta, depth)

		if(nextval > alpha):
			alpha = nextval

		if(alpha >= beta):
			return alpha

	return alpha


def MiniMaxDecision(board, player, opp):
	maxplay = -10000	

	global START

	#print("Finding moves for: ")
	board.legalmoves = []
	
	board.FindMoves(player, opp)

	#board.PrintBoard()
	nextrow = -1
	nextcol = -1


	if len(board.legalmoves) == 0:
		print("NO LEGAL MOVES FOUND")
		
	for move in board.legalmoves:
		newboard = copy_board(board)
		
		newboard.place_piece(move[0], move[1], player, opp)

		nextplay = MinValue(newboard, opp, player, -1000, 1000, START)

		if(nextplay > maxplay):
			maxplay = nextplay

			#print("New maxplay: ", maxplay)

			nextrow = move[0]
			nextcol = move[1]
		
	#board.place_piece(nextrow, nextcol, player, opp)
	print("Returning move (", nextrow + 1, ", " , nextcol + 1, ")")
	#board.PrintBoard()
	#newboard.PrintBoard()
	
	print(board.legalmoves)
	if board.islegal(nextrow, nextcol, player, opp):
		board.place_piece(nextrow, nextcol, player, opp)
		board.PrintBoard()
		return(nextrow, nextcol)
	#board.PrintBoard()
	return (-1, -1)
