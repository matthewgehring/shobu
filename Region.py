import pygame
import numpy as np

black = pygame.image.load("assets/black.png")
black_stone = pygame.transform.scale(black, (50, 50))
white = pygame.image.load("assets/white.png")
white_stone = pygame.transform.scale(white, (50, 50))

class Region:
    def __init__(self, reg_num, x_offset, y_offset, background):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.region_number = reg_num
        self.background = background
        self.map = []
        self.stones = [['b','b','b','b'],
                        [' ',' ',' ',' '],
                        [' ',' ',' ',' '],
                        ['w','w','w','w']]
    
    def draw(self):
        for j in range(4):
            for i in range(4):
                rect = pygame.Rect(45*self.x_offset + (60 * i), 45*self.y_offset + (60 * j), 60, 60)
                self.map.append(rect)
                pygame.draw.rect(self.background, (0, 0, 0), rect, 2)
    
    def set_up(self, screen):
        for square in self.map:
            index = self.map.index(square)
            row = index // 4
            col = index % 4
            if self.stones[row][col] == 'b':
                screen.blit(black_stone, (square[0]+5, square[1]+5))
            elif self.stones[row][col] == 'w':
                screen.blit(white_stone, (square[0]+5, square[1]+5))
    
    def set_stones(self, stone_list):
        self.stones = np.copy(stone_list)