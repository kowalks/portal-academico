import requests
from bs4 import BeautifulSoup
import urllib3
import PyPDF2

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

loginURL = 'https://portalacademico.ita.br/sg_web/default.aspx?escola=6748'

payload = {
	'ScriptManager1': 'acessoUpdatePanel|btnEntrar',
	'__LASTFOCUS': '',
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'txtCodigo': '###LOGIN###',
	'txtSenha': '###SENHA###',
	'cbLembrarCodigo': True,
	'codigoTextBox': '###LOGIN###',
	'emailTextBox': '',
	'ASYNCPOST': 'true',
	'btnEntrar': 'Entrar',
	'ctl00$numeroSerieHiddenField': 6748,
}

headers={
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'
}

def get_pdf():
	session = requests.Session()	
	
	# Request login in page
	loginPage = session.get(loginURL, verify=False)
	requestURL = loginPage.url
	
	# Get hidden input form fields
	soup = BeautifulSoup(loginPage.text, 'lxml')
	hidden_tags = soup.find_all("input", type="hidden")
	for tag in hidden_tags:
		payload[tag['name']] = tag['value']
	
	# Log in into SofiA
	consulta = session.post(requestURL, data=payload)
	consultaURL = consulta.url

	# Get hidden input form fields
	soup = BeautifulSoup(consulta.text, 'lxml')
	hidden_tags = soup.find_all("input", type="hidden")
	for tag in hidden_tags:
		payload[tag['name']] = tag['value']
		
		
	# Request desired file
	payload['ctl00$ContentPlaceHolder1$matriculaDropDownList$primaDropDownList'] = soup.select_one('option[selected]')['value']
	payload['ctl00$ContentPlaceHolder1$relatorioAlunoDropDownList$primaDropDownList'] = -8
	payload['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$visualizarAlunoLinkButton'
	pdf = session.post(consultaURL, data=payload, headers=headers)
	
	# Write file in disk
	open('relatorio.pdf', 'wb').write(pdf.content)
	
def pdf_print():
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


get_pdf()
pdf_print()
