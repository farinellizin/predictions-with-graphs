# Libs usadas: pandas, requests, openpyxl, lxml
import pandas as pd 
import requests
from openpyxl.workbook import Workbook

# Retorna os últimos confrontos entre os times x e y
def webScraping_headToHead(x, y):
	# Header usado para fazer a requisição/web scraping nos mais diferentes navegadores sem que haja erro.
	header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}

	# Palmeiras = "2248"
	# Internacional = "2245"
	# Fluminense = "2241"
	# Corinthians = "2234"
	# Flamengo = "2240"
	# Atletico_PR = "2230"
	# Atletico_MG = "2229"
	# America_MG = "2227"
	# Sao_Paulo = "2256"
	# Botafogo = "2233"
	# Fortaleza = "2239"
	# Santos = "2254"
	# Goias = "2244"
	# Bragantino = "3156"
	# Coritiba = "2235"
	# Cuiaba = "3220"
	# Ceara = "3183"
	# Atletico_GO = "3129"
	# Avai = "2615"
	# Juventude = "2246"

	# IDs dos times com base no site em que será feito as requisições.
	ids_times = {'palmeiras': '2248', 'internacional': '2245', 'fluminense': '2241', 'corinthians': '2234', 'flamengo': '2240', 'atletico_pr': '2230', 'atletico_mg': '2229', 
	'america_MG': '2227', 'sao_paulo': '2256', 'botafogo': '2233','fortaleza': '2239', 'santos': '2254', 'goias': '2244', 'bragantino': '3156', 'coritiba': '2235', 
	'cuiaba': '3220', 'ceara': '3183', 'atletico_go': '3129', 'avai': '2615', 'juventude': '2246'}

	# Endereço do site em que será feito as requisições já utilizando os IDs dos times.
	url_link = "https://www.ogol.com.br/xray.php?id_comp=51&ond=r&epoca_ini=0&epoca_fim=0&equipa_id=" + ids_times[x] + "&equipa_vs_equipa_id=" + ids_times[y] + "&player_detail="

	# Salva o HTML da requisição feita na variável 'req'
	req = requests.get(url_link, headers = header)

	# Transforma o HTML em um array de dataframes divididos por tabela
	df = pd.read_html(req.text)

	# Copia o dataframe[5], que é onde de acordo com o site, está presente os jogos entre os dois times selecionados, para a variável 'stats'.
	stats = df[5].copy()

	# Manipula o dataframe, deixando apenas as colunas selecionadas abaixo, que representam, respectivamente, o time 1, o placar, o time 2 e o ano.
	stats = stats[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6']]

	#Busca o número de linhas que o dataframe possui e salva na variável 'number_rows'
	number_rows = int(stats.tail(1).index.start)

	# Remove a última linha, que salva lixo.
	stats.drop([number_rows], inplace = True)

	# Renomeia as colunas do dataframe para melhor visualização.
	stats = stats.rename(columns={'Unnamed: 2': 'Time_1', 'Unnamed: 3': 'Placar', 'Unnamed: 4': 'Time_2', 'Unnamed: 6': 'Ano_new'})

	# Esse bloco separa o placar em duas colunas, sendo uma coluna para os gols do time 1 e outra coluna para os gols do time 2.
	new = stats["Placar"].str.split("-", n = 1, expand = True)
	stats["Gols_Time_1"] = new[0]
	stats["Gols_Time_2"] = new[1]
	stats.drop(columns =["Placar"], inplace = True)

	# Esse bloco atualiza a tabela de ano de 'Brasileirão 2022' para '2022', como exemplo, para melhor usabilidade.
	new = stats["Ano_new"].str.split(" ", n = 1, expand = True)
	stats["Ano"] = new[1]
	stats.drop(columns =["Ano_new"], inplace = True)

	# Salva os nomes dos times nessas duas variáveis.
	time1 = stats.Time_1[0]
	time2 = stats.Time_2[0]

	print("")

	# Esse looping organiza o dataframe colocando o time 1 de um lado e o time 2 do outro lado.
	for i in range(number_rows):
		if stats.Time_1[i] == time2:
			temp1 = stats.Time_2[i]
			stats.Time_2[i] = stats.Time_1[i]
			stats.Time_1[i] = temp1

			temp2 = stats.Gols_Time_2[i]
			stats.Gols_Time_2[i] = stats.Gols_Time_1[i]
			stats.Gols_Time_1[i] = temp2

		print(stats.Time_1[i], "	", stats.Gols_Time_1[i], " x ", stats.Gols_Time_2[i], "	", stats.Time_2[i], "	-	Ano:", stats.Ano[i])

	print("\nSalvando estatísticas...\n")

	# Salva o dataframe em forma de tabela em um arquivo .xlsx
	stats.to_excel("head_to_head/" + x + "_vs_" + y + ".xlsx")

def arithmeticsPositionAverage(stats):
	boundary = stats.last_valid_index() + 1
	lvi = 17

	if (boundary != 17):
		desconsider = 17 - boundary
	else:
		desconsider = 0

	# print(f'{boundary} // {desconsider}')

	numerator = 0
	j = 1
	denominator = 0

	while j <= 17:
		denominator = denominator + j
		j = j + 1

	# print(f'BOUNDARY: {boundary}')

	for i in range(boundary + desconsider):
		if i < (boundary) and stats['Divisão'].iloc[i] != "Segunda Divisão":
			numerator = numerator + (stats['Colocação'].iloc[i] * (lvi / 17))
			# print(f"Primeira condição: {stats['Colocação'].iloc[i]} x {lvi / 17}")
		elif i < (boundary) and stats['Divisão'].iloc[i] == "Segunda Divisão":
			# print(f"Segunda condição: {16} x {lvi / 17}")
			numerator = numerator + (16 * (lvi / 17))
		elif i >= boundary:
			# print(f"Terçeira Condição: {20} x {lvi / 17}")
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