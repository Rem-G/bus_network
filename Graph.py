from datetime import datetime
class Graph():

	def __init__(self, lines, stops, stops_name):
		self.lines = lines
		self.stops = stops
		self.stops_name = stops_name
		self.departure_time = None

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

	def common_stops(self):
		common_stops = list()
		for stop in self.stops:
			if len(stop.schedule) > 1:
				common_stops.append(stop)
		return common_stops


	def direction(self, departure_stop, arrival_stop):
		'''
		'''
		list_stops = list()
		common_stop_search = False


		######Lines with their stops
		for list_line in self.lines:
			list_stops_line = list()
			for line in list_line:
				for stop in line.stops:
					if stop.name not in list_stops_line:
						list_stops_line.append(stop.name)
			list_stops.append(list_stops_line[::-1])


		######Verification if departure_stop and arrival_stop are on the same line
		for line in list_stops:
			if departure_stop in line and arrival_stop in line:
				if line.index(departure_stop) < line.index(arrival_stop):
					return 1 #Ordre de lecture classique
				return -1

		common_stop_search = True
		common_stops = self.common_stops()
		common_stop_save = None

		if common_stop_search:
			for line in list_stops:
				if departure_stop not in line and arrival_stop in line:
					for common_stop in common_stops:
						if line.index(common_stop.name) < line.index(arrival_stop):
							common_stop_save = common_stop

		for line in list_stops:
			if departure_stop in line and arrival_stop in line:
				if line.index(common_stop_save) < line.index(arrival_stop):
					return 1
				return -1

	def fastest(self, departure_stop, arrival_stop, departure_time, journey_duration = '00:00'):
		#print(self.direction(departure_stop, arrival_stop))
		#print(departure_stop, departure_time)

		if self.direction(departure_stop, arrival_stop) is 1:
			departure_stop = self.stop_value(departure_stop)
			
			start_stop_schedule = self.first_schedule(departure_time, departure_stop)

			if self.departure_time is None:
				self.departure_time = start_stop_schedule

			if departure_stop.name == arrival_stop:
				return [self.departure_time, arrival_stop.upper(), journey_duration]

			for line_group in self.lines:
				for line in line_group:
					if departure_stop in line.stops:
						if len(departure_stop.next_stop.keys()) > 1  and self.stop_value(arrival_stop) not in line.stops: #common_stop
							pass

						else:
							duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, departure_stop.next_stop[line.name]))

							journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

							journey_duration = journey_duration[0] + ':' + journey_duration[1]

							return self.fastest(departure_stop.next_stop[line.name].name, arrival_stop, start_stop_schedule, journey_duration)
						
		else:
			departure_stop = self.stop_value(departure_stop)
			
			start_stop_schedule = self.first_schedule(departure_time, departure_stop)

			if self.departure_time is None:
				self.departure_time = start_stop_schedule

			if departure_stop.name == arrival_stop:
				return [self.departure_time, arrival_stop.upper(), journey_duration]

			for line_group in self.lines:
				for line in line_group:
					if departure_stop in line.stops:
						if len(departure_stop.previous_stop.keys()) > 1  and self.stop_value(arrival_stop) not in line.stops: #common_stop
							pass

						else:
							duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, departure_stop.previous_stop[line.name]))

							journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

							journey_duration = journey_duration[0] + ':' + journey_duration[1]

							return self.fastest(departure_stop.previous_stop[line.name].name, arrival_stop, start_stop_schedule, journey_duration)
					

			# departure_stop = self.stop_value(departure_stop)
			
			# start_stop_schedule = self.first_schedule(departure_time, departure_stop)

			# for line in departure_stop.previous_stop.keys():
			# 	for l in self.lines:
			# 		for e in l:
			# 			print(e.name)
			# 			if departure_stop.previous_stop[line].name != arrival_stop and departure_stop in e.stops:

			# 				duration_to_next_stop = self.distance(start_stop_schedule, self.first_schedule(start_stop_schedule, departure_stop.previous_stop[line]))

			# 				journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

			# 				journey_duration = journey_duration[0] + ':' + journey_duration[1]

			# 				return self.fastest(departure_stop.previous_stop[line].name, arrival_stop, start_stop_schedule, journey_duration)


			# return [departure_time, arrival_stop, journey_duration]








