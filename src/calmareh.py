#SALVA DADOS PARA CSV - Marinha ou CPTEC
#ESCOLHE O PORTO E ANO?
#GERA CABECALHO DO CALENDARIO
#EXTRAI CSV EM DOIS ARRAYS(hora e altura) POR DIA
#RODA O CSV E SALVA CADA EVENTO NO ICS
#INTERESSANTE FAZER POR ANO.

import requests
import time
import re
import portos_cptec
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import UnicodeDammit
import pandas as pd


# prepare the option for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--ignore-certificate-errors")
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options)

#Pandas - Dataframe
column_names = ['text']
df = pd.DataFrame(columns = column_names)

sera = "que deleta tudo"

def get_mare_porto(porto_info,ano):
    df_mares_ano = pd.DataFrame(columns = column_names)
    cod_porto = porto_info[0]
    for i in range(12):
        mes = str(i+1).zfill(2)
        url = portos_cptec.search_url + cod_porto + "&mes=" + mes + "&ano=" + ano
        browser.get(url)  
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8") #or soup = BeautifulSoup(html, from_encoding=encoding)
        list_tags = soup.find_all(class_="dados")
        for dia in list_tags:   
            teste = dia.text.strip()
            if teste != "":
                x = re.sub("\s\s\s","," , teste) 
                x = re.sub("/","," , x) 
                x = re.sub("([.]\d)(\d)","\\1,\\2" , x) 
                x = re.sub("(\d\d)(\d\d)","\\1,\\2" , x) 
                
                df_mares_ano = df_mares_ano.append({'text':x}, ignore_index=True)
    return df_mares_ano

# ACESSAR SITE
for p in portos_cptec.portos_br:
    ano = str(21)
    cod_porto = p[0]

    df = get_mare_porto(p,ano)
            
    df.to_csv(("../csv/"  + ano + '_' + cod_porto +'.csv'), mode='a', header=False)        
            
