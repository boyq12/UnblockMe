import pygame
from Block import *
from Movement import *
from Global import *
from copy import deepcopy

class Board(object):
	#def __init__(self):
	#	self.state = [[0 for x in range(6)] for x in range(6)]
	#	self.block_list = []

	#def generate_moves(self):
	#	result = []
	#	board = self.clone()

	#	for block in self.block_list:
	#		if block.direction == Direction.VERTICAL:
	#			for i in range(2):
	#				while block.check(board, i):
	#					new_block = next(b for b in board.block_list if b.name == block.name)
	#					new_block.move(board, i)
	#					new_board = board.clone()
	#					result.append(new_board)

	#				board = self.clone()

	#		if block.direction == Direction.HORIZONTAL:
	#			for i in range(2, 4):
	#				while block.check(board, i):
	#					new_block = next(b for b in board.block_list if b.name == block.name)
	#					new_block.move(board, i)
	#					new_board = board.clone()
	#					result.append(new_board)

	#				board = self.clone()

	#	return result

	#def equals(self, board):
	#	return self.state == board.state

	def __init__(self):
		super(Board, self).__init__()
		self.state = [[0 for x in range(6)] for x in range(6)]
		self.block_list = []
		self.pos = [400, 50]
		self.movement = None
		self.parent = None

	def process(self):
		for i in range(6):
			for j in range(6):
				c = self.state[i][j]
				
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
						self.block_list.append(Block(
								name = c,
								coord = [j, i],
								position = [self.pos[0] + j * 100, self.pos[1] + i * 100],
								length = 1))

	def update_block(self, block):
		block_name = block.name

		self.state = [[' ' if x is block_name else x for x in y] for y in self.state]

		if block.direction is Direction.HORIZONTAL:
			for i in range(block.length):
				self.state[block.coord[1]][block.coord[0] + i] = block_name
		else:
			for i in range(block.length):
				self.state[block.coord[1] + i][block.coord[0]] = block_name

	def generate_moves(self):
		result = []

		for block in self.block_list:
			if block.direction is Direction.HORIZONTAL:
				pos_x = block.coord[0] - 1

				while pos_x >= 0 and self.state[block.coord[1]][pos_x] is ' ':
					board = self.clone()
					step = pos_x - block.coord[0]
					new_board_block = next(b for b in board.block_list if b.name is block.name)
					new_board_block.move(step)
					board.movement = Movement(new_board_block.name, step)
					board.parent = self
					board.update_block(new_board_block)
					result.append(board)
					pos_x -= 1

				pos_x = block.coord[0] + block.length

				while pos_x < 6 and self.state[block.coord[1]][pos_x] is ' ':
					board = self.clone()
					step = pos_x - block.coord[0] - block.length + 1
					new_board_block = next(b for b in board.block_list if b.name is block.name)
					new_board_block.move(step)
					board.movement = Movement(new_board_block.name, step)
					board.parent = self
					board.update_block(new_board_block)
					result.append(board)
					pos_x += 1
			else:
				pos_y = block.coord[1] - 1

				while pos_y >= 0 and self.state[pos_y][block.coord[0]] is ' ':
					board = self.clone()
					step = pos_y - block.coord[1]
					new_board_block = next(b for b in board.block_list if b.name is block.name)
					new_board_block.move(step)
					board.movement = Movement(new_board_block.name, step)
					board.update_block(new_board_block)
					result.append(board)
					pos_y -= 1

				pos_y = block.coord[1] + block.length

				while pos_y < 6 and self.state[pos_y][block.coord[0]] is ' ':
					board = self.clone()
					step = pos_y - block.coord[1] - block.length + 1
					new_board_block = next(b for b in board.block_list if b.name is block.name)
					new_board_block.move(step)
					board.movement = Movement(new_board_block.name, step)
					board.update_block(new_board_block)
					result.append(board)
					pos_y += 1

		return result

	def is_win(self):
		block = next(x for x in self.block_list if x.name == 'x')
		return block.coord[0] + block.length == 6

		#x = block.coord[0] + block.length
		#y = block.coord[1]

		#while x < 6:
		#	if self.state[y][x] != ' ':
		#		return False
		#	x += 1

		#return True

	#get heristic score
	def get_score(self):
		block_list = []
		main_block = next(x for x in self.block_list if x.name == 'x')

		score = 0
		i = 0

		if((main_block.coord[0] + main_block.length) == 6):
			return 1

		block_list.append(main_block)

		while(i <= (len(block_list) - 1)):
			score -= self.count_obstructor(block_list[i], block_list)
			i+=1
		return score

	#count Obstructure
	def count_obstructor(self, block, blockList):
		count = 0
		position = block.coord
		processingBlock = block.name
		currentTileBlock = None
		lastBlock = '0'

		i = 0
		while i < 6:
			if i == 0 and block.name == 'x':
				i = position[0] + block.length

				if(i == 6):
					break

			if block.direction == Direction.HORIZONTAL:
				currentTileBlock = self.state[position[1]][i]
			else:
				currentTileBlock = self.state[i][position[0]]

			if currentTileBlock != ' ' and currentTileBlock != lastBlock and currentTileBlock != processingBlock:
				count += 1
				lastBlock = currentTileBlock
				next_block = next(block for block in self.block_list if block.name == currentTileBlock)

				if not any(block for block in blockList if block.name == next_block.name):
					blockList.append(next_block)

			i += 1

		return count

	def clone(self):
		return deepcopy(self)