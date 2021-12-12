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

# prepare the option for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--ignore-certificate-errors")
options.add_argument('log-level=3')
browser = webdriver.Chrome(options=options)

column_names = ['text']
df = pd.DataFrame(columns = column_names)

ano = str(21)
# ACESSAR SITE
for p in variables.portos_br:
    for i in range(12):
        mes = str(i+1).zfill(2)
        url = variables.search_url + p[0] + "&mes=" + mes + "&ano=" + ano
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
            
    df.to_csv(('issomesmo.csv'), mode='a', header=False)        
            
