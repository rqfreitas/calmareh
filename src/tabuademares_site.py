#DOWNLOAD DO CPTEC-INPE PARA CSV
#ESCOLHE ANO E PORTO PARA BAIXAR O DOWNLOAD
import requests
import time
import re
import variables
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
column_names = ['dia','mes','hora','altura']
df = pd.DataFrame(columns = column_names)

#Retorna DataFrame com Marés do ano da cidade escolhida
def mares_cidade(url_cidade):
    column_names = ['dia','mes','hora','altura']
    df_cidade = pd.DataFrame(columns = column_names)

    browser.get(url_cidade)    
    for imes in range(12):
            mes = imes + 1
            browser.execute_script("Day('2022-"+str(mes)+"-01')") #SÓ ANO 2022
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            list_tabua = soup.find_all(class_="tabla_mareas_marea tabla_mareas_marea_border_bottom")
            imare = 1
            dia = 1
            for mareh in list_tabua:
                if imare == 5:
                    imare = 1
                    dia = dia + 1
                if mareh.contents:
                    altura = mareh.find(class_="tabla_mareas_marea_altura_numero").text
                    hora = mareh.find(class_ = regex).text.strip()
                else:
                    altura = 'n'
                    hora = 'n'
                print(str(mes) + '-'+hora+'-'+altura)
                imare = imare +1
                # LEMBRAR QUE A CADA 4 MUDA O DIA
                df_cidade = df_cidade.append({'dia':dia,'mes':mes, 'hora':hora, 'altura':altura}, ignore_index=True)


def mares_estado(url_estado):
    browser.get(url_estado)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    list_cidades = soup.find_all(class_='sitio_estacion_a')
    for cidade in list_cidades:
        city = cidade.find("div").select_one(":nth-child(2)").text
        #if cidade.has_attr('class') and cidade['class'][0] == 'section_lugar_pais':
        url_cidade = cidade['href']
        mares_cidade(url_cidade)

#Acessa o CPTEC e baixa dados do ano para determinado porto
regex = re.compile('tabla_mareas_marea_hora.*')
url = "https://tabuademares.com/br"
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8") #or soup = BeautifulSoup(html, from_encoding=encoding)
list_estados = soup.find_all(class_="sitio_reciente_a")
for estado in list_estados:
    uf = estado.text
    url_estado = estado['href']

    browser.get(url_estado)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    list_cidades = soup.find_all(class_='sitio_estacion_a')
    for cidade in list_cidades:
        city = cidade.find("div").select_one(":nth-child(2)").text

        
        
        #if cidade.has_attr('class') and cidade['class'][0] == 'section_lugar_pais':
        url_cidade = cidade['href']
        browser.get(url_cidade)
        
        for imes in range(12):
                mes = imes + 1
                browser.execute_script("Day('2022-"+str(mes)+"-01')")
                html = browser.page_source
                soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
                list_tabua = soup.find_all(class_="tabla_mareas_marea tabla_mareas_marea_border_bottom")
                imare = 1
                dia = 1
                for mareh in list_tabua:
                    print(list_tabua.previous_sibling)
                    if imare == 5:
                        imare = 1
                        dia = dia + 1
                    if mareh.contents:
                        altura = mareh.find(class_="tabla_mareas_marea_altura_numero").text
                        hora = mareh.find(class_ = regex).text.strip()
                    else:
                        altura = 'n'
                        hora = 'n'
                    print(str(mes) + '-'+hora+'-'+altura)
                    imare = imare +1
                    # LEMBRAR QUE A CADA 4 MUDA O DIA
                    df = df.append({'dia':dia,'mes':mes, 'hora':hora, 'altura':altura}, ignore_index=True)

        df.to_csv(( uf + '_' + city +'.csv'), mode='a', header=False)  

    
    

#tabla_mareas_marea_altura_numero
# Para cada porto - pega dados em Dataframe e salva no csv

            
            
