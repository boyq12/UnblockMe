import pygame
from State import *
from Global import Singleton

@Singleton
class GameManager():
	def __init__(self):
		self.is_running = True
		self.next_state = None
		self.current_state = None

	def process_events(self):
		if self.current_state is None:
			return

		# Key press event
		self.current_state.process_key_press(pygame.key.get_pressed())

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.is_running = False
			else:
				self.current_state.process_events(event)

	def update(self):
		if (self.current_state != self.next_state):
			self.current_state = self.next_state
			self.current_state.init()

		self.current_state.update()

	def draw(self, screen):
		self.current_state.draw(screen)
		pygame.display.flip()

	def change_state(self, state):
		self.next_state = state

	def exit(self):
		self.is_running = False

	def get_running_state(self):
		return not self.is_running

	def get_current_state(self):
		return self.current_state