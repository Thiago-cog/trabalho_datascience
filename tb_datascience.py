import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
import math

url = 'https://www.kabum.com.br/perifericos/headset-gamer'
headers = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

soupQtdItens = soup.find('div', id='listingCount').get_text().strip()
splitQtdItens = soupQtdItens.split(' ')
iQtdItens = splitQtdItens[0]

iUltimaPagina = math.ceil(int(iQtdItens)/20)

dicProdutos = {'desc':[], 'valor':[]}

for i in range(1,iUltimaPagina+1):
    urlPag = f'https://www.kabum.com.br/perifericos/headset-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(urlPag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        desc = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        valor = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        dicProdutos['desc'].append(desc)
        dicProdutos['valor'].append(valor)

df = pd.DataFrame(dicProdutos)
df.to_excel('levantamentoHeadsetGamer.xlsx')