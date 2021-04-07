import pygame
import numpy as np
from Region import Region
import Rules
#TODO: set up highlight function

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

    def update_state(self, color, init_stone, init_move, aggro_stone,board_history=[]):
            self.board = [self.region0.stones, self.region1.stones, self.region2.stones, self.region3.stones]
            legality = Rules.Rules(self.board)
            updated_board= legality.update_board(color, init_stone, init_move, aggro_stone,board_history=[])
            print(updated_board)
            for region in self.regions:
                region.set_stones(updated_board[region.region_number])