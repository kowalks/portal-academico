import PyPDF2
import queue

def insertTab(str, pos):
	return str[:pos] + '\t' + str[pos:]


def pdf_open():
	pdf = open('relatorio.pdf', 'rb')
	lines = PyPDF2.PdfFileReader(pdf).getPage(0).extractText().splitlines()
	start = lines.index('HORÁRIA') + 1
	end = lines.index('RESUMO DO HISTÓRICO ESCOLAR - ')

	return lines[start:end]
	
def grade_parser(grades):
	q = queue.Queue()
	while(len(grades) > 0):
		if (grades[0] == 'S'):
			q.put('S')
			grades = grades[1:]
		elif (grades[1] == ','):
			q.put(grades[:3])
			grades = grades[3:]
		else:
			q.put(grades[:4])
			grades = grades[4:]
	
	str = ''
	size = q.qsize()
	while(q.qsize() > 0):
		str += q.get() + '\t'
	return str, size

def line_parser(line):
	# Get ID
	if (line[:2] == 'TG'):
		id = line[:3]
		str = line[3:]
	else:
		id = line[:6]
		str = line[6:]

	# Get Horas
	if (str[-2:-1] == '-'):
		horas = str[-7:]
		str = str[:-7]
	else:
		horas = ''
	
	# Get Optional Field
	if (str[0] == ' '):
		op = 'OP'
		str = str[7:]
	else:
		op = ''
	
	# Get order
	ord = str[0]
	str = str[1:]
	
	grades,size = grade_parser(str)
		
	return id+'\t'+op+'\t'+ ord + '\t' + grades + '\t'*(6-size) + horas	

def pdf_print():
	notas = pdf_open()
	
	print('\t\t\tP1\tP2\tM1\tExame\tM2\tM3\tHoras')

	for nota in notas:
		print(line_parser(nota))
