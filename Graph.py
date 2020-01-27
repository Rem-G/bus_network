from datetime import datetime
class Graph():

	def __init__(self, lines, stops, stops_name):
		self.lines = lines
		self.stops = stops
		self.stops_name = stops_name

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

	def direction(self, departure_stop, arrival_stop):
		'''
		'''
		list_stops = list()
		for list_line in self.lines:
			list_stops_line = list()
			for line in list_line:
				for stop in line.stops:
					if stop.name not in list_stops_line:
						list_stops_line.append(stop.name)
			list_stops.append(list_stops_line)

		for line in list_stops:
			line = line[::-1]
			if departure_stop in line:
				if line.index(departure_stop) < line.index(arrival_stop):
					return 1 #Ordre de lecture classique
				return -1

	def fastest(self, departure_stop, arrival_stop, departure_time, journey_duration = '00:00'):		
		if self.direction(departure_stop, arrival_stop) is 1:
			departure_stop = self.stop_value(departure_stop)
			
			start_stop_schedule = self.first_schedule(departure_time, departure_stop)

			for line in departure_stop.next_stop.keys():
				if departure_stop.next_stop[line].name != arrival_stop:

					duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, departure_stop.next_stop[line]))

					journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

					journey_duration = journey_duration[0] + ':' + journey_duration[1]

					#print(start_stop.next_stop[line].name, end_stop, start_stop_schedule, journey_duration)

					return self.fastest(departure_stop.next_stop[line].name, arrival_stop, start_stop_schedule, journey_duration)


			return [departure_time, arrival_stop, journey_duration]

		else:
			departure_stop = self.stop_value(departure_stop)
			
			start_stop_schedule = self.first_schedule(departure_time, departure_stop)

			for line in departure_stop.previous_stop.keys():
				if departure_stop.previous_stop[line].name != arrival_stop:

					duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, departure_stop.previous_stop[line]))

					journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

					journey_duration = journey_duration[0] + ':' + journey_duration[1]

					return self.fastest(departure_stop.previous_stop[line].name, arrival_stop, start_stop_schedule, journey_duration)


			return [departure_time, arrival_stop, journey_duration]








