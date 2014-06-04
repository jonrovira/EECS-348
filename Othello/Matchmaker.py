import sys, imp
import string, random, time

COLORS = ['B','W']
TURN_TIME_LIMIT = 20		# seconds
CONSECUTIVE_PASS_LIMIT = 2
PAUSE_BETWEEN_MOVES = False

class Matchmaker:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
		
#prints the board
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
		
#determines the score of the board by adding +1 for every tile owned by player, and -1 for every tile owned by opp
	def score(self, player, opp):
		score = 0
		for i in range(self.size):
			for j in range(self.size):
				if(self.get_square(i,j)==player):
					score +=1
				elif(self.get_square(i,j)==opp):
					score -= 1
		return score

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


#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
	def flip_tiles(self, row, col, Dir, dist, player):
		for i in range(dist):
			self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
		return True
	
#returns the value of a square on the board
	def get_square(self, row, col):
		return self.board[row][col]

#checks all board positions to see if there is a legal move
	def has_move(self, player, opp):
		for i in range(self.size):
			for j in range(self.size):
				if self.islegal(i,j,player,opp):
					return True
		return False

#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.	
	def islegal(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		for Dir in self.directions:
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
						return True
		return False

#returns true if no square in the board contains "_", false otherwise
	def full_board(self):
		for i in range(self.size):
			for j in range(self.size):
				if(self.board[i][j]==' '):
					return False

		return True
	
#Checks to see if the given player controls the entire board
	def all_pieces(self, player):
		for i in range(self.size):
			for j in range(self.size):
				if(self.get_square(i,j) != player and self.get_square(i,j) != ' '):
					return False
		return True
				   
def main():
	# Make sure user at least attempted to specify 2 python files
	if len(sys.argv) != 3:
		print("Error: %s requires two input files." % sys.argv[0])
		print("Correct usage: python %s File1.py File2.py" % sys.argv[0])
		exit(1)

	# Instantiate matchmaker, create default board
	mm = Matchmaker()

	# Store team names from command line arguments
	teamNames = []
	teamNames.append(sys.argv[1][:-3])
	teamNames.append(sys.argv[2][:-3])

	#mm = Matchmaker()
	#teamNames = []
	#teamNames.append("TeamA")
	#teamNames.append("TeamB")
		
	# Import files from teams as modules
	# Team modules will be referred to as as Player0 and Player1
	Team0 = imp.load_source(teamNames[0], sys.argv[1])
	Team1 = imp.load_source(teamNames[1], sys.argv[2])
	
	# Instantiate Boards for each of the two teams
	# Specifically: Search object Team0 for a class with the same name
	#   as the filename, instantiate the class, and store it in players
	players = []
	players.append(getattr(Team0,teamNames[0])())
	players.append(getattr(Team1,teamNames[1])())
	
	# Randomly choose first player and begin game
	curPlayerID = random.randint(0,1)
	print("Beginning match between %s and %s." % (teamNames[0], teamNames[1]))
	mm.PrintBoard()
	print()
	
	prevMove = (-1,-1)
	consecutivePasses = 0
   
	while True:
		# Pauses game between moves
		if (PAUSE_BETWEEN_MOVES):	
			input("Paused before player %s. Hit enter." % COLORS[curPlayerID])
				
		# Clarify player colors
		playerColor = COLORS[curPlayerID]
		oppColor = COLORS[1-curPlayerID]
		
		# If neither player has a valid move, end game and score
		if (not mm.has_move(playerColor, oppColor)) and (not mm.has_move(oppColor, playerColor)):
			print("Neither player has an available move.")
			break
		# Get player's move and calculate time taken to respond
		startTime = time.time()
		move = players[curPlayerID].play_square(prevMove[0], prevMove[1], playerColor, oppColor)
		stopTime = time.time()
		
		# End game if players are stuck in a loop of playing (-1,-1)
		if move == (-1,-1):
			consecutivePasses += 1
			print("%s (%s) has passed." % (teamNames[curPlayerID], playerColor))
			print()
			mm.PrintBoard()
			print()
			
			if consecutivePasses == CONSECUTIVE_PASS_LIMIT:
				print("Available moves, but both players have passed. Game over.")
				break
			else:
				# Change player
				curPlayerID = 1 - curPlayerID
				continue

		# If player exceeded time limit, player loses
		runTime = stopTime - startTime
		if (runTime > TURN_TIME_LIMIT):
			print("%s took %.1fs to play, which exceeded the time limit (%.1fs)." %
				  (teamNames[curPlayerID], runTime, TURN_TIME_LIMIT))
			print("%s (%s) is the winner." % (teamNames[1-curPlayerID], oppColor))
			return
		# If player has returned an illegal move, player loses
		elif (not mm.islegal(move[0], move[1], playerColor, oppColor)):
			print("%s has entered an illegal move." % teamNames[curPlayerID])
			print("%s (%s) is the winner." % (teamNames[1-curPlayerID], oppColor))
			return
		
		# Valid move acquired
		print("%s (%s) places a piece at (%d,%d) in %.1fs" %
			  (teamNames[curPlayerID],playerColor, move[0]+1, move[1]+1,runTime))
		print()
			  
		mm.place_piece(move[0], move[1], playerColor, oppColor)
		prevMove = move
		consecutivePasses = 0
		
		mm.PrintBoard()
		print()
		
		# Check whether game has ended		
		if mm.all_pieces(playerColor) or mm.full_board():
			break					

		# Change player
		curPlayerID = 1 - curPlayerID

	finalScore = mm.score(COLORS[0], COLORS[1])
	if (finalScore == 0):
		print("The game is a draw.")
	elif(finalScore > 0):
		
		print("%s (%s) wins by %d pieces." % (teamNames[0],COLORS[0],finalScore))
	else:
		print("%s (%s) wins by %d pieces." % (teamNames[1],COLORS[1],-finalScore))
main()
			
