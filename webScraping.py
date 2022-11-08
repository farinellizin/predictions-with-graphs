import pandas as pd 
import requests
from openpyxl.workbook import Workbook

def webScraping():
	header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
		"X-Requested-With": "XMLHttpRequest"
	}

	url_link = "https://www.soccerstats.com/latest.asp?league=brazil"

	req = requests.get(url_link, headers = header)

	df = pd.read_html(req.text)

	stats = df[22]
	stats = stats[[0,1,2,3,4,5,6,7,8,9,11,12,13,14]]
	stats.drop([0], inplace = True)
	stats = stats.rename(columns={0: 'Colocação', 1: 'Time', 2: 'GP', 3: 'W', 4: 'D', 5: 'L', 6: 'GF', 7: 'GA', 8: 'GD', 9: 'Pts', 11: 'PPG', 12: 'PPG last 8', 13: 'CS', 14: 'FTS'})

	stats.to_excel("statistics.xlsx")