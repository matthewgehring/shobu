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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for region in self.regions:
                        for square in region.map:
                            if square.collidepoint(event.pos):
                                index = region.map.index(square)
                                stone_color = region.stones[index]
                                row = index // 4
                                col = index % 4
                                return (region.region_number, row, col), stone_color

    def passive_move(self, color, stone_color, stone_coordinate,move_coordinate):
        legal = True
        vector = (0,move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])
        if color == "b":
            homeboard = ('0', '1')
        if color == "w":
            homeboard = ('2', '3')
        while True:
            print(stone_color, color)
            if str(stone_coordinate[0]) not in homeboard:                          #checks if passive move is on homeboard
                print("Error: Board selected is not a homeboard")
                legal=False
                pass
            if stone_color != color:                          #checks if you're selecting your own stone
                print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
                legal = False
                pass
            if stone_coordinate[0]!=move_coordinate[0]:
                print("Error: Stone coordinate and Move coordinate not on same board")
                legal = False
                pass
            if vector not in viable_vectors:                                        #checks if stone movement is legal
                print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
                legal = False
                pass
            return legal # , vector, stone_coordinate[0]

    def aggressive_move(self, color, passive_board, stone_coordinate, vector):
        legal=True
        players=['b','w']
        players.remove(color)        #returns w if color is b, b if color is w
        opponent=players[0]
        while True:
            move_position=np.array(stone_coordinate)+np.array(vector)
            unit_vector=np.array(generate_unit_vector(vector))
            if move_position[1] not in [0,1,2,3] or move_position[2] not in [0,1,2,3]:
                print('Error: Aggressive move out of 4x4 bounds')
                legal = False
                return legal
            if obtain_board_pos(stone_coordinate)!=color:                          #checks if you're selecting your own stone
                print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate) + '  (aggressive move)')
                legal = False
                pass
            if stone_coordinate[0] % 2 == passive_board % 2:
                print('error: stone must be played on opposite colored board as your passive move')                 #must play on boards of opposite parity
                legal = False
                pass
            if board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:                         #checks if you're selecting your own stone
                print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
                legal = False
                pass
            if obtain_board_pos(move_position)==color or obtain_board_pos(np.array(stone_coordinate)+np.array(unit_vector))==color:
                print('Error: Cannot push your own stones')         #if vector length = 2, checks both spots. if length = 1, only checks destination
                legal = False
            if obtain_board_pos(move_position)==opponent and (obtain_board_pos(move_position+unit_vector)!= ' ' or obtain_board_pos(move_position-unit_vector)== opponent):
                print('Error: Cannot push more than one stone (Case 1)')
                legal = False               #if moved onto opponent stone, checks if there is an opponent stone 1 unit ahead or behind of stone
                pass
            if obtain_board_pos(move_position)==' ' and obtain_board_pos(move_position-unit_vector)==opponent and obtain_board_pos(move_position+unit_vector)!=' ':
                print('Error: Cannot push more than one stone (Case 2)')
                legal= False                #if moved onto empty space, checks if there is an opponent stone both 1 unit behind and ahead of stone
                pass
            return legal, opponent, unit_vector

