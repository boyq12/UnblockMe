from Global import *

@Singleton
class AIManager(object):
	def __init__(self):
		self.open = []
		self.close = []
		self.moves = []

	def solve(self, bo, algorithm):
		self.open.append(bo)

		while self.open:
			board = self.open.pop(0)
			self.close.append(board)

			if board.is_win():
				self.moves = self.close
				self.moves.pop(0)
				return True

			if algorithm is Algorithm.HCL:
				g = None
				f = board.get_score()
								
				self.open.clear()
							
				for b in board.generate_moves():
					g = b.get_score()
					
					if g > f:
						self.open.insert(0, b)
						break
					
					if g == f:
						if not any(board for board in self.close if b.state == board.state):
							self.open.append(b)
			else:
				for b in board.generate_moves():
					exist = any(board for board in self.open if b.state == board.state) or \
								any(board for board in self.close if b.state == board.state)
					if not exist:
						if algorithm is Algorithm.DFS:
							self.open.insert(0, b)
						else:
							self.open.append(b)

		return False

	def get_next_move(self):
		if self.moves:
			return self.moves.pop(0).movement
		else:
			return None