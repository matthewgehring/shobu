import numpy as np
import sys

unit_vectors = np.array([[0, 1, 0], [0, 0, 1], [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, 0], [0, 0, -1],
                         [0, -1, -1]])  # defines the legal vectors for stone movement up to two spaces
viable_vectors = np.concatenate((unit_vectors, unit_vectors * 2))

class Rules(object):
    def __init__(self, board, errors):
        self.board = board
        self.errors = errors 
    
    def set_errors(self, value):
        self.errors = value

    def obtain_board_pos(self, stone):
        if stone[1] not in [0, 1, 2, 3] or stone[2] not in [0, 1, 2,
                                                            3]:  # checks if position is out of bounds and returns ' '
            position = ' '
        else:
            position = self.board[stone[0]][stone[1]][stone[2]]
        return position

    def update_board_pos(self, stone, input, board_update):
        out_of_bounds = False
        if stone[1] not in [0, 1, 2, 3] or stone[2] not in [0, 1, 2, 3]:  # checks if position is out of bounds
            out_of_bounds = True
            return out_of_bounds
        board_update[stone[0]][stone[1]][stone[2]] = input
        return out_of_bounds

    def generate_unit_vector(self, vector):
        unit_vector = [0, 0, 0]
        for i in (1, 2):
            if vector[i] in (1, 2):
                unit_vector[i] = 1
            if vector[i] in (-1, -2):
                unit_vector[i] = -1
            if vector[i] == 0:
                unit_vector[i] = 0
        return unit_vector

    def check_if_pushes(self, board, stone,
                        vector):  # checks if there is a stone in the vector path of the aggressive move
        if board[stone[0]][stone[1] + vector[1]][stone[2] + vector[2]] != ' ' or (
                2 in vector and board[stone[0]][stone[1] + int(round(vector[1] / 2 + 0.5))][
            stone[2] + int(round(vector[2] / 2 + 0.5))] != ' '):
            return True
        else:
            return False

    def get_vector(self, stone_coordinate, move_coordinate):
        return (0, move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])

    def passive_move(self, color, stone_coordinate, move_coordinate, vector):
        legal_state = True
        if color == "b":
            homeboard = ('0', '1')
        if color == "w":
            homeboard = ('2', '3')

        if str(stone_coordinate[0]) not in homeboard:  # checks if passive move is on homeboard
            if self.errors: 
                print("Error: Board selected is not a homeboard")
            legal_state = False

        if self.obtain_board_pos(stone_coordinate) != color:  # checks if you're selecting your own stone
            if self.errors: 
                print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate))
            legal_state = False

        if stone_coordinate[0] != move_coordinate[0]:
            if self.errors: 
                print("Error: Stone coordinate and Move coordinate not on same board")
            legal_state = False

        if not (vector == viable_vectors).all(1).any():  # checks if stone movement is legal
            if self.errors: 
                print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
            legal_state = False

        if self.check_if_pushes(self.board, stone_coordinate, vector):
            if self.errors: 
                print(self.board, stone_coordinate, vector)
            if self.errors: 
                print("Error: Cannot push a stone on a passive move.")
            legal_state = False

        return legal_state

    def aggressive_move(self, color, opponent, passive_board, stone_coordinate, vector, unit_vector):

        move_position = np.array(stone_coordinate) + np.array(vector)
        legal_state = True
        if move_position[1] not in [0, 1, 2, 3] or move_position[2] not in [0, 1, 2, 3]:
            if self.errors: 
                print('Error: Aggressive move out of 4x4 bounds')
            legal_state = False

        if self.obtain_board_pos(stone_coordinate) != color:  # checks if you're selecting your own stone
            if self.errors: 
                print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate) + '  (aggressive move)')
            legal_state = False

        if stone_coordinate[0] % 2 == passive_board % 2:
            if self.errors: 
                print(
                'error: stone must be played on opposite colored board as your passive move')  # must play on boards of opposite parity
            legal_state = False

        if self.board[stone_coordinate[0]][stone_coordinate[1]][
            stone_coordinate[2]] != color:  # checks if you're selecting your own stone
            if self.errors: 
                print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate))
            legal_state = False

        if self.obtain_board_pos(move_position) == color or self.obtain_board_pos(
                np.array(stone_coordinate) + np.array(unit_vector)) == color:
            if self.errors: 
                print('Error: Cannot push your own stones')  # if vector length = 2, checks both spots. if length = 1, only checks destination
            legal_state = False

        if self.obtain_board_pos(move_position) == opponent and (
                self.obtain_board_pos(move_position + unit_vector) != ' ' or self.obtain_board_pos(
                move_position - unit_vector) == opponent):
            if self.errors: 
                print('Error: Cannot push more than one stone (Case 1)')
            legal_state = False  # if moved onto opponent stone, checks if there is an opponent stone 1 unit ahead or behind of stone

        if self.obtain_board_pos(move_position) == ' ' and self.obtain_board_pos(
                move_position - unit_vector) == opponent and self.obtain_board_pos(move_position + unit_vector) != ' ':
            if self.errors: 
                print('Error: Cannot push more than one stone (Case 2)')
            legal_state = False  # if moved onto empty space, checks if there is an opponent stone both 1 unit behind and ahead of stone

        return legal_state

    def passive_aggressive(self, color, init_stone, init_move, aggro_stone, vector, unit_vector, opponent, sub_board):

        passive_legal = self.passive_move(color, init_stone, init_move, vector)

        if not passive_legal:
            return False

        aggro_legal = self.aggressive_move(color, opponent, sub_board, aggro_stone, vector,
                                           unit_vector)  # using the vector from passive move, applies to aggressive stone and determines if legal

        if not aggro_legal:
            return False

        aggressive_moved = (aggro_stone[0], aggro_stone[1] + vector[1],
                            aggro_stone[2] + vector[2])  # records position of newly moved aggressive stone

        return True

    def update_board(self, color, init_stone, init_move, aggro_stone, board_history=[]):
        updated_board = np.copy(self.board)
        opponent = 'b' if color == 'w' else 'w'
        vector = self.get_vector(init_stone, init_move)
        if self.errors: 
            print('vector: ' + str(vector))
        unit_vector = np.array(self.generate_unit_vector(vector))
        sub_board = init_stone[0]
        legal = self.passive_aggressive(color, init_stone, init_move, aggro_stone, vector, unit_vector, opponent,
                                        sub_board)
        aggressive_moved = (aggro_stone[0], aggro_stone[1] + vector[1], aggro_stone[2] + vector[2])
        if legal == True:
            self.update_board_pos(init_stone, ' ', updated_board)
            self.update_board_pos(init_move, color, updated_board)
            self.update_board_pos(aggro_stone, ' ', updated_board)
            self.update_board_pos(aggressive_moved, color, updated_board)
            if self.obtain_board_pos(aggressive_moved) == opponent:
                out_of_bounds = self.update_board_pos(aggressive_moved + unit_vector, opponent, updated_board)
                if out_of_bounds == True:
                    if self.errors: 
                        print(opponent + ' stone removed from the board')
                else:
                    if self.errors: 
                        print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                        aggressive_moved + unit_vector))
            if self.obtain_board_pos(aggressive_moved) == ' ' and self.obtain_board_pos(
                    aggressive_moved - unit_vector) == opponent:
                self.update_board_pos(aggressive_moved - unit_vector, ' ', updated_board)
                out_of_bounds = self.update_board_pos(aggressive_moved + unit_vector, opponent, updated_board)
                if out_of_bounds == True:
                    if self.errors: 
                        print(opponent + ' stone removed from the board')
                else:
                    if self.errors: 
                        print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                        aggressive_moved + unit_vector))
            # board_history+=updated_board
            board_history.append(updated_board)
        else:
            if self.errors: 
                print('illegal move')

        return updated_board #, board_history