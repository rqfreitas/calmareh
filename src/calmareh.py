### CHECK BOOK NAMES
### CHECK CHAPTERS AND VERSES
### STORE BOOK AND BIBLE
import requests
import time
import re
import variables
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import UnicodeDammit
import pandas as pd

## ANO ESCOLHIDO
ano = str(21)

# prepare the option for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--ignore-certificate-errors")
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options)

#Pandas - Dataframe
column_names = ['text']
df = pd.DataFrame(columns = column_names)


# ACESSAR SITE
for p in variables.portos_br:
    cod_porto = p[0]
    for i in range(12):
        mes = str(i+1).zfill(2)
        url = variables.search_url + cod_porto + "&mes=" + mes + "&ano=" + ano
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
                
                df = df.append({'text':x}, ignore_index=True)
            
    df.to_csv((cod_porto + '_' + ano +'.csv'), mode='a', header=False)        
            
