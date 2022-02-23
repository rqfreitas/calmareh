
import numpy as np
import os
from ast import literal_eval
from csv import reader
import pandas as pd
from calendar import monthrange
import datetime

csv_source = 'src/etl/marinha/csv_marinha/'
ics_dest = 'ics/'
arquivo = 'Pernambuco - PORTO DE SUAPE - 2022.csv'
utcdiff = 3


########################################################
################ METODOS AUXILIARES  ###################
########################################################

def tz(zona, utcdiff):
    tz_string = "\nBEGIN:VTIMEZONE\nTZID:"+ zona+ "\nX-LIC-LOCATION:"+ zona+ "America/Sao_Paulo\nBEGIN:STANDARD\nTZOFFSETFROM:-"+ str(utcdiff).zfill(2) +"00\nTZOFFSETTO:-"+ str(utcdiff).zfill(2) +"00\nTZNAME:-"+ str(utcdiff).zfill(2) +"\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE"
    return tz_string    


def descricao_sinalizada(df_mareh): #MONTA DESSCRIÇÃO COM ICONES DE MARÉ BAIXA
    seta1 = "🔺"
    seta2 = "🔹"
    troca = ""
    indice_gravacao = 1
    descricao_mareh = ""

    df_mareh['hora'] = df_mareh['hora'].astype(str)
    df_mareh['hora'] = df_mareh['hora'].str.zfill(4)
    df_mareh['mare'] = df_mareh['mare'].astype(str)

    hora_array = df_mareh['hora'].tolist()
    mareh_array = df_mareh['mare'].tolist()

    
    if float(mareh_array[0]) < float(mareh_array[1]):
        troca = seta1
        seta1 = seta2
        seta2 = troca
        
    mareh_array[0] =  hora_array[0][0:2]+":"+ hora_array[0][2:4] + " - " + mareh_array[0] + "m " + seta1
    mareh_array[1] =  hora_array[1][0:2]+":"+ hora_array[1][2:4] + " - " + mareh_array[1] + "m " + seta2
    mareh_array[2] =  hora_array[2][0:2]+":"+ hora_array[2][2:4] + " - " + mareh_array[2] + "m " + seta1
    if len(mareh_array)>3:
        mareh_array[3] =  hora_array[3][0:2]+":"+ hora_array[3][2:4] + " - " + mareh_array[3] + "m " + seta2


    for m in mareh_array:
        if m[0] ==  "":
            break
        
        descricao_mareh = descricao_mareh + m +"\n"
    
    descricao_mareh = descricao_mareh.replace("\n\n","\n")
    descricao_mareh = descricao_mareh.replace("\n","\\n")
    return descricao_mareh[0:-2]


def mareh_baixa(mareh_array): #RECEBE AS 4 MARÉS DO DIA E RETORNA AS 2 BAIXAS
    baixa = []
    if mareh_array[0][1] < mareh_array[1][1]:
        baixa.append(mareh_array[0])
        baixa.append(mareh_array[2])
    else:
        baixa.append(mareh_array[1])
        if mareh_array[3][0] != "":
            baixa.append(mareh_array[3])
    
    return baixa


       

########################################################
############ METODOS PARA ESCREVER NO ICS ##############
########################################################


def ics_header(arq_ics,zona,data_ini): #CRIA ARQUIVO INICIAL DO CALENDÁRIO
    cidade = arq_ics.split("-")[1].strip()
    calendario = arq_ics + ".ics"

    with open(ics_dest + calendario, "w") as ics:
        dia_fim  = data_ini[:-2] + str(int(data_ini[-2:])+1).zfill(2)
        

        ics.write("BEGIN:VCALENDAR")
        ics.write("\nPRODID:-//Google Inc//Google Calendar 70.9054//EN")
        ics.write("\nVERSION:2.0")
        ics.write("\nCALSCALE:GREGORIAN")
        ics.write("\nMETHOD:PUBLISH")
        ics.write("\nX-WR-CALNAME:Maré " + cidade.capitalize())
        ics.write("\nX-WR-TIMEZONE:"+zona)
        ics.write(tz(zona,utcdiff))
        ics.write("\nBEGIN:VEVENT")
        ics.write("\nDTSTART:"+data_ini)
        ics.write("\nDTEND:"+dia_fim)
        ics.write("\nRRULE:FREQ=DAILY")
        ics.write("\nUID:calmareh@rqf.fr")
        ics.write("\nDESCRIPTION:")
        ics.write("\nLOCATION:")
        ics.write("\nSTATUS:CONFIRMED")
        ics.write("\nSUMMARY:"+ "🌊 Maré -  " + cidade.capitalize() + " 🎣 🤿 🏄‍♂️")
        ics.write("\nEND:VEVENT")
        
        inicio = True
        ics.close()


def ics_mareh_dia(arq_ics, dia , descricao): # ESCREVE EVENTO DO DIA NO ICS
    delta = datetime.timedelta(days=1)

    dia_ics = str(dia).replace("-","")
    cidade = arq_ics.split("-")[1].strip()
    calendario = arq_ics + ".ics"
    nome_mareh = "🌊 Maré -  " + cidade.capitalize() + " 🎣 🤿 🏄‍♂️"
    dia_fim_ics = str(dia + datetime.timedelta(days=1)).replace("-","")

    with open(ics_dest + calendario, "a") as ics:        
        ics.write("\nBEGIN:VEVENT")
        ics.write("\nDTSTART:"+dia_ics)
        ics.write("\nDTEND:" + dia_fim_ics)
        ics.write("\nUID:calmareh@rqf.fr")
        ics.write("\nRECURRENCE-ID;VALUE=DATE:" + dia_ics)     
        ics.write("\nDESCRIPTION:" + descricao)
        ics.write("\nLOCATION:" + cidade.capitalize())
        ics.write("\nSTATUS:CONFIRMED")
        ics.write("\nSUMMARY:"+ nome_mareh)
        ics.write("\nEND:VEVENT")    
        ics.close()


def ics_end(arq_ics): # ESCREVE FINAL DO ICS
    calendario = arq_ics + ".ics"

    with open(ics_dest + calendario, "a") as ics:
        ics.write("\nEND:VCALENDAR")
        ics.close()



########################################################
############ TRANSFORMAÇÃo CSV PARA ICS ################
########################################################

def csv_to_cal(arquivo):
    prefixo = arquivo[:(arquivo.rfind("."))] #nome do arquivo sem extensão
    sufixo = ""
    zona = "America/Sao_Paulo"
    
    df = pd.read_csv(csv_source+arquivo)
    data_ini = "20220101"
    arq_ics = prefixo + sufixo
    
    ics_header(arq_ics, zona, data_ini) # COMEÇA A ESCRITA DO ICS

    start_date = datetime.date(2022, 1, 1)
    this_date = start_date
    end_date = datetime.date(2022, 12, 31)
    delta = datetime.timedelta(days=1)

    while this_date <= end_date: #ESCRITA DE CADA DIA NO ICS
        df_dia =  df[(df['data'] == str(this_date))]
        print(df_dia)
        descricao = descricao_sinalizada(df_dia)
        ics_mareh_dia(arq_ics,this_date, descricao)
        this_date += delta

    #TERMINA ESCRITA DO ICS
    ics_end(arq_ics)




csv_files = os.listdir(csv_source)
for file in csv_files:
    if file[-3:] == "csv":
        csv_to_cal(file)

