class Stop():

	def __init__(self, name):
		self.name = name
		self.schedule = {}
		self.previous_stop = None
		self.next_stop = None

	def set_schedule(self, line, schedule):
		self.schedule[line] = schedule

	def set_next_stop(self, next_stop):
		self.next_stop = next_stop

	def set_previous_stop(self, previous_stop):
		self.previous_stop = previous_stop


