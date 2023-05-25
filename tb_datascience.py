import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
import math

headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"}

urlPag = f'https://exame.com/brasil/onde-ha-mais-pessoas-acima-do-peso-no-brasil/'

site = requests.get(urlPag, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
estados = soup.find_all('strong', class_=re.compile('gallery-title'))

estados.pop(28)
estados.pop(0)
iCountEstados = len(estados)


dicStatus = {'Posicao':[], 'Estado':[],'Total':[]}

for i in range(0, iCountEstados):
    posicao = i + 1
    if i == 9:
        dicStatus['Estado'].append(estados[i].text.split('–')[1].split('-')[0].strip())
        dicStatus['Total'].append(estados[i].text.split('–')[1].split('-')[1].split('%')[0])
    else:
        dicStatus['Estado'].append(estados[i].text.split('-')[1].strip())
        dicStatus['Total'].append(estados[i].text.split('-')[2].split('%')[0])
    
    dicStatus['Posicao'].append(posicao)

urlPag2 = f'https://www.geografiaopinativa.com.br/2016/02/lista-dos-estados-brasileiros-por.html'

site2 = requests.get(urlPag2, headers=headers)
soup2 = BeautifulSoup(site2.content, 'html.parser')
dadosHabitantes = soup2.find_all('td', class_=re.compile('xl65'))
iCountDadosHabitantes = len(dadosHabitantes)

dicHabitantes = {'Estado':[], 'Habitantes':[]}

for i in range(0, iCountDadosHabitantes):
    if i % 2 == 0:
        if i == 6 or i == 16:
            dicHabitantes['Estado'].append(dadosHabitantes[i].text.split()[0])
        else:
            dicHabitantes['Estado'].append(dadosHabitantes[i].text.strip())
    else:
        dicHabitantes['Habitantes'].append(''.join(dadosHabitantes[i].text.split()))


df = pd.DataFrame(dicStatus)
df.to_csv('statusObesidade.csv', encoding='UTF-8', sep=';')

df2 = pd.DataFrame(dicHabitantes)
df2.to_csv('habitantes.csv', encoding='UTF-8', sep=';')
