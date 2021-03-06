import struct, string

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def PrintBoard(self):
        print "\n"
        print(self.board[0][0] + " | " + self.board[1][0] + " | " + self.board[2][0])
        
        print(self.board[0][1] + " | " + self.board[1][1] + " | " + self.board[2][1])
        
        print(self.board[0][2] + " | " + self.board[1][2] + " | " + self.board[2][2])
        print "\n"
    def play_square(self, col, row, val):
        self.board[col][row] = val

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]
        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] and self.board[0][0]==self.board[2][2] ):
            return self.board[0][0]
        if(self.board[2][0]!='N' and self.board[2][0] == self.board[1][1] and self.board[2][0]==self.board[0][2]):
            return self.board[2][0]
        return 'N'

def make_simple_cpu_move(board, cpuval):
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j)=='N'):
                board.play_square(i,j,cpuval)
                return True
    return False




def MiniMaxDecision(board, player):
    maxplay = -10
    nextrow = -1
    nextcol = -1
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j) == 'N'):

                board.play_square(i, j, player)

                if(player == 'X'):
                    nextplayer = 'O'
                else:
                    nextplayer = 'X'

                nextplay = MinValue(board, nextplayer, -10, 10)
                
                if(nextplay > maxplay):
                    maxplay = nextplay
                    
                    nextrow = i
                    nextcol = j
#                    print "Updated next play (max): ", i, ' ', j
                board.play_square(i, j, 'N')
    '''
    if(maxplay == 1):
        print "I am going to win"
    elif(maxplay == 0):
        print "Playing to tie"
    else:
        print "Shit"
    '''


    board.play_square(nextrow, nextcol, player)


def MinValue(board, player, alpha, beta):

    testDone = board.winner()
    if testDone == player:
        return -1
    elif testDone != 'N':
        return 1
    elif board.full_board():
        return 0

#    minval = 10
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j) == 'N'):

                board.play_square(i, j, player)

                if(player == 'X'):
                    nextplayer = 'O'
                else:
                    nextplayer = 'X'

                nextval = MaxValue(board, nextplayer, alpha, beta)

                board.play_square(i,j,'N')


                if(nextval < beta):
                    beta = nextval
                    
                
                if(beta <= alpha):
#                    print "Alpha: ", alpha, "\tnextval: ", nextval
                    return beta
    
    return beta

        
def MaxValue(board, player, alpha, beta):

    testDone = board.winner()
    if testDone == player:
        return 1
    elif testDone != 'N':
        return -1
    elif board.full_board():
        return 0


#    maxval = -10
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j) == 'N'):
                board.play_square(i, j, player)

                if(player == 'X'):
                    nextplayer = 'O'
                else:
                    nextplayer = 'X'

                nextval = MinValue(board, nextplayer, alpha, beta)
                board.play_square(i,j,'N')                                
                

                if(nextval > alpha):
                    alpha = nextval
                 

                if(alpha >=  beta):
 #                   print "Beta: ", beta, "\tnextval: ", nextval
                    return alpha
                   
                                    

    return alpha



def play():
    
    print "Enter 1 to go first, enter 0 to let computer go first"    

    turn = int(input())

    if(turn == 1):
        humanval = 'X'
        cpuval = 'O'
    else:
        cpuval = 'X'
        humanval = 'O'

    Board = TicTacToeBoard()
#    humanval =  'X'
#   cpuval = 'O'
    Board.PrintBoard()

 
    if(turn == 0):
        print("CPU Move")
        MiniMaxDecision(Board, cpuval)
        Board.PrintBoard()

    

    while( Board.full_board()==False and Board.winner() == 'N'):

        print("your move, pick a row (0-2)")
        row = int(input())
        print("your move, pick a col (0-2)")
        col = int(input())

        if(Board.get_square(col,row)!='N'):
            print("square already taken!")
            continue
        else:
            Board.play_square(col,row,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                Board.PrintBoard()
                print("CPU Move")
                # make_simple_cpu_move(Board,cpuval)
                MiniMaxDecision(Board, cpuval)
                Board.PrintBoard()

    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("Cat game")
    elif(Board.winner()==humanval):
        print("You Win!")
    elif(Board.winner()==cpuval):
        print("CPU Wins!")

    print "1 to play again, 0 to exit"
    again = int(input())


    if(again):
        play()

def main():
    play()

main()
