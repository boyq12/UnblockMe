import pygame
from Block import *
from Global import *
from copy import deepcopy

class Board(object):
	def __init__(self):
		super(Board, self).__init__()
		self.state = [[0 for x in range(6)] for x in range(6)]
		self.size = (600, 600)
		self.pos = (400, 50)
		self.block_list = []
		self.coord_goal_x = None
		self.coord_goal_y = None

	def process(self):
		for i in range(6):
			for j in range(6):
				c = self.state[i][j];
				
				if c is not ' ':
					block = next((block for block in self.block_list if block.name == c), None)
					
					if block is not None:
						block.length += 1
						
						if block.direction is None:
							if block.coord[1] is i:
								block.direction = Direction.HORIZONTAL
							else:
								block.direction = Direction.VERTICAL
					else:
						self.block_list.append(
							Block(
								self,
								name = c,
								coord = [j, i],
								position = [self.pos[0] + j * 100, self.pos[1] + i * 100],
							    length = 1
								)
							)

	def update_block(self, block):
		block_name = block.name

		self.state = [[' ' if x is block_name else x for x in y] for y in self.state]

		if block.direction is Direction.HORIZONTAL:
			for i in range(block.length):
				self.state[block.coord[1]][block.coord[0] + i] = block_name
		else:
			for i in range(block.length):
				self.state[block.coord[1] + i][block.coord[0]] = block_name

	def clone(self):
		return deepcopy(self)