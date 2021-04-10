import pygame
import numpy as np
from Board import Board
#importing the stuff

class AI:

#Table to show to points awarded based on position, stones near the center are higher value.
    board_points = numpy.array([
        [0,0,0,0],
        [0,.1,.1,0],
        [0,.1,.1,0],
        [0,0,0,0]
    ])

    def __init__(self):
        INFINITE = 10000000


    @staticmethod
    def evaluate(board):
        material = AI.get_piece_position_score(board, stone[1], board_points)
        return material 
    @staticmethod
    def get_piece_position_score(board, stone_color, table):
        white = 0
        black = 0
        for region in self.regions:
            for square in region.map:
                stone_color = region.stones[index]
                if (stone_color != ''):
                    if (stone_color == 'w'):
                        white += table[x][y]
                    else:
                        black += table[3 - x][y]

        return white - black
    #
        def get_ai_move(board, invalid_moves):
        best_move = 0
        best_score = AI.INFINITE
        for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True)
            if (score < best_score):
                best_score = score
                best_move = move

        # that's game
        if (best_move == 0):
            return 0

        copy = board.Board.clone(board)
        copy.perform_move(best_move)
        if (copy.is_check(pieces.Piece.BLACK)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(chessboard, invalid_moves)

        return best_move

    def minimax(position, depth, alpha, beta, maximizingPlayer)
	    if depth == 0
		return position
 
	if maximizingPlayer
		maxEval = -infinity
		for each child of position
			eval = minimax(child, depth - 1, alpha, beta false)
			maxEval = max(maxEval, eval)
			alpha = max(alpha, eval)
			if beta <= alpha
				break
		return maxEval
 
	else
		minEval = +infinity
		for each child of position
			eval = minimax(child, depth - 1, alpha, beta true)
			minEval = min(minEval, eval)
			beta = min(beta, eval)
			if beta <= alpha
				break
		return minEval