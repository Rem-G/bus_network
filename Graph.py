
class Graph():

	def __init__(self, lines, stops):
		self.lines = lines
		self.stops = stops


	def distance(self, hour):
		hour = hour.split(':')
		return (hour[0]*60) + hour[1]