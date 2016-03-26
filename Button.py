from GameManager import *
from Object import *
from Scene import *

class Button(Object):
	def __init__(self):
		super(Button, self).__init__()

		self.image_normal = None
		self.image_hover = None
		self.type = None
		self.is_pressed = False
		self.orig_pos = None

	def init(self, image_path, image_highlight_path):
		""" Add 2 variables image_normal and image_highlight
		"""
		super(Button, self).init('Image', file_name = image_path, alpha = True)
		self.image_normal = pygame.image.load(image_path).convert_alpha()
		self.image_highlight = pygame.image.load(image_highlight_path).convert_alpha()

	def set_type(self, type):
		self.type = type

	def turn_off_highlight(self):
		self.orig_image = self.image = self.image_normal

	def turn_on_highlight(self):
		self.orig_image = self.image = self.image_highlight

	def press(self):
		self.is_pressed = True
		self.scale(0.95, 0.95)
		
		# Move to origin center
		self.orig_pos = self.rect.topleft
		translate_coefs = [math.ceil(x / 2) for x in list(map(operator.sub, self.orig_image.get_size(), self.image.get_size()))]
		self.translate(*translate_coefs)

	def unpress(self):
		self.is_pressed = False
		self.image = self.orig_image
		self.move_to(*self.orig_pos)

	def do_click(self):
		current_state = GameManager.instance().get_current_state()

		if self.button_type == 'play':
			GameManager.instance().change_state(ResourceManager.instance().menu_list['SelectMenu'])
		elif self.button_type == 'exit':
			GameManager.instance().exit()
		elif self.button_type == 'start':
			# Pass variable to next state
			current_state.add_shared_var({'mode': Game_mode.PvP})
			current_state.add_shared_var({'P1_team_ID': current_state.Team1})
			current_state.add_shared_var({'P2_team_ID': current_state.Team2})
			current_state.add_shared_var({'P1_formation': Formation[current_state.Formation1]})
			current_state.add_shared_var({'P2_formation': Formation[current_state.Formation2]})

			# Load match
			scene_path = ResourceManager.instance().scene_path_list['STADIUM1']
			GameManager.instance().change_state(Scene(scene_path))
		elif self.button_type == 'lt1':
			current_state.changeTeam(1, -1)
		elif self.button_type == 'rt1':
			current_state.changeTeam(1, 1)
		elif self.button_type == 'lt2':
			current_state.changeTeam(2, -1)
		elif self.button_type == 'rt2':
			current_state.changeTeam(2, 1)
		elif self.button_type == 'lf1':
			current_state.changeFormation(1, -1)
		elif self.button_type == 'rf1':
			current_state.changeFormation(1, 1)
		elif self.button_type == 'lf2':
			current_state.changeFormation(2, -1)
		elif self.button_type == 'rf2':
			current_state.changeFormation(2, 1)