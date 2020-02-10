from Line import Line
from Stop import Stop
from Graph import Graph


data_file_name = ['data/1_Poisy-ParcDesGlaisins.txt', 'data/2_Piscine-Patinoire_Campus.txt']

def read_file(file_path):
	content = None
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			content = f.read()
	except OSError:
		# 'File not found' error message.
		print("File not found")

	return content

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def elements(file_path, type_element):
	content = read_file(file_path)

	slited_content = content.split("\n\n")
	if type_element == 'regular_path':
		regular_path = slited_content[0]
		return regular_path

	elif type_element == 'regular_date_go':
		regular_date_go = dates2dic(slited_content[1])
		return regular_date_go

	elif type_element == 'regular_date_back':
		regular_date_back = dates2dic(slited_content[2])
		return regular_date_back

	elif type_element == 'we_holidays_path':
		we_holidays_path = slited_content[3]
		return we_holidays_path

	elif type_element == 'we_holidays_date_go':
		we_holidays_date_go = dates2dic(slited_content[4])
		return we_holidays_date_go

	elif type_element == 'we_holidays_date_back':
		we_holidays_date_back = dates2dic(slited_content[5])
		return we_holidays_date_back

def stops_line(name, hollidays, file_path, go):
	'''
	:param hollidays bool: Hollidays period True/False
	:param file_path str: path of the file to read
	:return stop_lines list: List of lines with their stops and schedules
	'''
	if go == 'go':
		type_elements = 'regular_date_go'
	else:
		type_elements = 'regular_date_back'

	if hollidays is True:
		if go == 'go':
			type_elements = 'we_holidays_date_go'
		else:
			type_elements = 'we_holidays_date_back'

	return elements(file_path, type_elements)

def create_stops():
	'''
	Create stops objects
	:return list: List of created stops
	'''
	list_stops = list()
	stops = set()
	for file in data_file_name:
		list_stop = elements(file, 'regular_path').split(' + ')
		for s in list_stop:
			s = s.split(' N ')
			for e in s:
				stops.add(e)

	#FORK
	for stop in stops:
		if stop == 'Vernod':
			right_stop = Stop('LYCÉE_DE_POISY')
			left_stop = Stop('POISY_COLLÈGE')
			s = Stop(stop)
			s.set_left_stop(left_stop)
			s.set_right_stop(right_stop)

			list_stops.append(s)
			list_stops.append(left_stop)
			list_stops.append(right_stop)

		elif stop != 'LYCÉE_DE_POISY' and stop != 'POISY_COLLÈGE':
			list_stops.append(Stop(stop))

	return list_stops

def create_line(file_path, name, hollidays, list_stops, go):
	'''
	:param file_path str: Path of the file to read
	:param name str: Name of the file to create
	:param hollidays bool: Hollidays period True/False
	:return lines list: List of the created lines
	'''
	stops = stops_line(name, hollidays, file_path, go)
	lines = list()

	if len(stops) > 1 and type(stops) is list:
		line = Line(name, hollidays, list_stops, go)
		for stop in stops:
			line.create_stops_line(stop)
		lines.append(line)
	else:
		line = Line(name, hollidays, list_stops, go)
		line.create_stops_line(stops)
		lines.append(line)

	return lines

def main():
	'''
	Create stops, lines, graph and call the function
	'''

	#######Creation of stops and lines
	list_stops = create_stops()
	list_lines = list()

	########Line 1
	list_lines.append(create_line(data_file_name[0], '1', False, list_stops, 'go'))
	list_lines.append(create_line(data_file_name[0], '1', False, list_stops, 'back'))

	#Hollidays
	list_lines.append(create_line(data_file_name[0], '1', True, list_stops, 'go'))
	list_lines.append(create_line(data_file_name[0], '1', True, list_stops, 'back'))

	#######Line 2
	list_lines.append(create_line(data_file_name[1], '2', False, list_stops, 'go'))
	list_lines.append(create_line(data_file_name[1], '2', False, list_stops, 'back'))

	#Hollidays
	list_lines.append(create_line(data_file_name[1], '2', True, list_stops, 'go'))
	list_lines.append(create_line(data_file_name[1], '2', True, list_stops, 'back'))

	#######Creation of  graph
	G = Graph(list_lines, list_stops)

	option, departure_stop, arrival_stop, hollidays, departure_time = display()

	if option == 'Fastest':
		print('\n', G.fastest(departure_stop, arrival_stop, hollidays, departure_time))

	elif option == 'Shortest':
		print('\n', G.shortest(departure_stop, arrival_stop, departure_time))

	#print(G.fastest('Chorus', 'PARC_DES_GLAISINS', False, '09:20'), '\n')
	#print(G.fastest('PARC_DES_GLAISINS', 'Chorus', False, '09:20'), '\n')
	#print(G.fastest('PISCINE-PATINOIRE', 'POISY_COLLÈGE', False, '09:20'), '\n')
	#print(G.fastest('POISY_COLLÈGE', 'PISCINE-PATINOIRE', False, '09:20'), '\n')
	#print(G.fastest('POISY_COLLÈGE', 'LYCÉE_DE_POISY', False, '09:20'), '\n')
	#print(G.fastest('LYCÉE_DE_POISY', 'POISY_COLLÈGE', False, '09:20'), '\n')
	#print(G.fastest('POISY_COLLÈGE', 'CAMPUS', False, '07:40'), '\n')
	#print(G.fastest('LYCÉE_DE_POISY', 'CAMPUS', False, '07:40'), '\n')
	#print(G.fastest('POISY_COLLÈGE', 'CAMPUS', True, '07:40'), '\n')
	#print(G.fastest('LYCÉE_DE_POISY', 'CAMPUS', True, '07:40'), '\n')
	#print(G.fastest('GARE', 'VIGNIÈRES', False, '07:40'), '\n')
	#print(G.fastest('Vernod', 'GARE', False, '15:00'), '\n')
	#print(G.fastest('France_Barattes', 'GARE', False, '15:00'), '\n')



	#print(G.shortest('Chorus', 'PARC_DES_GLAISINS', '07:40'))
	#print(G.shortest('PISCINE-PATINOIRE', 'Vernod', '09:20'), '\n')
	#print(G.shortest('PISCINE-PATINOIRE', 'POISY_COLLÈGE', '09:20'), '\n')
	#print(G.shortest('GARE', 'VIGNIÈRES', '09:20'), '\n')
	#print(G.shortest('POISY_COLLÈGE', 'PISCINE-PATINOIRE', '09:20'))

def display():
	'''
	Request user decision and display the result
	'''
	options_algo_user = {0 : 'Fastest', 1 : 'Shortest'}
	stops_user = {0 : 'PARC_DES_GLAISINS', 1 : 'Ponchy', 2 : 'VIGNIÈRES', 3 : 'C.E.S._Barattes', 4 : 'France_Barattes', 5 : 'GARE', 6 : 'Mandallaz',
	7 : 'Chorus', 8 : 'Meythet_Le_Rabelais', 9 : 'Vernod', 10 : 'POISY_COLLÈGE' , 11 : 'LYCÉE_DE_POISY', 12 : 'CAMPUS' , 13 : 'Pommaries',
	14 : 'Impérial', 15 : 'Préfecture_Pâquier' , 16 : 'Bonlieu' , 17 : 'Courier', 18 : 'Place_des_Romains', 19 : 'Parc_des_Sports', 20 : 'Arcadium',
	21 : 'PISCINE-PATINOIRE'}

	print(options_algo_user)
	option = options_algo_user[int(input('Please choose a search algorithm : '))]

	print('\n', stops_user, '\n')
	departure_stop = stops_user[int(input('Please choose a departure stop : '))]
	arrival_stop = stops_user[int(input('Please choose an arrival stop : '))]

	hollidays = input('Are you on hollidays ? y/n : ')

	if hollidays == 'y':
		hollidays = True
	else:
		hollidays = False

	departure_time = input('When do you want to go ? HH:MM : ')

	return [option, departure_stop, arrival_stop, hollidays, departure_time]

if __name__ == "__main__":
    main()









