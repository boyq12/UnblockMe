import pygame
from Global import *
from Board import *

class Block(object):
	def __init__(self, name = None, direction = None, coord = [], position = [], length = 0):
		super(Block, self).__init__()
		self.coord = coord
		self.length = length
		self.name = name
		self.direction = direction
		self.position = position

	#def __init__(self, name = None, location = []):
	#	super(Block, self).__init__()

	#	self.name = name
	#	self.contain = location
	#	self.direction = None

	#	if self.contain[1] == self.contain[3]:
	#		self.direction = Direction.VERTICAL
	#	else:
	#		self.direction = Direction.HORIZONTAL

	#def check(self, board, direction):
	#	if direction == 0:
	#		row = self.contain[0]
	#		col = self.contain[1]
	#		if row > 0:
	#			if board.state[row - 1][col] == ' ':
	#				return True
	#		return False

	#	if direction == 1:
	#		row = self.contain[len(self.contain) - 2]
	#		col = self.contain[1]
	#		if row < 5:
	#			if board.state[row + 1][col] == ' ':
	#				return True
	#		return False

	#	if direction == 2:
	#		row = self.contain[0]
	#		col = self.contain[1]
	#		if col > 0:
	#			if board.state[row][col - 1] == ' ':
	#				return True
	#		return False

	#	if direction == 3:
	#		row = self.contain[0]
	#		col = self.contain[len(self.contain) - 1]
	#		if col < 5:
	#			if board.state[row][col + 1] == ' ':
	#				return True;
	#		return False;

	#	return False
	
	#def move(self, board, direction):
	#	if direction == 0:
	#		firstRow = self.contain[0]
	#		col = self.contain[1]
	#		lastRow = self.contain[len(self.contain) - 2]

	#		for i in range(0, len(self.contain), 2):
	#			self.contain[i] = self.contain[i] - 1

	#		board.state[firstRow - 1][col] = self.name;
	#		board.state[lastRow][col] = ' '
		
	#	elif direction == 1:
	#		firstRow = self.contain[0]
	#		col = self.contain[1]
	#		lastRow = self.contain[len(self.contain) - 2]

	#		for i in range(0, len(self.contain), 2):
	#			self.contain[i] = self.contain[i] + 1

	#		board.state[lastRow + 1][col] = self.name
	#		board.state[firstRow][col] = ' '
		
	#	elif direction == 2:
	#		firstCol = self.contain[1]
	#		row = self.contain[0]
	#		lastCol = self.contain[len(self.contain) - 1]

	#		for i in range(1, len(self.contain), 2):
	#			self.contain[i] = self.contain[i] - 1

	#		board.state[row][firstCol - 1] = self.name
	#		board.state[row][lastCol] = ' '

	#	elif direction == 3:
	#		firstCol = self.contain[1]
	#		row = self.contain[0]
	#		lastCol = self.contain[len(self.contain) - 1]

	#		for i in range(1, len(self.contain), 2):
	#			self.contain[i] = self.contain[i] + 1

	#		board.state[row][lastCol + 1] = self.name;
	#		board.state[row][firstCol] = ' '
		
	#	return board
	

	def move(self, step):
		if self.direction is Direction.HORIZONTAL:
			self.coord[0] += step
			self.position[0] += step * 100
		else:
			self.coord[1] += step
			self.position[1] += step * 100