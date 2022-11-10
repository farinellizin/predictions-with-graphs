# Libs usadas: pandas, requests, openpyxl, lxml

import pandas as pd 
import requests
from openpyxl.workbook import Workbook

def webScraping():
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

	time_1 = input("Digite o time 1: ").lower()
	time_2 = input("Digite o time 2: ").lower()

	url_link = "https://www.ogol.com.br/xray.php?id_comp=51&ond=r&epoca_ini=0&epoca_fim=0&equipa_id=" + ids_times[time_1] + "&equipa_vs_equipa_id=" + ids_times[time_2] + "&player_detail="
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

	for x in range(number_rows):
		if stats.Time_1[x] == time2:
			temp1 = stats.Time_2[x]
			stats.Time_2[x] = stats.Time_1[x]
			stats.Time_1[x] = temp1

			temp2 = stats.Gols_Time_2[x]
			stats.Gols_Time_2[x] = stats.Gols_Time_1[x]
			stats.Gols_Time_1[x] = temp2

		print(stats.Time_1[x], "	", stats.Gols_Time_1[x], " x ", stats.Gols_Time_2[x], "	", stats.Time_2[x], "	-	Ano:", stats.Ano[x])

	print("\nSalvando estatísticas...\n")
	stats.to_excel("statistics.xlsx")