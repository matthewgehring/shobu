import pygame
import numpy as np
from Region import Region

unit_vectors=np.array([[0,1, 0], [0,0, 1], [0,1, 1], [0,1,-1], [0,-1,1], [0,-1, 0], [0,0, -1], [0,-1, -1]])         #defines the legal vectors for stone movement up to two spaces
viable_vectors=np.concatenate((unit_vectors,unit_vectors*2))


class Board:
    def __init__(self, bg, screen):
        self.player = 'b'
        self.outline = pygame.Rect(45, 45, 690,690)
        self.background = bg
        self.screen = screen
        self.holding_stone = [False, ' ']
        self.region0 = Region(0, 1, 1,self.background)
        self.region1 = Region(1,11, 1,self.background)
        self.region2 = Region(2,1, 11,self.background)
        self.region3 = Region(3,11, 11,self.background)
        self.regions = [self.region0, self.region1, self.region2, self.region3]
        self.board = [self.region0.stones, self.region1.stones, self.region2.stones, self.region3.stones]
        self.draw()

    def arrow(self, passive_stone, passive_stone_move):
        pygame.draw.line(self.screen, (50, 205, 50), (((passive_stone[0]*2)+60)/2, ((passive_stone[1]*2)+60)/2), (((passive_stone_move[0]*2)+60)/2, ((passive_stone_move[1]*2)+60)/2), 2) 
        pygame.display.update()

    def draw(self):
        pygame.draw.rect(self.background,  (0,0, 0), self.outline, 3)
        self.screen.blit(self.background, (0, 0))
        self.update()

    def update(self):
        self.board = [self.region0.stones, self.region1.stones, self.region2.stones, self.region3.stones]
        for region in self.regions:
            region.draw()
            region.set_up(self.screen)

    def clear(self):
        self.screen.blit(self.background, (0, 0))

    def highlight(self, square):
        print(square)
        pygame.draw.rect(self.screen, (50, 205, 50), square, 2)
        pygame.display.update()
    
    def unhighlight(self, square):
        pygame.draw.rect(self.screen, (0, 0, 0), square, 2)
        pygame.display.update()

    def get_square(self):
        finished = False
        reg_num = None
        row = None
        col = None
        index = None
        stone_color = None
        current_square = None
        while finished == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for region in self.regions:
                            for square in region.map:
                                if square.collidepoint(event.pos):
                                    current_square = square
                                    reg_num = region.region_number
                                    index = region.map.index(square)
                                    row = index // 4
                                    col = index % 4
                                    stone_color = region.stones[row][col]
                                    finished = True
        return (reg_num, row, col), stone_color, current_square

    def obtain_board_pos(self, stone):
        if stone[1] not in [0,1,2,3] or stone[2] not in [0,1,2,3]:      #checks if position is out of bounds and returns ' '
            position=' '
        else:
            position= self.board[stone[0]][stone[1]][stone[2]]
        return position
    
    def update_board_pos(self, stone,input,board_update):
        out_of_bounds=False
        if stone[1] not in [0, 1, 2, 3] or stone[2] not in [0, 1, 2, 3]:  # checks if position is out of bounds
            out_of_bounds = True
            return out_of_bounds
        board_update[stone[0]][stone[1]][stone[2]]=input
        return out_of_bounds

    def generate_unit_vector(self, vector):
        unit_vector=[0,0,0]
        for i in (1,2):
            if vector[i] in (1,2):
                unit_vector[i]=1
            if vector[i] in (-1,-2):
                unit_vector[i]=-1
            if vector[i]==0:
                unit_vector[i]=0
        return unit_vector

    def check_if_pushes(self,board,stone,vector):                                       #checks if there is a stone in the vector path of the aggressive move
        if board[stone[0]][stone[1]+vector[1]][stone[2]+vector[2]]!=' ' or( 2 in vector and board[stone[0]][stone[1]+int(round(vector[1]/2+0.5))][stone[2]+int(round(vector[2]/2+0.5))]!=' '):
            return True
        else:
            return False

    def get_vector(self, stone_coordinate,move_coordinate):
        return (0,move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])

    def passive_move(self, color,stone_coordinate,move_coordinate, vector):

        if color == "b":
            homeboard = ('0', '1')
        if color == "w":
            homeboard = ('2', '3')

        if str(stone_coordinate[0]) not in homeboard:                          #checks if passive move is on homeboard
            print("Error: Board selected is not a homeboard")
            return False

        if self.obtain_board_pos(stone_coordinate)!=color:                          #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
            return False

        if stone_coordinate[0]!=move_coordinate[0]:
            print("Error: Stone coordinate and Move coordinate not on same board")
            return False

        if vector not in viable_vectors:                                        #checks if stone movement is legal
            print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
            return False

        if self.check_if_pushes(self.board,stone_coordinate,vector):
            print(self.board, stone_coordinate, vector)
            print("Error: Cannot push a stone on a passive move.")
            return False

        return True

    def aggressive_move(self, color, opponent, passive_board, stone_coordinate, vector, unit_vector):

        move_position=np.array(stone_coordinate)+np.array(vector)

        if move_position[1] not in [0,1,2,3] or move_position[2] not in [0,1,2,3]:
            print('Error: Aggressive move out of 4x4 bounds')
            return False

        if self.obtain_board_pos(stone_coordinate)!=color:                          #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate) + '  (aggressive move)')
            return False
            
        if stone_coordinate[0] % 2 == passive_board % 2:
            print('error: stone must be played on opposite colored board as your passive move')                 #must play on boards of opposite parity
            return False
            
        if self.board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:    #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
            return False
            
        if self.obtain_board_pos(move_position)==color or self.obtain_board_pos(np.array(stone_coordinate)+np.array(unit_vector))==color:
            print('Error: Cannot push your own stones')         #if vector length = 2, checks both spots. if length = 1, only checks destination
            return False
            
        if self.obtain_board_pos(move_position)==opponent and (self.obtain_board_pos(move_position+unit_vector)!= ' ' or self.obtain_board_pos(move_position-unit_vector)== opponent):
            print('Error: Cannot push more than one stone (Case 1)')
            return False               #if moved onto opponent stone, checks if there is an opponent stone 1 unit ahead or behind of stone
            
        if self.obtain_board_pos(move_position)==' ' and self.obtain_board_pos(move_position-unit_vector)==opponent and self.obtain_board_pos(move_position+unit_vector)!=' ':
            print('Error: Cannot push more than one stone (Case 2)')
            return False               #if moved onto empty space, checks if there is an opponent stone both 1 unit behind and ahead of stone
            
        return True

    def passive_aggressive(self, color, init_stone,init_move,aggro_stone, vector, unit_vector, opponent, sub_board):

        passive_legal = self.passive_move(color, init_stone, init_move, vector)

        if not passive_legal:
            return False

        aggro_legal = self.aggressive_move(color, opponent, sub_board, aggro_stone, vector, unit_vector)  #using the vector from passive move, applies to aggressive stone and determines if legal

        if not aggro_legal:
            return False

        aggressive_moved=(aggro_stone[0],aggro_stone[1]+vector[1],aggro_stone[2]+vector[2]) #records position of newly moved aggressive stone

        return True

    def update_board(self, color, init_stone, init_move, aggro_stone,board_history=[]):
            self.board = [self.region0.stones, self.region1.stones, self.region2.stones, self.region3.stones]
            updated_board=np.copy(self.board)
            opponent= 'b' if color == 'w' else 'w'
            vector = self.get_vector(init_stone, init_move)
            unit_vector = np.array(self.generate_unit_vector(vector))
            sub_board = init_stone[0]
            legal = self.passive_aggressive(color,init_stone, init_move,aggro_stone, vector, unit_vector, opponent, sub_board)
            aggressive_moved = (aggro_stone[0], aggro_stone[1] + vector[1], aggro_stone[2] + vector[2])
            if legal==True:
                self.update_board_pos(init_stone, ' ', updated_board)
                self.update_board_pos(init_move, color, updated_board)
                self.update_board_pos(aggro_stone, ' ', updated_board)
                self.update_board_pos(aggressive_moved, color, updated_board)
                if self.obtain_board_pos(aggressive_moved) == opponent:
                    out_of_bounds=self.update_board_pos(aggressive_moved+unit_vector, opponent, updated_board)
                    if out_of_bounds==True:
                        print(opponent + ' stone removed from the board')
                    else:
                        print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                        aggressive_moved + unit_vector))
                if self.obtain_board_pos(aggressive_moved) == ' ' and self.obtain_board_pos(aggressive_moved - unit_vector) == opponent:
                    self.update_board_pos(aggressive_moved-unit_vector,' ', updated_board)
                    out_of_bounds= self.update_board_pos(aggressive_moved+unit_vector,opponent,updated_board)
                    if out_of_bounds==True:
                        print(opponent + ' stone removed from the board')
                    else:
                        print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                        aggressive_moved + unit_vector))
                #board_history+=updated_board
                board_history.append(updated_board)
            else:
                print('illegal move')

            for region in self.regions:
                region.set_stones(updated_board[region.region_number])
            return updated_board,board_history