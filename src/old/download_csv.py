#DOWNLOAD FEITO DO SITE TABUAADEMARES.COM
#ESCOLHE ANO E PORTO PARA BAIXAR O DOWNLOAD
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
ano = 2022


#Retorna DataFrame com Marés do ano da cidade escolhida
def mares_cidade(url_cidade, regiao_uf):
    column_names = ['dia','mes','maré']
    df_cidade = pd.DataFrame(columns = column_names)
    regex = re.compile('tabla_mareas_marea_hora.*')


    browser.get(url_cidade)
    regiao  = browser.current_url.replace("https://tabuademares.com/", "").split("/")
    pais = regiao[0]
    uf = regiao[1]
    city = regiao[2]

    for imes in range(4):
            mes = imes + 1
            browser.execute_script("Day('" + str(ano) + "-" + str(mes) + "-01')") #SÓ ANO 2022
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            tabela = soup.find("table", {"id": "tabla_mareas_swipe1"})
            #mes_todo = soup.find_all(class_="tabla_mareas_dia")
            regex_linhas = re.compile('tabla_mareas_fila tabla_mareas_fila_fondo(1|2|3)$')
            mes_todo = tabela.find_all(class_=regex_linhas)
            
            for tagsd in mes_todo:
                print(tagsd['class'][0])
            #print(mes_todo)
            for dia_info in mes_todo:
                #print(len(dia_todo))
                #dia_info = dia_todo.parent                       
                if dia_info is not None:
                    
                    dia = dia_info.findChild(class_="tabla_mareas_dia_numero").text.strip()
                    dia = dia.zfill(2)
                    
                    
                    mares_dia = dia_info.find_all(class_="tabla_mareas_marea tabla_mareas_marea_border_bottom")
                    m1 = [mares_dia[0].find(class_ = regex).text.strip(), mares_dia[0].find(class_="tabla_mareas_marea_altura_numero").text]
                    m2 = [mares_dia[1].find(class_ = regex).text.strip(), mares_dia[1].find(class_="tabla_mareas_marea_altura_numero").text]
                    m3 = [mares_dia[2].find(class_ = regex).text.strip(), mares_dia[2].find(class_="tabla_mareas_marea_altura_numero").text]
                    if mares_dia[3].contents:
                        m4 = [mares_dia[3].find(class_ = regex).text.strip(), mares_dia[3].find(class_="tabla_mareas_marea_altura_numero").text]
                    else:
                        m4 = ["",""]
                    mareh = [m1,m2,m3,m4]
                    print(dia+"/"+str(mes))
                    print(mareh)
                    df_cidade = df_cidade.append({'dia':dia,'mes':str(mes).zfill(2), 'maré':mareh}, ignore_index=True)
    df_cidade.to_csv((uf + '_' + city +'.csv'), mode='a', header=False)  


#Grava CSV com marés do ano para cada cidade do estado escolhido
def mares_estado(url_estado,regiao_uf):
    browser.get(url_estado)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
    list_cidades = soup.find_all(class_='sitio_estacion_a')
    for cidade in list_cidades:
        city = cidade.find("div").select_one(":nth-child(2)").text
        #if cidade.has_attr('class') and cidade['class'][0] == 'section_lugar_pais':
        url_cidade = cidade['href']
        mares_cidade(url_cidade, regiao_uf)


#Grava CSV com marés do ano para cada cidade de cada estado do pais escolhido
def mares_pais(url_pais):
    browser.get(url_pais)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8") #or soup = BeautifulSoup(html, from_encoding=encoding)
    list_estados = soup.find_all(class_="sitio_reciente_a")
    for estado in list_estados:
        regiao_uf = estado.find_previous_sibling(class_="cabecera_seccion").text.split(" ")[1]
        uf = estado.text
        url_estado = estado['href']
        mares_estado(url_estado,regiao_uf)        

def get_regiao(url):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8") #or soup = BeautifulSoup(html, from_encoding=encoding)
    list_estados = soup.find_all(class_="sitio_reciente_a")
    for estado in list_estados:
        regiao_uf = estado.find_previous_sibling(class_="cabecera_seccion").text.split(" ")[1]
        
        

       # tags_regiao = estado.previous_siblings
        #for t in tags_regiao:
        #    if t.has_attr("class"):
         #       classetudo = t['class']
          #      classe = t['class'][0]
          #      if classe  == "cabecera_seccion":
           #         print(t.text)
    
 
url2 = "https://tabuademares.com/br/pernambuco/recife"
#mares_cidade(url2)


get_regiao("https://tabuademares.com/br")


