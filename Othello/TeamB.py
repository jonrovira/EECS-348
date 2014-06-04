
class TeamB:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]

#prints the boards
	def PrintBoard(self):

		# Print column numbers
		print("  ",end="")
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

#Search the game board for a legal move, and play the first one it finds
	def make_move(self, playerColor, oppColor):
		for row in range(self.size):
			for col in range(self.size):
				if(self.islegal(row,col,playerColor, oppColor)):
					for Dir in self.directions:
						#look across the length of the board to see if the neighboring squares are empty,
						#held by the player, or held by the opponent
						for i in range(self.size):
							if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
								#does the adjacent square in direction dir belong to the opponent?
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= oppColor and i==1 : # no
									#no pieces will be flipped in this direction, so skip it
									break
								#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
								#of opponent pieces
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
									break

								#with one of player's pieces at the other end
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])==playerColor and i!=0 and i!=1 :
									#set a flag so we know that the move was legal
									legal = True
									self.flip_tiles(row, col, Dir, i, playerColor)
									break
					return (row,col)
		return (-1,-1)
