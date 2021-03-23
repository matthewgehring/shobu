import pygame
from Board import Board
from sys import exit

#todo: clean up magic code, work on separating movement logic into the correct areas, start building stone class if needed, implement move check logic

BACKGROUND = 'assets/ramin.jpg'
BOARD_SIZE = (810, 810)

def main():
    while True:
        pygame.display.update()
        pygame.time.wait(250)
        passive_stone = board.get_square()
        if passive_stone != None:
            print(passive_stone[0], passive_stone[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # if event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         for region in board.regions:
            #             for square in region.map:
            #                 while board.holding_stone[0] == False:
            #                 if square.collidepoint(event.pos):
            #                     #if board square and has stone then holding stone = true
            #                     if board.holding_stone[0] == False and region.stones[region.map.index(square)] == board.player:
            #                         print("space", region.region_number, region.map.index(square))
            #                         stone_color = region.stones[region.map.index(square)]
            #                         rowi = region.map.index(square) // 4
            #                         coli = region.map.index(square) % 4
            #                         initial = (region.region_number, rowi, coli)
            #                         board.holding_stone = [True, initial]
            #                         region.stones[region.map.index(square)] = ' '

            #                     elif board.holding_stone[0] == True:
            #                         board.holding_stone[0] = False
            #                         rowf = region.map.index(square) // 4
            #                         colf = region.map.index(square) % 4
            #                         final = (region.region_number, rowf, colf)
            #                         print("ass", region.stones[rowi*4+coli], "blaster")
            #                         if board.passive_move(board.player, stone_color, initial, final):
            #                             print('it worked!')
            #                             region.stones[region.map.index(square)] = board.player
            #                             board.holding_stone[1] = ' '
            #                             board.clear()
            #                             board.draw() #should be update here
            #                     break                



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Shobu')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    board = Board(background, screen)
    board.draw() 
    main()