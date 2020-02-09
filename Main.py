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

def stops_line(name, hollidays, file_path):
	'''
	:param hollidays bool: Hollidays period True/False
	:param file_path str: path of the file to read
	:return stop_lines list: List of lines with their stops and schedules
	'''
	type_elements = ['regular_date_go', 'regular_date_back']

	stop_lines = list()

	if hollidays is True:
		type_elements = ['we_holidays_date_go', 'we_holidays_date_back']

	for type_element in type_elements:
		stop_lines.append(elements(file_path, type_element))

	return stop_lines

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

def create_line(file_path, name, hollidays):
	'''
	:param file_path str: Path of the file to read
	:param name str: Name of the file to create
	:param hollidays bool: Hollidays period True/False
	:return lines list: List of the created lines
	'''
	stops = stops_line(name, hollidays, file_path)
	lines = list()

	if len(stops) > 1 and type(stops) is list:
		line = Line(name, hollidays, list_stops)
		for stop in stops:
			line.create_stops_line(stop)
		lines.append(line)
	else:
		line = Line(name, hollidays, list_stops)
		line.create_stops_line(stops)
		lines.append(line)

	return lines

#######Creation of stops and lines
list_stops = create_stops()
list_lines = list()

########Line 1
list_lines.append(create_line(data_file_name[0], '1', False))

#Hollidays
list_lines.append(create_line(data_file_name[0], '1', True))

#######Line 2
list_lines.append(create_line(data_file_name[1], '2', False))

#Hollidays
list_lines.append(create_line(data_file_name[1], '2', True))

#######Creation of the graph
G = Graph(list_lines, list_stops)
print(G.fastest('Chorus', 'PARC_DES_GLAISINS', False, '09:20'), '\n')
print(G.fastest('PARC_DES_GLAISINS', 'Chorus', False, '09:20'), '\n')
print(G.fastest('PISCINE-PATINOIRE', 'POISY_COLLÈGE', False, '09:20'), '\n')
print(G.fastest('POISY_COLLÈGE', 'PISCINE-PATINOIRE', False, '09:20'), '\n')
print(G.fastest('POISY_COLLÈGE', 'LYCÉE_DE_POISY', False, '09:20'), '\n')
print(G.fastest('LYCÉE_DE_POISY', 'POISY_COLLÈGE', False, '09:20'), '\n')
print(G.fastest('POISY_COLLÈGE', 'CAMPUS', False, '07:40'), '\n')
print(G.fastest('LYCÉE_DE_POISY', 'CAMPUS', False, '07:40'), '\n')
print(G.fastest('POISY_COLLÈGE', 'CAMPUS', True, '07:40'), '\n')
print(G.fastest('LYCÉE_DE_POISY', 'CAMPUS', True, '07:40'), '\n')
print(G.fastest('GARE', 'VIGNIÈRES', False, '07:40'), '\n')
print(G.fastest('Vernod', 'GARE', False, '15:00'), '\n')
print(G.fastest('France_Barattes', 'GARE', False, '15:00'), '\n')



#print(G.shortest('Chorus', 'PARC_DES_GLAISINS', '07:40'))
#print(G.shortest('PISCINE-PATINOIRE', 'Vernod', '09:20'), '\n')
print(G.shortest('PISCINE-PATINOIRE', 'POISY_COLLÈGE', '09:20'), '\n')
#print(G.shortest('GARE', 'VIGNIÈRES', '09:20'), '\n')








