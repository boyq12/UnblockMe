import math
from enum import Enum

# Window config
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# Enum
Direction = Enum('Direction', 'HORIZONTAL, VERTICAL')
Algorithm = Enum('Algorithm', 'DFS BFS HCL')
Game_state = Enum('Game_state', 'RUNNING STOP')
Game_mode = Enum('Game_mode', 'NORMAL AUTO')
Team_side = Enum('Team side', 'LEFT RIGHT')
Match_state = Enum('Match_state', 'PLAYING GOAL KICKOFF PAUSE')
Formation = [[1, 3, 4, 3], [1, 3, 5, 2], [1, 4, 3, 3], [1, 4, 4, 2], [1, 4, 5, 1], [1, 5, 3, 2], [1, 5, 4, 1]]
Team_name = ['ACM', 'AMA', 'ARS', 'BAR', 'BDO', 'BMU', 'CHE', 'INT', 'JUV', 'LIV', 'MNC', 'MUN']

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ROYALBLUE = (65, 105, 255)
YELLOW = (255, 255, 0)

RM_path = 'Resources/Managers/RM.txt'

# Common function
def rotate_point(point, center, angle):
	""" Rotate a point around another point
	"""
	angle = math.radians(angle)
	x = center[0] + (point[0] - center[0]) * math.cos(angle) - (point[1] - center[1]) * math.sin(angle);
	y = center[1] - (point[0] - center[0]) * math.sin(angle) + (point[1] - center[1]) * math.cos(angle);
	return (x, y)

def apply_all(seq, func, *args, **kwargs):
	"""Usage: pass function's name as string for calling object's method, otherwise pass function's name
	"""
	for obj in seq:
		if (isinstance(func, str)):
			getattr(obj, func)(*args, **kwargs)
		else:
			func(*args, **kwargs)

def new_class(Class, *args, **kwargs):
    return Class(*args, **kwargs)

def sign(num):
	return -1 if num < 0 else 1

# Common class
class Struct:
     def __init__(self, **kwds):
         self.__dict__.update(kwds)

# Common design pattern
class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. 
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)