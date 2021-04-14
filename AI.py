import numpy as np
from Rules import Rules
import sys, os

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
