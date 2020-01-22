
class Line():

	def __init__(self, name, line_type, list_stops):
		self.name = name
		self.line_type = line_type #we -> weekend/vacances/jours fériés, reg -> semaine
		self.stops = []
		self.list_stops = list_stops

	def set_stop(self, stop):
		self.stops.append(stop)

	def stops_name(self):
		stops = list()
		stops = [stop.name for stop in self.stops]
		return stops

	def create_stops_line(self, stops, previous_stop = None):
		"""
		Link stops to lines and add line schedule to the stop
		"""
		if len(stops):
			keys = list(stops.keys())

			for stop in self.list_stops:
				if stop.name == keys[0]:
					stop.set_previous_stop(previous_stop)
					stop.set_schedule(self.name, stops[keys[0]])

					if previous_stop is not None:
						previous_stop.set_next_stop(stop)

					self.set_stop(stop)

					previous_stop = stop
					del stops[keys[0]]

					self.create_stops_line(stops, stop)

