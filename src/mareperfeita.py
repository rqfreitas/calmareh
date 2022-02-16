#resolver problema de + de 4 marés/dia
#rescrever csv
#transformar pra ics
import ast
import numpy as np
import os
from ast import literal_eval
from csv import reader
import pandas as pd

pdf_source = 'src/etl/marinha/csv_marinha/'
arquivo = 'Pernambuco - PORTO DE SUAPE - 2022.csv'
df = pd.read_csv(pdf_source+arquivo)


#df['data'] = df['data'].astype(str)
df['hora'] = df['hora'].astype(int)
df['mare'] = df['mare'].astype(float)

def mergulhar_manha():
    df_result = df[(df['mare'] < 0.4) & (df['hora'] > 800)& (df['hora'] < 1100)]
    df_result.to_csv('mergulhar_manha.csv')
    print(df_result)

path = 'csv/'
csv_files = os.listdir(path)
data_ini = "20220101"
utcdiff = 3
arquivo = "pernambuco_recife.csv"

mares_top = []

def mareh_baixa(mareh_array):
    baixa = []
    if mareh_array[0][1] < mareh_array[1][1]:
        baixa.append(mareh_array[0])
        baixa.append(mareh_array[2])
    else:
        baixa.append(mareh_array[1])
        if mareh_array[3][0] != "":
            baixa.append(mareh_array[3])
    return baixa

def funcao_antiga():
    with open(('csv/'+ arquivo), 'r') as read_obj:
        csv_reader = reader(read_obj)
        alarm  = False
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            lista_mares = ast.literal_eval(row[3])
            baixas = mareh_baixa(lista_mares)
            hora = baixas[0][0]
            mare = baixas[0][1]
            h = hora.split(":")[0]
            if int(h)< 11 and int(h) > 8 and (float(mare.replace(",","."))<0.4):
                #print(row)
                print(row[1]+"/"+row[2] + " - " + str(baixas) )
                mares_top.append(row)
    # print(mares_top)




mergulhar_manha()