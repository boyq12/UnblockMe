class State(object):
	def __init__(self):
		super(State, self).__init__()
		self.is_running = True

	def init(self):
		raise NotImplementedError

	def pause(self):
		self.is_running = False

	def resume(self):
		self.is_running = True

	def process_events(self, event):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def draw(self, screen):
		raise NotImplementedError