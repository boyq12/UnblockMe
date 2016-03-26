import pygame
import math
import operator
from copy import deepcopy
from Global import *

class Object(pygame.sprite.Sprite):
	"""This class represent object"""

	def __init__(self):
		super(Object, self).__init__()
		self.coefficients = Struct(angle = 0, scale_x = 1.0, scale_y = 1.0)
		self.orig_image = None
		self.image = None
		self.type = None
		self.rect = None
		self.mask = None
		self._layer = None
		
	def init(self, type, colorkey = WHITE, width = 0, height = 0, file_name = "", color = WHITE, line_width = 0, alpha = True):
		self.type = type

		if (type == 'Image'):
			if (alpha == True):
				self.image = pygame.image.load(file_name).convert_alpha()
			else:
				self.image = pygame.image.load(file_name).convert()
				self.image.set_colorkey(colorkey)
			
		elif (type == 'Circle' or type == 'Ellipse'):
			self.image = pygame.Surface([width, height])
			self.image.fill(colorkey)
			self.image.set_colorkey(colorkey)
			pygame.draw.ellipse(self.image, color, [0, 0, width, height], line_width)
			
		elif (type == 'Square' or type == 'Rectangle'):
			self.image = pygame.Surface([width, height])
			self.image.fill(colorkey)
			self.image.set_colorkey(colorkey)
			pygame.draw.rect(self.image, color, [0, 0, width, height], line_width)
			
		else:
			return False

		self.rect = self.image.get_rect()
		self.orig_image = self.image
		self.mask = pygame.mask.from_surface(self.image)
		self._layer = pygame.sprite.LayeredUpdates()._default_layer

	def set_layer(self, layer):
		self._layer = layer

	def update(self):
		pass
		
	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def move_to(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def translate(self, x, y):
		self.rect.x += x
		self.rect.y += y
		
	def rotate(self, angle):
		self.coefficients.rotate = angle
		self.image = pygame.transform.rotate(self.orig_image, angle)

	def scale(self, x, y):
		#self.coefficients.scale_x, self.coefficients.scale_y = x, y
		#self.orig_image = self.image = pygame.transform.scale(self.orig_image, [int(self.get_width() * x), int(self.get_height() * y)])
		#self.mask = pygame.mask.from_surface(self.image)
		#pos = self.get_pos()
		#self.rect = self.image.get_rect()
		#self.move_to(*pos)
		self.image = pygame.transform.scale(self.image, [int(self.get_width() * x), int(self.get_height() * y)])

	def scale_to(self, x, y):
		self.coefficients.scale_x, self.coefficients.scale_y = x, y
		self.image = pygame.transform.scale(self.orig_image, [x, y])
		self.mask = pygame.mask.from_surface(self.image)
		pos = self.get_pos()
		self.rect = self.image.get_rect()
		self.move_to(*pos)
		
	def change_color(self, color):
		if (self.type == 'Circle' or type == 'Ellipse'):
			pygame.draw.ellipse(self.image, color, [0, 0, self.width, self.height])
		elif (self.type == 'Square' or type == 'Rectangle'):
			self.image.fill(color)
		else:
			return

	def collide_point(self, point):
		mask = pygame.mask.from_surface(self.image)

		# Pixel perfect collision
		try:
			if (mask.get_at(point)):
				return True
		except Exception:
			pass

	def get_width(self):
		return self.image.get_width()

	def get_height(self):
		return self.image.get_height()

	def get_pos(self):
		return (self.rect.x, self.rect.y)

	def get_center_pos(self):
		return (self.rect.x + self.image.get_rect().centerx, self.rect.y + self.image.get_rect().centery)

	def get_angle(self):
		return self.coefficients.rotate

	def get_scale(self):
		return (self.coefficients.scale_x, self.coefficients.scale_y)

	def clone(self):
		object = deepcopy(self)
		return object

	def __deepcopy__(self, memo):
		cls = self.__class__
		object = cls.__new__(cls)
		memo[id(self)] = object

		for k, v in self.__dict__.items():
			if (k is 'font'):
				object.font = self.font
			elif (k is not 'mask'):
				setattr(object, k, deepcopy(v, memo))

		object.image = self.image.copy()
		object.orig_image = self.orig_image.copy()
		object.mask = pygame.mask.from_surface(object.image)

		return object

	def setImage(self,file_name):
		self.orig_image = self.image = pygame.image.load(file_name).convert_alpha()
		self.scale(self.coefficients.scale_x, self.coefficients.scale_y)
		self.rotate(self.coefficients.rotate)
		self.move_to(*self.get_pos())