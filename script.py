import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_pdf(user, pwd):
	loginURL = 'https://portalacademico.ita.br/sg_web/default.aspx?escola=6748'

	payload = {
		'ScriptManager1': 'acessoUpdatePanel|btnEntrar',
		'__LASTFOCUS': '',
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'txtCodigo': user,
		'txtSenha': pwd,
		'cbLembrarCodigo': True,
		'codigoTextBox': user,
		'emailTextBox': '',
		'ASYNCPOST': 'true',
		'btnEntrar': 'Entrar',
		'ctl00$numeroSerieHiddenField': 6748,
	}

	headers={
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'
	}

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


