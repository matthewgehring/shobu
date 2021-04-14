import numpy as np
from Rules import Rules
from Board import Board
import sys, os

#Table to show to points awarded based on position, stones near the center are higher value.
#Used in evaluate method
    board_points = numpy.array([
        [0,0,0,0],
        [0,.1,.1,0],
        [0,.1,.1,0],
        [0,0,0,0]
    ])

def blockPrint():           # Disable printing
    sys.stdout = open(os.devnull, 'w')

def enablePrint():          # Restore printing
    sys.stdout = sys.__stdout__
zeros=np.zeros((4,4,4),dtype='str')
initboard=np.array((('b','b','b','b'),(' ',' ',' ',' '),(' ',' ',' ',' '),('w','w','w','w')))
board=np.core.defchararray.add(zeros, initboard)
unit_vectors = np.array([[0, 1, 0], [0, 0, 1], [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, 0], [0, 0, -1],
                                 [0, -1, -1]])  # defines the legal vectors for stone movement up to two spaces
viable_vectors = np.concatenate((unit_vectors, unit_vectors * 2))
Board=Rules(board)

def find_my_stones(color,board):
    my_stones =[]
    for i in range(0, 4):
        for j in range(0,4):
            for k in range(0,4):
                if board[i][j][k]==color:
                    my_stones.append((i,j,k))
    return my_stones

def potential_passive_moves(color,my_stones):           # returns passive moves in the form of: (initial stone, move coordinate, vector)
    passive_moves=[]
    passive_stones=my_stones.copy()
    blockPrint()
    cases_tested=0
    homeboard=Board.initialize_homeboard(color)
    for i in range(len(my_stones)):                 #filters out stones not on homeboard to be tested
        if str(my_stones[i][0]) not in homeboard:
            passive_stones.remove(my_stones[i])
    for i in range(len(passive_stones)):
        for j in range((len(viable_vectors))):
            cases_tested+=1
            if any((-2,-1,4,5)) not in (passive_stones[i]+viable_vectors[j]):
                stone_coordinate=passive_stones[i]
                move_coordinate=np.array(passive_stones[i]+viable_vectors[j]).tolist()
                vector = Board.get_vector(stone_coordinate,move_coordinate)
                if Board.passive_move(color,stone_coordinate,move_coordinate,vector):
                    passive_moves.append((stone_coordinate,move_coordinate,vector))
    enablePrint()
    return passive_moves, cases_tested

def potential_aggressive_moves(color,passive_moves,my_stones):
    aggressive_moves=[]
    aggrostones=[]
    cases_tested=1
    opponent = 'b' if color == 'w' else 'w'
    blockPrint()
    for i in range(len(passive_moves)):
        aggrostones=my_stones.copy()
        unit_vector = Board.generate_unit_vector(passive_moves[i][2])
        aggroboards = [0, 2] if passive_moves[i][0][0] in [1, 3] else [1, 3]
        for i in range(len(my_stones)):                     # filters out stones not on aggressive boards to be tested
            if (my_stones[i][0]) not in aggroboards:
                aggrostones.remove(my_stones[i])
        for i in range(len(aggrostones)):
            cases_tested+=1
            if Board.aggressive_move(color,opponent,passive_moves[i][0][0],aggrostones[i],passive_moves[i][2],unit_vector):
                aggressive_moves.append((passive_moves[i][0],passive_moves[i][1],aggrostones[i]))
    enablePrint()
    return aggressive_moves, cases_tested



#my_stones=find_my_stones('b',board)
#all_passive_moves,cases_tested = potential_passive_moves('b',my_stones)
#all_possible_moves,aggro_cases_tested = potential_aggressive_moves('b', all_passive_moves,my_stones)
def find_all_moves(color,board):
    my_stones = find_my_stones(color, board)
    all_passive_moves, passive_cases_tested = potential_passive_moves(color, my_stones)
    all_possible_moves, aggro_cases_tested = potential_aggressive_moves(color, all_passive_moves, my_stones)
    return all_possible_moves, all_passive_moves,my_stones, passive_cases_tested, aggro_cases_tested

all_possible_moves, all_passive_moves,my_stones, passive_cases, aggro_cases=find_all_moves('b',board)

print('number of my stones on the board: ' +  str(len(my_stones)))
print(('number of valid passive moves: ' + str(len(all_passive_moves))))
print('cases tested: ' + str(passive_cases))
print('number of total possible moves: ' + str(len(all_possible_moves)))
print('cases tested: ' + str(aggro_cases))


class Static:
    #Evaluates the static material value of each board
    def evaluate(board):
        material = Static.get_piece_position_score(board, stone[1], board_points)
        return material 
    #Evaluates the the piece position based score taking in the board, stone color of the piece and the constant table which will be board points at the beginning.
    def get_piece_position_score(board, stone_color, table):
        white = 0
        black = 0
        for region in self.regions: #Maps the regions and goes through each square to evaluate the color
            for square in region.map:
                stone_color = region.stones[index]
                if (stone_color != ''):
                    if (stone_color == 'w'):
                        white += 1
                    else:
                        black += 1

        return white - black #returns the total material score less is good for black and more is good for white
class AI:

    INFINITE = 10000000 

        def get_ai_move(color, board):
        best_move = 0
        best_score = AI.INFINITE
        for stone in find_my_stones(color, board): #3 for loops to test each stone / passive_move / aggressive_move
            for passive_move in potential_passive_moves(color, stone):
                 if potential_passive_moves(color, stone)[0] != []: #once we remove cases tested we won't need [0]
                    continue   
                for aggro_move in potential_aggressive_moves(color, passive_move, stone)
                    copy = np.copy(self.board)
                    copy.update_state(color, stone, passive_move, aggro_move[2]) #Updates the cloned board with the new move

                    score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True) #Find's the score for a particular move, need to add more ways to affect the score this is just material and position based 
                    if (score < best_score):
                        best_score = score
                        best_move = [stone, passive_move, aggro_move[2]]

                # no possible best move
                if (best_move == []):
                    return 0

                copy = np.copy(self.board)
                copy.update_state(color, best_move[0], best_move[1], best_move[2])
                return best_move

def alphabeta(board, depth, a, b, maximizing): #Maximizing is either True for white or False for Black. Depends on depth too
        if (depth == 0):
            return Static.evaluate(board)

        if (maximizing):
            best_score = -AI.INFINITE
            for stone in find_my_stones('w', board): #Finds best score for white cuts off any branches where black would get a good move
                for passive_move in potential_passive_moves(color, stone):
                    for aggro_move in potential_aggressive_moves(color, passive_move, stone)
                        copy = np.copy(self.board)
                        copy.update_state(color, stone, passive_move, aggro_move[2])

                        best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                        a = max(a, best_score)
                        if (b <= a):
                            break
            return best_score
        else:
            best_score = AI.INFINITE
            for stone in find_my_stones('b', board): #Finds best score for black, cuts off any branches where white would get a good move
                for passive_move in potential_passive_moves(color, stone):
                    for aggro_move in potential_aggressive_moves(color, passive_move, stone)
                        copy = np.copy(self.board)
                        copy.update_state(color, stone, passive_move, aggro_move[2])

                        best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                        b = min(b, best_score)
                        if (b <= a):
                            break
            return best_score