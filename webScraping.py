# Libs usadas: pandas, requests, openpyxl, lxml
import pandas as pd 
import requests
from openpyxl.workbook import Workbook

# Retorna os últimos confrontos entre os times x e y
def webScraping_headToHead(x, y):
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

	ids_times = {'palmeiras': '2248', 'internacional': '2245', 'fluminense': '2241', 'corinthians': '2234', 'flamengo': '2240', 'atletico_pr': '2230', 'atletico_mg': '2229', 
	'america_MG': '2227', 'sao_paulo': '2256', 'botafogo': '2233','fortaleza': '2239', 'santos': '2254', 'goias': '2244', 'bragantino': '3156', 'coritiba': '2235', 
	'cuiaba': '3220', 'ceara': '3183', 'atletico_go': '3129', 'avai': '2615', 'juventude': '2246'}

	url_link = "https://www.ogol.com.br/xray.php?id_comp=51&ond=r&epoca_ini=0&epoca_fim=0&equipa_id=" + ids_times[x] + "&equipa_vs_equipa_id=" + ids_times[y] + "&player_detail="
	req = requests.get(url_link, headers = header)
	df = pd.read_html(req.text)

	stats = df[5].copy()
	stats = stats[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 6']]

	number_rows = int(stats.tail(1).index.start)
	stats.drop([number_rows], inplace = True)
	stats = stats.rename(columns={'Unnamed: 2': 'Time_1', 'Unnamed: 3': 'Placar', 'Unnamed: 4': 'Time_2', 'Unnamed: 6': 'Ano_new'})

	new = stats["Placar"].str.split("-", n = 1, expand = True)
	stats["Gols_Time_1"] = new[0]
	stats["Gols_Time_2"] = new[1]
	stats.drop(columns =["Placar"], inplace = True)

	new = stats["Ano_new"].str.split(" ", n = 1, expand = True)
	stats["Ano"] = new[1]
	stats.drop(columns =["Ano_new"], inplace = True)

	time1 = stats.Time_1[0]
	time2 = stats.Time_2[0]

	print("")

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

	stats.to_excel("head_to_head/" + x + "_vs_" + y + ".xlsx")


# Retorna as posições no brasileirão do time x nos últimos anos
def webScraping_position(x):
	ids_times = {'palmeiras': '1023', 'internacional': '6600', 'fluminense': '2462', 'corinthians': '199', 'flamengo': '614', 'atletico_pr': '679', 'atletico_mg': '330', 
	'america_MG': '2863', 'sao_paulo': '585', 'botafogo': '537','fortaleza': '10870', 'santos': '221', 'goias': '3197', 'bragantino': '8793', 'coritiba': '776', 
	'cuiaba': '28022', 'ceara': '2029', 'atletico_go': '15172', 'avai': '2035', 'juventude': '10492'}

	header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}

	url_link = "https://www.transfermarkt.com.br/standart-team/platzierungen/verein/" + ids_times[x]
	req = requests.get(url_link, headers = header)
	df = pd.read_html(req.text)

	stats = df[1].copy()
	stats = stats[['Temporada', 'Pontos']]
	stats = stats.rename(columns={'Temporada': 'Temporada', 'Pontos': 'Colocação'})

	stats.to_excel("position/" + x + ".xlsx")