import pygame
import numpy as np
from Region import Region
#TODO: set up highlight function

zeros=np.zeros((4,4,4),dtype='str')                                                             #initializes the board state
board=np.array((('b','b','b','b'),(' ',' ',' ',' '),(' ',' ',' ',' '),('w','w','w','w')))
board=np.core.defchararray.add(zeros, board)
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
        self.draw()

    def draw(self):
        pygame.draw.rect(self.background,  (0,0, 0), self.outline, 3)
        self.screen.blit(self.background, (0, 0))
        self.update()

    def update(self):
        for region in self.regions:
            region.draw()
            region.set_up(self.screen)

    def clear(self):
        self.screen.blit(self.background, (0, 0))

    def highlight(self, square):
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
        while finished == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for region in self.regions:
                            for square in region.map:
                                if square.collidepoint(event.pos):
                                    #self.highlight(square)
                                    reg_num = region.region_number
                                    index = region.map.index(square)
                                    stone_color = region.stones[index]
                                    row = index // 4
                                    col = index % 4
                                    finished = True
        return (reg_num, row, col), stone_color

    def obtain_board_pos(self, stone):
        if stone[1] not in [0,1,2,3] or stone[2] not in [0,1,2,3]:      #checks if position is out of bounds and returns ' '
            position=' '
        else:
            position=board[stone[0]][stone[1]][stone[2]]
        return position

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
        if board[stone[0]][stone[1]+vector[1]][stone[2]+vector[2]]!=' 'or\
                    board[stone[0]][stone[1]+int(round(vector[1]/2+0.1))][stone[2]+int(round(vector[2]/2+0.1))]!=' ':
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

        if self.check_if_pushes(board,stone_coordinate,vector):
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
            
        if board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:    #checks if you're selecting your own stone
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

    def update_board(self, init_stone, init_move, aggro_stone, aggressive_moved, aggro_legal, passive_legal, unit_vector, opponent):
        print('stone selected: '+str([self.obtain_board_pos(init_stone)])+ ' at ' + str(init_stone))
        print('move position: '+str([self.obtain_board_pos(init_move)]) + ' at ' +str(init_move))
        print('aggressive stone selected: '+str([self.obtain_board_pos(aggro_stone)]) + ' at ' +str(aggro_stone))
        print('aggressive stone moved to: ' + str([self.obtain_board_pos(aggressive_moved)])+' at ' + str(aggressive_moved))

        if aggro_legal==True and passive_legal==True:
            legal = True
        if legal == True and self.obtain_board_pos(aggressive_moved) == opponent:
            print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(aggressive_moved+unit_vector))
            if -1 in aggressive_moved+unit_vector or 4 in aggressive_moved+unit_vector:
                print(opponent + ' stone removed from the board')
        if legal == True and self.obtain_board_pos(aggressive_moved) == ' ' and self.obtain_board_pos(aggressive_moved-unit_vector)==opponent:
            print(str([opponent]) + ' stone pushed from ' + str(aggressive_moved-unit_vector) + ' to ' + str(aggressive_moved+unit_vector) )
            if -1 in aggressive_moved+unit_vector or 4 in aggressive_moved+unit_vector:
                print(opponent + ' stone removed from the board')

    def passive_aggressive(self, color, init_stone,init_move,aggro_stone):
        #this does the same thing as what you had in aggresive_move
        #its called a "ternary operator" all languages have this ability but usually with different syntax
        opponent= 'b' if color == 'w' else 'w'

        vector = self.get_vector(init_stone, init_move)
        unit_vector = np.array(self.generate_unit_vector(vector))
        sub_board = init_stone[0]

        passive_legal = self.passive_move(color, init_stone, init_move, vector)

        if not passive_legal:
            return False

        aggro_legal = self.aggressive_move(color, opponent, sub_board, aggro_stone, vector, unit_vector)  #using the vector from passive move, applies to aggressive stone and determines if legal

        if not aggro_legal:
            return False

        aggressive_moved=(aggro_stone[0],aggro_stone[1]+vector[1],aggro_stone[2]+vector[2]) #records position of newly moved aggressive stone

        self.update_board(init_stone, init_move, aggro_stone, aggressive_moved, aggro_legal, passive_legal, unit_vector, opponent)
        return True

