import pygame
from Object import *

class Text(Object):
	def __init__(self, font, size, bold = False, italic = False, color = BLACK):
		super(Text, self).__init__()
		self.font = pygame.font.SysFont(font, size, bold, italic)
		self.color = color
		self.text = ''
		self.rect = pygame.Rect(0, 0, 1, 1)
		self._layer = pygame.sprite.LayeredUpdates()._default_layer

	def update(self):
		self.image = self.font.render(self.text, True, self.color)

	def set_color(self, color):
		self.color = color

	def set_text(self, text):
		self.text = text