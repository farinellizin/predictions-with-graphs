# Libs usadas: pandas, requests, openpyxl, lxml
import pandas as pd 
import requests
from openpyxl.workbook import Workbook

def arithmeticsPositionAverage(stats):
	boundary = stats.last_valid_index() + 1
	lvi = 17

	numerator = 0
	j = 1
	denominator = 0

	for j in range(18):
		denominator = denominator + (j/17)

	for i in range(17):
		if i < (boundary) and stats['Divisão'].iloc[i] != "Segunda Divisão":
			numerator = numerator + (stats['Colocação'].iloc[i] * (lvi / 17))
		elif i < (boundary) and stats['Divisão'].iloc[i] == "Segunda Divisão":
			numerator = numerator + (16 * (lvi / 17))
		elif i >= boundary:
			numerator = numerator + (20 * (lvi / 17))

		lvi = lvi - 1

	return (numerator/denominator)

# Retorna as posições no brasileirão do time x nos últimos anos
def webScraping_position(x):
	# IDs dos times com base no site em que será feito as requisições.
	ids_times = {'palmeiras': '1023', 'internacional': '6600', 'fluminense': '2462', 'corinthians': '199', 'flamengo': '614', 'atletico_pr': '679', 'atletico_mg': '330', 
	'america_MG': '2863', 'sao_paulo': '585', 'botafogo': '537','fortaleza': '10870', 'santos': '221', 'goias': '3197', 'bragantino': '8793', 'coritiba': '776', 
	'cuiaba': '28022', 'ceara': '2029', 'atletico_go': '15172', 'avai': '2035', 'juventude': '10492'}

	# Header usado para fazer a requisição/web scraping nos mais diferentes navegadores sem que haja erro.
	header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}

	# Endereço do site em que será feito as requisições já utilizando o ID do time a ser pesquisado.
	url_link = "https://www.transfermarkt.com.br/standart-team/platzierungen/verein/" + ids_times[x]

	# Salva o HTML da requisição feita na variável 'req'
	req = requests.get(url_link, headers = header)

	# Transforma o HTML em um array de dataframes divididos por tabela
	df = pd.read_html(req.text)

	# Copia o dataframe[1], que é onde de acordo com o site, está presente as colocações do time escolhido, para a variável 'stats'.
	stats = df[1].copy()

	# Manipula o dataframe, deixando apenas as colunas selecionadas abaixo, que representam, respectivamente, a temporada, a colocação e a divisão.
	stats = stats[['Temporada', 'Pontos', 'Liga.2']]

	# Renomeia as colunas para melhor visualização.
	stats = stats.rename(columns={'Temporada': 'Temporada', 'Pontos': 'Colocação', 'Liga.2': 'Divisão'})

	# Salva os dados do time em um arquivo .xlsx
	stats.to_excel("position/" + x + ".xlsx")
	return (arithmeticsPositionAverage(stats))