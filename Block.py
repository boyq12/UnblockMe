import pygame
from Global import *

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.coord_x = None
        self.coord_y = None
        self.length = None
        self.direction = Direction.HORIZONTAL

