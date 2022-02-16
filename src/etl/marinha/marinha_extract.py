#DOWNLOAD FEITO DO SITE TABUAADEMARES.COM
#ESCOLHE ANO E PORTO PARA BAIXAR O DOWNLOAD
import requests
import time
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import UnicodeDammit
import pandas as pd
import urllib


# prepare the option for the chrome driver

url_marinha = "https://www.marinha.mil.br/chm/tabuas-de-mare"
source_folder = "src/etl/marinha/"
dest_folder = "src/etl/marinha/"



options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--ignore-certificate-errors")
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options)

#Scrap url dos pdfs do site da marinha
def info_site_marinha():
    browser.get(url_marinha)
    #regiao  = browser.current_url.replace("https://tabuademares.com/", "").split("/")

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

    mares_estados = soup.find_all(class_="table-responsive")

    colunas=['estado', 'cidade', 'ano', 'url']
    df = pd.DataFrame([], columns=colunas)

    for me in mares_estados:
        data = []
        for c in me.find_all('tr'):
            cols = c.find_all('td')
            if cols != []:
                porto = cols[0].text.strip()
                estado = cols[3].text.strip()
                pdf = cols[1].find('a')['href']
                ano = porto[-4:]
                porto = porto[:-7]
                arq_tabela = dest_folder + estado + " - " + porto+".pdf"
                print(arq_tabela)
                df_mare =  pd.DataFrame({'estado':estado, 'cidade': porto, 'ano':ano ,'url': pdf},index=[0])
                                #mares_dia = []
                df = df.append(df_mare)
                    
    df.to_csv(dest_folder+ "Tabela Marés - "+ ano +".csv", sep=',',index=False)
            
#LÊ CSV E FAZ DOWNLOAD DAS TABELAS
def download_tabelas():
    with open(source_folder+"Tabelas Marés 2022.csv", 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        next(csv_reader, None)
        for row in csv_reader:
            url = row[3]
            nome = row[0]+ " - " +row[1] + " - "+ row[2]
            r = requests.get(url, allow_redirects=True)

            open(dest_folder + nome + ".pdf", 'wb').write(r.content)

    



        

          #  print(c.td[2].text)

download_tabelas()