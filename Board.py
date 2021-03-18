import pygame
from Region import Region

class Board:
    def __init__(self, bg, screen):
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
        pygame.draw.rect(self.background, (0, 0, 0), self.outline, 3)
        self.screen.blit(self.background, (0, 0))
        self.update()

    def update(self):
        for region in self.regions:
            region.draw()
            region.set_up(self.screen)

    def clear(self):
        self.screen.blit(self.background, (0, 0))
