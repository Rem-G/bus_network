class Stop():

	def __init__(self, name):
		self.name = name
		self.schedule = {}
		self.previous_stop = dict()
		self.next_stop = dict()
		self.neighbords = [self.previous_stop, self.next_stop]
		self.left_stop = None
		self.right_stop = None

	def set_schedule(self, line, schedule):
		self.schedule[line] = schedule

	def set_next_stop(self, line, next_stop):
		self.next_stop[line] = next_stop

	def set_previous_stop(self, line, previous_stop):
		self.previous_stop[line] = previous_stop

	def set_left_stop(self, left_stop):
		self.left_stop = left_stop

	def set_right_stop(self, right_stop):
		self.right_stop = right_stop


