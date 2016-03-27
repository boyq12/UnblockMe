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
				pass
			else:
				for b in board.generate_move():
					if not any(board for board in self.open + self.close if b.state == board.state):
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