import pygame
import os
import time
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
size = (700, 500)
# Window config
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576


def main():
    # Create window at center
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # Initialize Pygame and set up the window
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    back = pygame.image.load("Resources/background/main-back.jpg")
    back = pygame.transform.scale(back, (SCREEN_WIDTH, SCREEN_HEIGHT))
    block = pygame.image.load("Resources/background/menu-background.jpg")
    block = pygame.transform.scale(block, (500,500))
    button = pygame.image.load("Resources/background/button.jpg")
    button = pygame.transform.scale(button, (360,70))
    game_area = pygame.image.load("Resources/background/sand.jpg")
    game_area = pygame.transform.scale(game_area, (500,500))
    myfont = pygame.font.SysFont("monospace", 30)

    # render text
    next_lable = myfont.render("Next Game", 1, (255, 255, 0))
    dfs_lable = myfont.render("Deapth First Search", 1, (255, 255, 0))
    bfs_lable = myfont.render("Best First Search", 1, (255, 255, 0))
    hill_lable = myfont.render("Simple Hill Climbing", 1, (255, 255, 0))
    reset_lable = myfont.render("Reset", 1, (255, 255, 0))

    #drawing background
    screen.blit(back, [0,0] )
    screen.blit(block, [0,50])
    screen.blit(button, [70,140])
    screen.blit(button, [70,225])
    screen.blit(button, [70,310])
    screen.blit(button, [70,395])
    screen.blit(button, [70,475])
    screen.blit(next_lable, (170, 160))
    screen.blit(dfs_lable, (80, 245))
    screen.blit(bfs_lable, (100, 330))
    screen.blit(hill_lable, (72, 415))
    screen.blit(reset_lable, (190, 495))
    screen.blit(game_area, [515,50])
    #update
    pygame.display.flip()

    time.sleep(30)
if __name__ == "__main__":
	main()