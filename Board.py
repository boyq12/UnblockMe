import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self, size):
        super(Board, self).__init__()
        self.size = size
        self.block_list = []
        self.coord_goal_x = None
        self.coord_goal_y = None