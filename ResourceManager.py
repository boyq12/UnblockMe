from Global import Singleton, new_class
from Board import *

@Singleton
class ResourceManager():
	def __init__(self):
		self.scene_path_list = dict()
		self.image_path_list = []
		self.sound_path_list = []
		self.board_list = []

	def read_resources(self, file_name):
		with open(file_name) as file:
			self.read_scenes(file)
			self.read_image(file)
			self.read_sound(file)
			self.read_input(file)

	def read_scenes(self, file):
		scene_num = int(file.readline().strip().split(' ')[1])

		for i in range(scene_num):
			scene_type = file.readline().strip().replace('#', '')
			scene_path = file.readline().strip()
			self.scene_path_list.update({scene_type: scene_path})

	def read_image(self, file):
		image_num = int(file.readline().strip().split(' ')[1])

		for i in range(image_num):
			file.readline()
			image_path = file.readline().strip()
			self.image_path_list.append(image_path)

	def read_sound(self, file):
		sound_num = int(file.readline().strip().split(' ')[1])

		for i in range(sound_num):
			file.readline()
			sound_path = file.readline().strip()
			self.sound_path_list.append(sound_path)

	def read_input(self, file):
		input_num = int(file.readline().strip().split(' ')[1])

		for i in range(input_num):
			file.readline()
			input_path = file.readline().strip()
			self.board_list.append(self.read_board(input_path))

	def read_board(self, file_name):
		board = Board()

		with open(file_name) as file:
			for i in range(6):
				line = file.readline()
				for j in range(6):
					board.state[i][j] = line[j * 2]

		board.process()
		return board
					