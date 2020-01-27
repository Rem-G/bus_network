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

def stops_line(name, line_type, file_path):
	type_elements = ['regular_date_go', 'regular_date_back']

	stops_lines = list()

	if line_type == 'we':
		type_elements = ['we_holidays_date_go', 'we_holidays_date_back']

	if '+' in elements(file_path, 'regular_path'):
		for type_element in type_elements:
			stops = elements(file_path, 'regular_path').split(' + ')
			dest1 = [stops[0]]
			dest2 = [stops[1].split(' N ')[0]]

			common_stops = stops[1].split(' N ')[1:]

			stops = [dest1 + common_stops, dest2 + common_stops]

			stops1 = stops2 = elements(file_path, type_element)

			for line in stops:
				for stop in line:
					if stop not in list(stops1.keys()):
						del stops1[stop]

					if stop not in list(stops1.keys()):
						del stops2[stop]

			stops_lines.append(stops1)
			stops_lines.append(stops2)

		return stops_lines

	else:
		for type_element in type_elements:
			stops_lines.append(elements(file_path, type_element))
		
	return stops_lines

def create_stops():
	list_stops = list()
	list_stops_name = list()
	stops = set()
	for file in data_file_name:
		list_stop = elements(file, 'regular_path').split(' + ')
		for s in list_stop:
			s = s.split(' N ')
			for e in s:
				stops.add(e)

	for stop in stops:
		list_stops.append(Stop(stop))
		list_stops_name.append(stop)


	return [list_stops, list_stops_name]

def create_line(file_path, name, line_type):
	stops = stops_line(name, line_type, file_path)
	lines = list()
	if len(stops) >= 2 and type(stops) is list:
		for stop in stops:
			line = Line(name, line_type, list_stops)
			line.create_stops_line(stop)
			lines.append(line)
	else:
		line = Line(name, line_type, list_stops)
		line.create_stops_line(stops)
		lines.append(line)

	return lines

#######Creation of stops and lines
list_stops, list_stops_name = create_stops()
list_lines = list()

########Ligne 1
list_lines.append(create_line(data_file_name[0], '1', 'reg'))

create_line(data_file_name[0], '1', 'we')

#######Ligne 2
list_lines.append(create_line(data_file_name[1], '2', 'reg'))

create_line(data_file_name[1], '2', 'we')

#######Creation of the graph
g = Graph(list_lines, list_stops, list_stops_name)
print(g.fastest('Chorus', 'PARC_DES_GLAISINS', '09:20'))
print(g.fastest('PARC_DES_GLAISINS', 'Chorus', '09:20'))
print(g.fastest('GARE', 'PISCINE-PATINOIRE', '09:20'))
print(g.fastest('POISY_COLLÈGE', 'PISCINE-PATINOIRE', '09:20'))


