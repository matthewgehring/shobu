import pygame
from Board import Board
from sys import exit

#todo: clean up magic code, work on separating movement logic into the correct areas, start building stone class if needed, implement move check logic

BACKGROUND = 'ramin.jpg'
BOARD_SIZE = (810, 810)

def main():
    while True:
        count = 0
        pygame.display.update()
        pygame.time.wait(250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for region in board.regions:
                        for square in region.map:
                            if square.collidepoint(event.pos):
                                #if board square and has stone then holding stone = true
                                if board.holding_stone[0] == False and (region.stones[region.map.index(square)] == 'b' or region.stones[region.map.index(square)] == 'w') :
                                    print("space", region.region_number, region.map.index(square))
                                    stone = 'b' if region.stones[region.map.index(square)] == 'b' else 'w'
                                    board.holding_stone = [True, stone]
                                    region.stones[region.map.index(square)] = ' '

                                elif board.holding_stone[0] == True and region.stones[region.map.index(square)] == ' ':
                                    board.holding_stone[0] = False
                                    region.stones[region.map.index(square)] = board.holding_stone[1]
                                    board.holding_stone[1] = ' '
                                    board.clear()
                                    board.draw() #should be update here
                                break                



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Shobu')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    board = Board(background, screen)
    board.draw() 
    main()