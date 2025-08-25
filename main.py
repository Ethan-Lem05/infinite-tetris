import pygame
from sys import exit
import math


class Board:
    
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height

        self.board = [[0]*width for i in range(height)]
    
    def update_board(self, next_state):
        self.board = next_state
        return 
    
    def get_board(self):
        return self.board


def get_board_sprite(sprite_width, sprite_height, board_width = 10, board_height = 20):
    background_color = pygame.Color('#004585')
    background = pygame.Surface((sprite_width, sprite_height))
    background.fill(background_color)

    border_color = pygame.Color('#046ac9')
    horizontal_seperation_dist = sprite_width / board_width
    vertical_seperation_dist = sprite_height / board_height

    horizontal_line = pygame.Surface((sprite_width,2), border_color)
    horizontal_line.fill(border_color)
    
    for i in range(board_height+1):
        background.blit(horizontal_line, (0,min(i*vertical_seperation_dist, sprite_height-2)))

    vertical_line = pygame.Surface((2,sprite_height), border_color)
    vertical_line.fill(border_color)

    for i in range(board_width+1):
        background.blit(vertical_line,(min(i*horizontal_seperation_dist, sprite_width-2),0))
    
    return background

def get_background(width, height): 
    background = pygame.Surface((width,height))
    background_color = pygame.Color('#013361')
    background.fill(background_color)

    return background

def main():

    pygame.init()

    # CONSTATNS
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 960
    BOARD_SPRITE_WIDTH = 0.8*SCREEN_WIDTH
    BOARD_SPRITE_HEIGHT = 0.8*SCREEN_HEIGHT
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    # GAME OBJECT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    background = get_background(SCREEN_WIDTH,SCREEN_HEIGHT)
    board = Board(BOARD_WIDTH, BOARD_HEIGHT) 
    board_sprite = get_board_sprite(BOARD_SPRITE_WIDTH, BOARD_SPRITE_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT)

    # GAME LOOP
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.blit(background, (0,0))
        screen.blit(board_sprite, (0.1*SCREEN_WIDTH,0.1*SCREEN_HEIGHT))
                
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()