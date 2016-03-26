import os
import pygame
from ResourceManager import *
from GameManager import *
from Scene import *
from Global import *

class Main():
	def __init__(self):
		self.done = False

	def exit(self):
		self.done = True

	def main(self):
		# Create window at center
		os.environ['SDL_VIDEO_CENTERED'] = '1'

		# Initialize Pygame and set up the window
		pygame.init()

		size = [SCREEN_WIDTH, SCREEN_HEIGHT]
		screen = pygame.display.set_mode(size)

		pygame.mouse.set_visible(True)
	
		# Read resource
		ResourceManager.instance().read_resources(RM_path)
	
		# Create an instance of the Game class
		#game = GameManager()
		#game.change_state(Scene())
		GameManager.instance().change_state(Scene(ResourceManager.instance().scene_path_list['MAIN_SCENE']))
		
		clock = pygame.time.Clock()
	
		# Main game loop
		while not self.done:
			pygame.display.set_caption((' ' * 130) + 'UnBlock Me - FPS : ' + str(round(clock.get_fps(), 1)))

			# Check if exit game
			self.done = GameManager.instance().get_running_state()

			# Process events (keystrokes, mouse clicks, etc)
			GameManager.instance().process_events()
		
			# Update object positions, check for collisions
			GameManager.instance().update()
		
			# Draw the current frame
			GameManager.instance().draw(screen)
		
			# Pause for the next frame
			clock.tick(60)

		# Close window and exit
		pygame.quit()
		quit()

if __name__ == "__main__":
	Main().main()