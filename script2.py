import PyPDF2

pdf = open('relatorio.pdf', 'rb')
reader = PyPDF2.PdfFileReader(pdf)
page = reader.getPage(0)
string = page.extractText()
lines = string.splitlines()
start = lines.index('HORÁRIA') + 1
end = lines.index('RESUMO DO HISTÓRICO ESCOLAR - ')

notas = lines[start:end]

print('\t\t\tP1\tP2\tM1\tExame\tM2\tM3\tHoras')

for nota in notas:
	nota = nota + '#' 
	if(nota[:2] == 'TG'):
		nota = nota[:3] + '\t' + nota[3:]
	else:
		nota = nota[:6] + '\t' + nota[6:]
		
	if((pos := nota.find('OP'))!=-1):
		nota = nota[:pos-5] + 'OP\t' + nota[pos+2] + '\t' + nota[pos+3:]
	else:
		pos = nota.find('\t')
		nota = nota[:pos] + '\t\t' + nota[pos+1] + '\t' + nota[pos+2:]
	
	for i in range(0,len(nota)):
		char = nota[i]
		if (char == ','):
			nota = nota[:i+2] + '\t' + nota[i+2:]
			
	tabs = nota.count('\t')
	pos = nota.rfind('\t')
	nota = nota[:pos] + '\t'*(9-tabs) + nota[pos:] 
	nota = nota[:-1]

	print(nota)


