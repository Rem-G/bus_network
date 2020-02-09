from datetime import datetime
class Graph():

	def __init__(self, lines, stops):
		self.lines = lines
		self.stops = stops
		self.departure_time = None
		self.hollidays = False
		self.departure_stop = None

	def set_departure_stop(self, departure_stop):
		self.departure_stop = departure_stop

	def set_hollidays(self, hollidays):
		self.hollidays = hollidays

	def distance(self, time1, time2):
		'''
		:param time1 str: First time to compare
		:param time2 str: Second time to compare
		:return datetime: Return the time between time1 and time2
		'''
		if time2 == '-':
			d = datetime.strptime('00:00', '%H:%M')
			return d - d

		time_object1 = datetime.strptime(time1, '%H:%M')
		time_object2 = datetime.strptime(time2, '%H:%M')

		return time_object2 - time_object1

	def stop_value(self, stop_name):
		'''
		:return Stop object: Return the stop object associated to stop_name
		'''
		for stop in self.stops:
			if stop_name == stop.name:
				return stop

	def first_schedule(self, departure_stop, arrival_stop):
		'''
		:param stop object: departure stop
		:param duration str: actual duration of the journey
		:return list: Return the first schedule and its index 
		'''
		for line in arrival_stop.schedule.keys():
			for stop_time in arrival_stop.schedule[line]:
				if stop_time != '-' and datetime.strptime(stop_time, '%H:%M') >= datetime.strptime(departure_stop, '%H:%M'):
					return [stop_time, arrival_stop.schedule[line].index(stop_time)]

	def common_stops(self):
		'''
		:return list: Return the common stops of all the lines
		'''
		common_stops = list()
		for stop in self.stops:
			if len(stop.schedule) > 1:
				common_stops.append(stop)
		return common_stops

	def hours_mins_to_seconds(self, time):
		'''
		:param time str: Time to convert
		:return int: Return the converted time from str to int
		'''
		time = time.split(':')
		return int(time[0])*3600 + int(time[1])*60


	def direction(self, departure_stop, arrival_stop):
		'''
		:param departure_stop str: Beginning stop
		:param arrival_stop str: Arrival stop
		:return int: Return the direction 1/-1
		'''
		list_stops = list()
		common_stop_search = False
		list_stops_line = list()

		######Lines with their stops
		for list_line in self.lines:
			for line in list_line:
				for stop in line.stops:
					if stop.name not in list_stops_line:
						list_stops_line.append(stop.name)

				list_stops.append(list_stops_line[::-1])
				list_stops_line = list()

		######Verification if departure_stop and arrival_stop are on the same line
		for line in list_stops:
			if departure_stop in line and arrival_stop in line:
				if line.index(departure_stop) < line.index(arrival_stop):
					return 1 #Ordre de lecture classique
				return -1

		common_stop_search = True
		common_stops = self.common_stops()
		common_stop_save = None

		######Stops are not on the same line, we look for the first common stop
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

	def fastest(self, departure_stop, arrival_stop, hollidays, departure_time, journey_duration = '00:00'):
		'''
		:param departure_stop str:
		:param arrival_stop str:
		:param hollidays bool:
		:param departure_time str:
		:param journey_duration str:
		:return dict:
		'''
		self.set_hollidays(hollidays)

		if self.departure_stop is None:
			self.set_departure_stop(departure_stop)

		direction = self.direction(departure_stop, arrival_stop)

		departure_stop = self.stop_value(departure_stop)#Take the stop object associated to the departure stop name

		start_stop_schedule, index_start_stop_schedule = self.first_schedule(departure_time, departure_stop)

		if self.departure_time is None:
			self.departure_time = start_stop_schedule

		if departure_stop.name == arrival_stop:
			departure_stop = self.departure_stop
			self.departure_stop = None
			return {'Departure time' : self.departure_time,
					'Departure stop' : departure_stop,
					'Arrival stop' : arrival_stop.upper(),
					'Hollidays' : self.hollidays,
					'Journey duration' : journey_duration
					}


		if direction is 1:
			for line_group in self.lines:
				for line in line_group:
					if departure_stop in line.stops and self.hollidays is line.hollidays:
						if len(departure_stop.next_stop.keys()) > 1  and self.stop_value(arrival_stop) not in line.stops: #common_stop
							pass

						else:
							duration_to_next_stop = self.distance(start_stop_schedule, departure_stop.next_stop[line.name].schedule[line.name][index_start_stop_schedule])
							while duration_to_next_stop == '-':
								index_start_stop_schedule += 1
								duration_to_next_stop = self.distance(start_stop_schedule, departure_stop.next_stop[line.name].schedule[line.name][index_start_stop_schedule])

							journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

							journey_duration = journey_duration[0] + ':' + journey_duration[1]

							#FORK
							#We check if the right stop of the fork is our arrival stop
							if (departure_stop.next_stop[line.name].right_stop is not None
								and departure_stop.next_stop[line.name].right_stop.name == arrival_stop):

								return self.fastest(departure_stop.next_stop[line.name].name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)
							
							#We check if the left stop of the fork is our arrival stop
							elif (departure_stop.next_stop[line.name].left_stop is not None
								and departure_stop.next_stop[line.name].left_stop.name == arrival_stop):

								return self.fastest(departure_stop.next_stop[line.name].left_stop.name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)
							
							return self.fastest(departure_stop.next_stop[line.name].name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)
						
		else:
			for line_group in self.lines:
				for line in line_group:
					if departure_stop in line.stops and self.hollidays is line.hollidays:
						if len(departure_stop.previous_stop.keys()) > 1  and self.stop_value(arrival_stop) not in line.stops: #common_stop
							pass

						else:
							duration_to_next_stop = self.distance(start_stop_schedule, departure_stop.next_stop[line.name].schedule[line.name][index_start_stop_schedule])
							while duration_to_next_stop == '-':
								index_start_stop_schedule += 1
								duration_to_next_stop = self.distance(start_stop_schedule, departure_stop.next_stop[line.name].schedule[line.name][index_start_stop_schedule])

							journey_duration = str(datetime.strptime(str(journey_duration), '%H:%M') + duration_to_next_stop).split(' ')[1].split(':')[:2]

							journey_duration = journey_duration[0] + ':' + journey_duration[1]

							#FORK
							#We check if the right stop of the fork is our arrival stop
							if (departure_stop.previous_stop[line.name].right_stop is not None
								and departure_stop.previous_stop[line.name].right_stop.name == arrival_stop):

								return self.fastest(departure_stop.previous_stop[line.name].name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)
							
							#We check if the left stop of the fork is our arrival stop
							elif (departure_stop.previous_stop[line.name].left_stop is not None
								and departure_stop.previous_stop[line.name].left_stop.name == arrival_stop):

								return self.fastest(departure_stop.previous_stop[line.name].left_stop.name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)

							return self.fastest(departure_stop.previous_stop[line.name].name, arrival_stop, self.hollidays, start_stop_schedule, journey_duration)


	def shortest(self, departure_stop, arrival_stop, departure_time, dist = 0, checked_stops = list(), path = list(), index_start_stop_schedule = None):
		'''
		:param departure_stop str:
		:param arrival_stop str:
		:param departure_time str:
		:param dist int:
		:param checked_stops list:
		:param path list:
		:param index_start_schedule int:
		:return dict:
		'''
		if departure_stop == arrival_stop:
			time = datetime.fromtimestamp(dist - self.hours_mins_to_seconds(departure_time)).strftime("%H:%M")
			return {'Path': path, 'Duration' : time}

		departure_stop = self.stop_value(departure_stop)

		dist_neighbords = list()

		if not len(checked_stops):
			dist = self.hours_mins_to_seconds(departure_time)
			start_stop_schedule, index_start_stop_schedule = self.first_schedule(departure_time, departure_stop)

		for neighbord in departure_stop.neighbords:
			for line in neighbord:

				if (neighbord[line] is not None#Neighbord exists
					and neighbord[line].name not in checked_stops#Neighbord is not already checked
					and None not in neighbord[line].neighbords):#Check if there is no shapes in neighbords

					n = 0

					while neighbord[line].schedule[line][index_start_stop_schedule + n] == '-':
						n += 1

					dist_neighbord = self.hours_mins_to_seconds(neighbord[line].schedule[line][index_start_stop_schedule + n])

					dist_neighbords.append([neighbord[line], dist_neighbord])

		checked_stops.append(departure_stop.name)

		#If all the neighbords are already checked, we go back to the nearby common stop
		if not len(dist_neighbords):
			for stop in self.stops:
				if len(stop.schedule) > 1 and stop.name in checked_stops:
					for neighbord in stop.neighbords:#previous or next
						for s in neighbord.values():
							if s.name not in checked_stops:
								return self.shortest(stop.name, arrival_stop, departure_time, dist, checked_stops, path, index_start_stop_schedule)

		nearby_stop = dist_neighbords[0][0].name
		min_neighbord = dist_neighbords[0][1]

		for neighbord in dist_neighbords:
			if neighbord[0].name in checked_stops:
				index = dist_neighbords.index(neighbord)
				dist_neighbords.pop(index)

			if neighbord[1] < min_neighbord:#fWe take the shorter distance
				nearby_stop = neighbord[0].name
				min_neighbord = neighbord[1]

		dist += (min_neighbord - dist)
		path.append(nearby_stop)

		return self.shortest(nearby_stop, arrival_stop, departure_time, dist, checked_stops, path, index_start_stop_schedule)















