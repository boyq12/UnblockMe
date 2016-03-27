import pygame
from Block import *
from Movement import *
from Global import *
from copy import deepcopy

class Board(object):
	def __init__(self):
		super(Board, self).__init__()
		self.state = [[0 for x in range(6)] for x in range(6)]
		self.pos = (400, 50)
		self.block_list = []
		self.movement = None

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
						self.block_list.append(Block(self,
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

	def generate_move(self):
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

	#def getPosibleMove(self):
	#	num_block = len(self.blocks)
	#	result = [Board]
	#	for i in range(num_block):
	#		position = self.blocks[i].getPos()
	#		length = self.blocks[i].getLength()
	#		dir = self.blocks[i].getDir()
	#		j = 1
	#		if(dir == Direction.HORIZONTAL):
	#			while ((position[1] - j) >= 0 and (self.state[position[0]][position[1] - j] == ' ')):
	#				board = self
	#				j+=1
	#				board.move(board.blocks[i], dir, Move_Direction.LEFT, j)
	#				result.append(board)
	#			j = 1
	#			while (position[1] + length + j - 1) < 6 and (' ' == self.state[position[0]][position[1] - +length + j - 1]):
	#				board = self
	#				j+=1
	#				board.move(board.blocks[i], dir, Move_Direction.RIGHT, j)
	#				result.append(board)
	#		elif(dir == Direction.VERTICAL):
	#			while ((position[0] - j) >= 0 and (self.state[position[0] - j][position[1]] == ' ')):
	#				board = self
	#				j+=1
	#				board.move(board.blocks[i], dir, Move_Direction.UP,j)
	#				result.append(board)
	#			while (((position[0] + length + j - 1) < 6) and (self.state[position[0] + length + j - 1][position[1]] == ' ')):
	#				board = self
	#				j+=1
	#				board.move(board.blocks[i], dir, Move_Direction.DOWN,j)
	#				result.append(board)
	#	return result


	##move function
	#def move(self, block, dir, move_dir, move):
	#	row = block.getPos()[0]
	#	col = block.getPos()[1]
	#	index = self.blocks.index(block)
	#	length = block.getLength()
	#	if(dir == Direction.HORIZONTAL):
	#		if(move_dir == Move_Direction.LEFT):
	#			newpos = col - move
	#			for i in range(newpos, newpos + length):
	#				self.state[row][i] = self.blocks[index].getName()
	#			for i in range(newpos + length, col + length):
	#				self.state[row][i] = ' '
	#		elif move_dir == Move_Direction.RIGHT:
	#			newpos = col + move
	#			for i in range(col, newpos):
	#				self.state[row][i] = ' '
	#			for i in range(newpos, newpos + length):
	#				self.state[row][i] = self.blocks[index].getName()
	#		self.blocks[index].setColPos(newpos)
	#	elif(dir == Direction.VERTICAL):
	#		if(move_dir == Move_Direction.UP):
	#			newpos = row - move
	#			for i in range(newpos, newpos + length):
	#				self.state[i][col] = self.blocks[index].getName()
	#			for i in range(newpos + length, row + length):
	#				self.state[i][col] = ' '
	#		elif(move_dir == Move_Direction.DOWN):
	#			newpos = row + move
	#			for i in range(row, newpos):
	#				self.state[i][co] = ' '
	#			for i in range(newpos, newpos + length):
	#				self.state[i][col] = self.blocks[index].getName()
	#		self.blocks[index].setRowPos(newpos)

	#check goal:
	def is_win(self):
		block = next(x for x in self.block_list if x.name == 'x')
		x = block.coord[0] + block.length
		y = block.coord[1]

		while x < 6:
			if self.state[y][x] != ' ':
				return False
			x += 1

		return True

	#get heristic score
	def get_score(self):
		blockList = [Block]
		mainBlock = self.blocks[self.getIndexBlock('x')]
		score = 0
		i = 0
		if((mainBlock.getPos()[1] + mainBlock.getLength()) == 6):
			return 1
		blockList.append(mainBlock)
		while(i <= (len(blockList) - 1)):
			score -= self.countObstructure(blockList[i],blockList)
			i+=1
		return score

	#count Obstructure
	def count_obstructor(self, block, blockList):
		count = 0
		positon = block.getPos()
		processingBlock = block.getName()
		currentTileBlock = Block
		lastBlock = '0'
		for i in range(6):
			if i == 0 and block.getName == 'x':
				i = positon[1] + block.getLength()
				if(i == 6):
					break
			if block.getDir() == Direction.HORIZONTAL:
				currentTileBlock = self.state[positon[0]][i]
			else:
				currentTileBlock = self.state[positon[1]]
			if currentTileBlock == ' ' and currentTileBlock != lastBlock and currentTileBlock != processingBlock:
				count+=1
				lastBlock = currentTileBlock
				next_block = self.blocks[self.getIndexBlock(currentTileBlock)]
				if next_block not in blockList:
					blockList.append(next_block)
		return count

	def clone(self):
		return deepcopy(self)