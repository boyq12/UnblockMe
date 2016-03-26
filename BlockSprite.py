import pygame
from Global import *
from Object import *
from Block import *

class BlockSprite(Object):
	def __init__(self, block = None):
		super(BlockSprite, self).__init__()
		self.block = block

	def set_block(self, block):
		self.block = block