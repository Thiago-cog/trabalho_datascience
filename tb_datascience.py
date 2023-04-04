import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
import math

headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"}

iQtdItens = 254
iUltimaPagina = math.ceil(int(iQtdItens)/50)

dicStatus = {'Name':[], 'Name Short':[],'Position':[], 'PPG':[], 'FG':[], '3FG':[], 'FT':[]}

for i in range(1,iUltimaPagina+1):
    
    urlPag = f'https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?page={i}'
    site = requests.get(urlPag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    
    pages = soup.find_all('tr', class_=re.compile('TableBase-bodyTr'))
    
    for page in pages:

        soupJogadoresNameSplit = page.find('span', class_=re.compile('CellPlayerName--long')).get_text().split()
        soupJogadoresName = soupJogadoresNameSplit[0]+' '+soupJogadoresNameSplit[1]

        soupJogadoresNameShortSplit = page.find('span', class_=re.compile('CellPlayerName--short')).get_text().split()
        soupJogadoresNameShort = soupJogadoresNameShortSplit[0]+soupJogadoresNameShortSplit[1]

        soupJogadoresPosition = page.find('span', class_=re.compile('CellPlayerName-position')).get_text().split()

        soupJogadoresPPGSplit = page.find_all('td', class_=re.compile('TableBase-bodyTd--number'))
        soupJogadoresPPG = soupJogadoresPPGSplit[3].text.split()

        soupJogadoresFGSplit = page.find_all('td', class_=re.compile('TableBase-bodyTd--number'))
        soupJogadoresFG = soupJogadoresFGSplit[6].text.split()

        soupJogadores3FGSplit = page.find_all('td', class_=re.compile('TableBase-bodyTd--number'))
        soupJogadores3FG = soupJogadores3FGSplit[9].text.split()

        soupJogadoresFTSplit = page.find_all('td', class_=re.compile('TableBase-bodyTd--number'))
        soupJogadoresFT = soupJogadoresFTSplit[12].text.split()
        
        dicStatus['Name'].append(soupJogadoresName)
        dicStatus['Name Short'].append(soupJogadoresNameShort)
        dicStatus['Position'].append(soupJogadoresPosition[0])
        dicStatus['PPG'].append(soupJogadoresPPG[0])
        dicStatus['FG'].append(soupJogadoresFG[0])
        dicStatus['3FG'].append(soupJogadores3FG[0])
        dicStatus['FT'].append(soupJogadoresFT[0])

df = pd.DataFrame(dicStatus)
df.to_csv('statusNBA.csv', encoding='UTF-8', sep='|')