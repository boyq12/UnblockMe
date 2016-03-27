import pygame
import operator
import random
import collections
from itertools import chain
from ResourceManager import *
from Global import *
from BlockSprite import *
from Board import *
from Block import *
from Button import *
from State import *
from Text import *
from AIManager import *

class Scene(State):
	def __init__(self, file_path):
		super(Scene, self).__init__()

		pygame.mixer.init(44100, -16, 4, 2048)
		self.all_object_list = pygame.sprite.LayeredUpdates()
		self.blocks = dict() # Prototype
		self.main_block = BlockSprite()
		self.background = Object()
		self.current_button = None
		self.button_list = []
		self.block_list = []
		self.sound_list = dict()
		self.current_stage = 0
		self.board = None
		self.stage_text = Text('Monotype Corsiva', 38, bold = True, color = (200, 50, 0))

		self.is_mouse_pressed = False
		self.is_drag = False
		self.orig_mouse_pos = None
		self.orig_block_pos = None
		self.current_block_margin = [0, 0]
		self.current_block = None

		self.game_mode = Game_mode.NORMAL
		self.is_solve = False
		self.is_moving = False
		self.speed = 5
		self.velocity = None
		self.goal = None

		# Load scene's resources
		self.read_scene(file_path)

	def init(self):
		# Set board
		self.change_stage()

		# Set stage text position
		self.stage_text.move_to(605, 5)
		self.stage_text.set_text('STAGE 1')
		self.all_object_list.add(self.stage_text)

		# Set background music
		pygame.mixer.stop()
		self.sound_list['background'].play().set_endevent(pygame.constants.USEREVENT)

	def process_key_press(self, key):
		pass

	def process_events(self, event):
		if event.type == pygame.USEREVENT:
			self.sound_list['background'].play()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if self.current_button is not None:
				self.is_mouse_pressed = True
				self.current_button.press()
			else:
				self.process_raycast_block()
		elif event.type == pygame.MOUSEBUTTONUP:
			if self.current_button is not None:
				self.is_mouse_pressed = False
				self.current_button.unpress()

				if self.is_mouse_hover:
					self.process_button_click()
			elif self.is_drag is True:
				self.is_drag = False
				self.orig_mouse_pos = None
				self.orig_block_pos = None
				self.confirm_block_pos()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if self.is_running:
					self.pause()
				else:
					self.resume()

	def update(self):
		if (not self.is_running):
			return

		# Update all objects
		self.all_object_list.update()

		if self.game_mode is Game_mode.NORMAL:
			if self.is_drag is True:
				self.process_drag()
			else:
				self.process_raycast_button()
		else:
			if self.is_moving:
				if self.current_block.block.direction == Direction.HORIZONTAL and self.current_block.rect.x == self.goal \
					or self.current_block.block.direction == Direction.VERTICAL and self.current_block.rect.y == self.goal:
					self.is_moving = False
					self.confirm_block_pos()
				else:
					if self.current_block.block.direction == Direction.HORIZONTAL:
						self.current_block.translate(self.velocity, 0)
					else:
						self.current_block.translate(0, self.velocity)
			else:
				movement = AIManager.instance().get_next_move()

				if movement is not None:
					self.current_block = next(block for block in self.block_list if block.block.name == movement.name)
					self.goal = (self.current_block.block.position[0] if self.current_block.block.direction == Direction.HORIZONTAL \
									else self.current_block.block.position[1]) + movement.step * 100
					self.velocity = self.speed * sign(movement.step)
					self.is_moving = True
					print(movement.name + ' ' + str(movement.step) + ' ' + str(self.velocity) + ' ' + self.current_block.block.name)
				else:
					self.is_moving = False
					self.game_mode = Game_mode.NORMAL

	def draw(self, screen):
		screen.fill(BLACK)
		self.all_object_list.draw(screen)

	def reset_game(self):
		self.calculate_position()
		self.match_state = Match_state.KICKOFF

	#--------------------------------------LOGIC PROCESSING SECTION-----------------------------------------------
	def process_raycast_button(self):
		mouse_pos = pygame.mouse.get_pos()

		button = next((button for button in self.button_list if button.rect.collidepoint(mouse_pos)), None)

		if button is not None:
			self.is_mouse_hover = True
			
			if self.current_button is None and self.is_mouse_pressed is False:
				self.current_button = button
				self.current_button.turn_on_highlight()
		else:
			self.is_mouse_hover = False
			
			if self.current_button is not None and self.is_mouse_pressed is False:
				self.current_button.turn_off_highlight()
				self.current_button = None

	def process_button_click(self):
		if self.current_button.type == 'EXIT':
			GameManager.instance().exit()
		elif self.current_button.type == 'LEFT_ARROW':
			self.current_stage = (self.current_stage - 1) % 11
			self.stage_text.set_text('STAGE ' + str(self.current_stage + 1))
			self.change_stage()
		elif self.current_button.type == 'RIGHT_ARROW':
			self.current_stage = (self.current_stage + 1) % 11
			self.stage_text.set_text('STAGE ' + str(self.current_stage + 1))
			self.change_stage()
		elif self.current_button.type == 'RESET':
			self.change_stage()
		elif self.current_button.type == 'DFS':
			self.game_mode = Game_mode.AUTO
			self.is_solve = AIManager.instance().solve(self.board, Algorithm.DFS)
		elif self.current_button.type == 'BFS':
			self.game_mode = Game_mode.AUTO
			self.is_solve = AIManager.instance().solve(self.board, Algorithm.BFS)
		elif self.current_button.type == 'HCL':
			self.game_mode = Game_mode.AUTO
			self.is_solve = AIManager.instance().solve(self.board, Algorithm.HCL)

	def process_raycast_block(self):
		mouse_pos = pygame.mouse.get_pos()

		block = next((block for block in self.block_list if block.rect.collidepoint(mouse_pos)), None)

		if block is not None:
			self.is_drag = True
			self.orig_mouse_pos = mouse_pos
			self.orig_block_pos = block.block.position
			self.current_block = block
			self.get_block_margin()

	def process_drag(self):
		mouse_pos = pygame.mouse.get_pos()
		new_pos = None

		if self.current_block.block.direction is Direction.HORIZONTAL:
			dx = mouse_pos[0] - self.orig_mouse_pos[0]
			new_pos = [self.orig_block_pos[0] + dx, self.orig_block_pos[1]]

			if new_pos[0] < self.current_block_margin[0]:
				new_pos[0] = self.current_block_margin[0]
			elif new_pos[0] > self.current_block_margin[1]:
				new_pos[0] = self.current_block_margin[1]
		else:
			dy = mouse_pos[1] - self.orig_mouse_pos[1]
			new_pos = [self.orig_block_pos[0], self.orig_block_pos[1] + dy]

			if new_pos[1] < self.current_block_margin[0]:
				new_pos[1] = self.current_block_margin[0]
			elif new_pos[1] > self.current_block_margin[1]:
				new_pos[1] = self.current_block_margin[1]

		self.current_block.move_to(*new_pos)
			

	def confirm_block_pos(self):
		self.current_block.block.position[0] = round(self.current_block.rect.x / 100) * 100
		self.current_block.block.position[1] = round(self.current_block.rect.y / 100 + 0.5) * 100 - 50
		self.current_block.block.coord[0] = int((self.current_block.block.position[0] - 400) / 100)
		self.current_block.block.coord[1] = int((self.current_block.block.position[1] - 50) / 100)
		self.board.update_block(self.current_block.block)
		self.current_block.move_to(*self.current_block.block.position)

	def get_block_margin(self):
		if self.current_block.block.direction is Direction.HORIZONTAL:
			x = self.current_block.block.coord[0] - 1
			y = self.current_block.block.coord[1]

			while x >= -1:
				if x is -1:
					self.current_block_margin[0] = 400
				elif self.board.state[y][x] is not ' ':
					self.current_block_margin[0] = 400 + (x + 1) * 100
					break

				x -= 1

			x = self.current_block.block.coord[0] + self.current_block.block.length

			while x <= 6:
				if x is 6:
					self.current_block_margin[1] = 1000 - self.current_block.block.length * 100
				elif self.board.state[y][x] is not ' ':
					self.current_block_margin[1] = 400 + (x - self.current_block.block.length) * 100
					break

				x += 1

		else:
			x = self.current_block.block.coord[0]
			y = self.current_block.block.coord[1] - 1

			while y >= -1:
				if y is -1:
					self.current_block_margin[0] = 50
					break
				if self.board.state[y][x] is not ' ':
					self.current_block_margin[0] = 50 + (y + 1) * 100
					break

				y -= 1

			y = self.current_block.block.coord[1] + self.current_block.block.length

			while y <= 6:
				if y is 6:
					self.current_block_margin[1] = 650 - self.current_block.block.length * 100
					break
				if self.board.state[y][x] is not ' ':
					self.current_block_margin[1] = 50 + (y - self.current_block.block.length) * 100
					break

				y += 1

	def change_stage(self):
		self.board = ResourceManager.instance().board_list[self.current_stage].clone()
		self.map_block()

	def map_block(self):
		self.all_object_list.remove(self.main_block)
		self.all_object_list.remove(self.block_list)
		self.block_list.clear()
		block_sprite = None

		for block in self.board.block_list:	
			if block.name is 'x':
				block_sprite = self.main_block
			else:
				if block.direction is Direction.HORIZONTAL:
					if block.length is 2:
						block_sprite = self.blocks['HORIZONTAL_BLOCK_SHORT'].clone()
					else:
						block_sprite = self.blocks['HORIZONTAL_BLOCK_LONG'].clone()
				else:
					if block.length is 2:
						block_sprite = self.blocks['VERTICAL_BLOCK_SHORT'].clone()
					else:
						block_sprite = self.blocks['VERTICAL_BLOCK_LONG'].clone()

			block_sprite.set_block(block)
			block_sprite.move_to(*block.position)
			self.block_list.append(block_sprite)
			self.all_object_list.add(block_sprite)

	#----------------------------------------READ FILE SECTION-----------------------------------------------------
	def read_scene(self, file_path):
		with open(file_path) as file:
			self.read_background(file)
			self.read_main_block(file)
			self.read_blocks(file)
			self.read_buttons(file)
			self.read_sound(file)

	def read_background(self, file):
		file.readline()
		image_id = int(file.readline().strip().split(' ')[1])
		self.background.init('Image', file_name = ResourceManager.instance().image_path_list[image_id])
		self.background.scale_to(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.all_object_list.add(self.background)

	def read_main_block(self, file):
		file.readline()
		image_id = int(file.readline().strip().split(' ')[1])
		self.main_block.init('Image', file_name = ResourceManager.instance().image_path_list[image_id])

	def read_blocks(self, file):
		block_num = int(file.readline().strip().split(' ')[1])

		for i in range(block_num):
			block_type = file.readline().strip().replace('#', '')
			image_id = int(file.readline().strip().split(' ')[1])
			block = BlockSprite()
			block.init('Image', file_name = ResourceManager.instance().image_path_list[image_id])
			self.blocks.update({block_type: block})

	def read_buttons(self, file):
		button_num = int(file.readline().strip().split(' ')[1])

		for i in range(button_num):
			button_type = file.readline().strip().replace('#', '')
			image_id = list(map(int, file.readline().strip().split(' ')[1:]))
			button = Button()
			button.init(ResourceManager.instance().image_path_list[image_id[0]], ResourceManager.instance().image_path_list[image_id[1]])
			button.translate(*map(int, file.readline().strip().split(' ')[1:]))
			button.set_type(button_type)
			self.button_list.append(button)
			self.all_object_list.add(button)

	def read_sound(self, file):
		sound_num = int(file.readline().strip().split(' ')[1])

		for i in range(sound_num):
			sound_type = file.readline().strip().replace('#', '')
			sound_id = int(file.readline().strip().split(' ')[1])
			sound = pygame.mixer.Sound(ResourceManager.instance().sound_path_list[sound_id])
			self.sound_list.update({sound_type: sound})