class State(object):
	shared_var = dict()

	def __init__(self):
		super(State, self).__init__()
		self.is_running = True

	def init(self):
		raise NotImplementedError

	def pause(self):
		self.is_running = False

	def resume(self):
		self.is_running = True

	def process_key_press(self, key):
		raise NotImplementedError

	def process_events(self, event):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def draw(self, screen):
		raise NotImplementedError

	def add_shared_var(self, dict):
		State.shared_var.update(dict)

	def get_shared_var(self, key):
		return State.shared_var[key]