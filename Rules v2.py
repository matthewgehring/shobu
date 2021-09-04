# README
#  Board coordinates respond to list index follows:
#   0  1  2  3      16 17 18 19
#   4  5  6  7      20 21 22 23
#   8  9  10 11     24 25 26 27
#   12 13 14 15     28 29 30 31
#
#   32 33 34 35     48 49 50 51
#   36 37 38 39     52 53 54 55
#   40 41 42 43     56 57 58 59
#   44 45 46 47     60 61 62 63
#
#   Thus, the movement vector for moving vertically up 1 space would be -4, for moving to the right +1, to the left -1, etc.
#   input1 is the initial passive stone coordinate, input2 is the passive stones desired location, and input3 is the aggressive stone coordinate.
#   'b' is a black stone, 'w' is a white stone, 'x' is an empty space. x is a placeholder, it looks really ugly as a space.
board = 'bbbb' \
        'xxxx' \
        'xxxx' \
        'wwww' \
    \
        'bbbb' \
        'xxxx' \
        'xxxx' \
        'wwww' \
    \
        'bbbb' \
        'xxxx' \
        'xxxx' \
        'wwww' \
    \
        'bbbb' \
        'xxxx' \
        'xxxx' \
        'wwww'
board = list(board)
class Rules(object):
    def __init__(self, board):
        self.board = board
        self.two_space_moves=(10,-10,8,-8,6,-6,4,-4)
        self.one_space_moves=(5,-5,4,-4,3,-3,2,-2)

    def initialize_homeboard(self, color):
        if color == "b":
            homeboard = (0, 1)
        if color == "w":
            homeboard = (2, 3)
        return homeboard

    def check_if_valid(self, input1, input2, color):
        invertboard = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        invertmoves = {1: 4, -1: -4, 5: 5, -5: -5, 4: 1, -4: -1, -3: 3, 3: -3, 2: 8, -2: -8, 10: 10, -10: -10, 8: 2,
                       -8: -2, -6: 6, 6: -6}            # dictionary mapping coordinates to an inverted matrix to detect move legality
        valid_moves = (1, -1, 5, -5, 4, -4, 3, -3, 2, -2, 10, -10, 8, -8, 6, -6, 4, -4)     #all valid movement vectors

        if board[input1] != color:      #must select your own color stone
            return False
        if input1 // 16 != input2 // 16:        #floor division to see if both inputs are in 4x4 grids
            print('input1 and input2 not on same subboard')
            return False

        input1 = input1 % 16
        input2 = input2 % 16
        move = input2 % 16 - input1 % 16

        if move not in valid_moves:     #detects if illegal move like a knights move, or something
            return False

        if move > 0 and (input1 + move) % 16 < input1:  #if in valid moves, checks if goes off the board for top and bottom edges
            return False

        if (invertboard[input1 % 16]+ invertmoves[move]) % 16 < invertboard[input2 % 16]:   #checks if goes off the board for left and right edges
            return False

        if move < 0 and (input1 + move) % 16 > input1:
            return False

        if (invertboard[input1 % 16]+ invertmoves[move]) % 16 > invertboard[input2 % 16]:
            print('check 5')
            return False

        else:
            return True

    def check_if_pushes(self,input1,input2,color):          #checks if a stone is being pushed, returns the location of the stone being pushed
        move = input2 - input1
        # print(board)
        # print(board[input2])
        if move in self.two_space_moves:
            if (board[int(input1+move/2)] != 'x' and board[input2]=='x'):
                return input1+move/2    #if stone moves past another stone, returns location of the stone being jumped over

            if board[int(input1 + move / 2)] == 'x' and board[input2] != 'x':
                return input2           # if stone moves onto other stone, returns location of stone being moved onto

            if (board[int(input1+move/2)] != 'x' and board[input2]!='x'):
                return False            # if move both jumps over a stone and lands on a stone, returns false

        if move in self.one_space_moves:
            if board[input2] !='x' and board[input2 + move] == 'x': #checks if one space move lands on enemy stone
                return input2

        return 'x'      #shows nothing has been pushed

    def passive_move(self,input1,input2,color):
        subboard=self.initialize_homeboard(color)
        if board[input1] != color or board[input2] != 'x':  #checks if you select your own color or if you push another stone
            return False
        if input1 // 16 not in subboard:                    #checks if passive move not on passive board
            print('move not on ' + color + ' homeboard')
            return False
        if not self.check_if_valid(input1,input2,color):    #checks if movement is valid
            print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
            return False
        if self.check_if_pushes(input1,input2,color)!='x':  #checks if a stone is being pushed
            print('cannot push a stone on your passive move')
            return False
        return True

    def aggressive_move(self,input3,move,color,passive_board):
        pushed_stone = self.check_if_pushes(input3, input3 + move, color)   #returns the coordinate of the pushed stone, or 'x' if nothing pushed
        if board[input3] != color:
            print('must select your own stone')
            return False
        if passive_board % 2 == (input3 // 16) % 2:     #checks if aggressive move on same parity board of passive move
            print('move not on opposite colored board')
            return False
        if not self.check_if_valid((input3) % 16, (input3 + move) % 16, color): #checks if aggressive move pushes off board
            print('Error: aggressive move out of bounds')
            return False
        if board[input3+move] == color:
            print('you cannot push your own stone')
            return False
        if pushed_stone == False:       #check_if_pushes returns false if two stones are pushed
            print('cant push 2 stones')
            return False
        if pushed_stone != 'x':         #if a stone is being pushed, checks if the stone is your own color
            pushed_stone = int(pushed_stone)
            if board[pushed_stone]==color:
                print('cant push your own stone')
                return False
        return True


    def passive_aggressive(self, input1, input2, input3, color):
        move = input2 - input1
        passive_board = input1 // 16
        if not self.passive_move(input1, input2, color):
            print('passive move false')
            return False
        if not self.aggressive_move(input3,move,color,passive_board):
            print('aggressive move false')
            return False
        return True


    def update_board(self,input1,input2,input3,color,board):
        opponent = 'b' if color == 'w' else 'w'
        updated_board = list(board)
        move = input2 % 16 - input1 % 16
        halfmove = move


        if not self.passive_aggressive(input1,input2,input3,color):     #verifies the move is legal
            return False

        print(board)
        updated_board[input1] = 'x'
        updated_board[input2] = color
        updated_board[input3] = 'x'
        updated_board[input3 + move] = color
        print(board)
        
        pushed_stone = self.check_if_pushes(input3, input3 + move, color)
        print(pushed_stone)
        if pushed_stone != 'x':
            pushed_stone=int(pushed_stone)
            pushed_stone = int(pushed_stone)
            if move in self.two_space_moves:  #if move is 2 spaces, creates a 1 space move of same vector
                move = int(input1 + move / 2)
            if not self.check_if_valid(pushed_stone, int(input1 + move * 2), color): #checks if stone was pushed off board
                print('opponent ' + opponent + ' stone pushed off board from position ' + str(pushed_stone))
            else:
                updated_board[input3 + move + halfmove] = opponent
        return updated_board


def convert_to_string(board): #converts the board back from a list into a string for readability
    string=str(board[0])
    for i in range(1,len(board)):
        if i % 4 == 0:
            string += '\n'
        if i % 16 == 0:
            string +='\n \n'
        string+=board[i]
    return string

#testing
game=Rules(list(board))
updated_board=game.update_board(45,39,28,'w',board)
try:
    print(convert_to_string(updated_board))
except TypeError:
    pass

#print(game.board)