import pygame
from Global import *
from Board import *

class Block(object):
	def __init__(self, board = None, name = None, direction = None, coord = [], position = [], length = 0):
		super(Block, self).__init__()
		self.board = board
		self.coord = coord
		self.length = length
		self.name = name
		self.direction = direction
		self.position = position
		self.speed = 5

	def move(self, step):
		if self.direction is Direction.HORIZONTAL:
			self.coord[0] += step
			self.position[0] += step * 100
		else:
			self.coord[1] += step
			self.position[1] += step * 100