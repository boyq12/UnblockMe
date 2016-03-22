import os
import pygame
import random
from Global import *
from GameManager import *

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
    pygame.mouse.set_visible(False)
    game = GameManager()
    game.change_state(Scene())

    done = False
    clock = pygame.time.Clock()

    # Main game loop
    while not done:
        pygame.display.set_caption((' ' * 130) + 'Unblock Mine - FPS : ' + str(round(clock.get_fps(), 1)))
        # Check if exit game
        done = GameManager.instance().get_running_state()

        # Process events (keystrokes, mouse clicks, etc)
        game.process_events()

        # Update object positions, check for collisions
        game.update()

        # Draw the current frame
        game.draw(screen)

        # Pause for the next frame
        clock.tick(60)  # Close window and exit
    pygame.quit()

if __name__ == "__main__":
    main()
