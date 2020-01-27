from datetime import datetime
class Graph():

	def __init__(self, lines, stops):
		self.lines = lines
		self.stops = stops

	def distance(self, time1, time2):
		'''
		'''
		if time2 == '-':
			d = datetime.strptime('00:00', '%H:%M')
			return d - d

		time_object1 = datetime.strptime(time1, '%H:%M')
		time_object2 = datetime.strptime(time2, '%H:%M')

		return time_object2 - time_object1

	def stop_value(self, stop_name):
		stops = dict()
		for stop in self.stops:
			if stop_name == stop.name:
				return stop

	def first_schedule(self, departure_stop, arrival_stop):
		'''
		:param stop object: departure stop
		:param duration str: actual duration of the journey
		'''
		for line in arrival_stop.schedule.keys():
			for stop_time in arrival_stop.schedule[line]:
				if stop_time != '-' and datetime.strptime(stop_time, '%H:%M') > datetime.strptime(departure_stop, '%H:%M'):
					return stop_time

	def fastest(self, start_stop, end_stop, departure_time, journey_duration = '00:00'):
		start_stop = self.stop_value(start_stop)
		
		start_stop_schedule = self.first_schedule(departure_time, start_stop)

		for line in start_stop.next_stop.keys():
			if start_stop.next_stop[line].name != end_stop:

				duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, start_stop.next_stop[line]))

				journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

				journey_duration = journey_duration[0] + ':' + journey_duration[1]

				print(start_stop.next_stop[line].name, end_stop, start_stop_schedule, journey_duration)

				return self.fastest(start_stop.next_stop[line].name, end_stop, start_stop_schedule, journey_duration)

			return [departure_time, end_stop, journey_duration]






