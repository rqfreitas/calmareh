#resolver problema de + de 4 marés/dia
#rescrever csv
#transformar pra ics

import numpy as np
import os
from ast import literal_eval
from csv import reader

path = 'csv/'
csv_files = os.listdir(path)

def calendario_cidade(cidade):
    for f in csv_files:
        partes = f.split("_")
        cidade_file = partes[1][:-4]
        estado_file = partes[0]
        if cidade_file == cidade:
            csv_to_cal(f)

def calendario_estado(estado):
    for f in csv_files:
        partes = f.split("_")
        estado_file = partes[0]
        cidade_file = partes[1][:-4]
        if estado_file == estado:
            csv_to_cal(f)

# open file in read mode
def csv_to_cal(arquivo):
    partes = arquivo.split("_")
    cidade_file = partes[1][:-4]
    estado_file = partes[0]

    zona = "America/Recife"
    
    ics_header(cidade_file,estado_file, zona)
    inicio_ics = True
   # pass the file object to reader() to get the reader object   
    with open(('csv/'+ arquivo), 'r') as read_obj:
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        
        
        for row in csv_reader:
            ano = "2022"
            dia = row[1]
            mes = row[2]
            mares = row[3]
            
            dia_full = ano+mes+dia
            alarm  = False
            ics_mareh_dia(cidade_file,estado_file,zona, dia_full, mares, alarm,inicio_ics)
            inicio_ics = False

        
        ics_end(cidade_file,estado_file)

        

def csv_antigo_inpe():

    with open('csv/pernambuco_recife.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            dados = row[1].split(",")
            dia  = dados[0]
            mes = dados[1]
            dados = dados[2:]
            horas = []
            alturas = []
            for info in dados:
                if ":" not in info:
                    alturas.append(info)
                else:
                    horas.append(info)
            # row variable is a list that represents a row in csv
            

            tabua_dia = ""
            for dupla in range(len(horas)):
                tabua_dia = tabua_dia + horas[dupla] + " - " + alturas[dupla] + "\n"
            print(tabua_dia) #Descrição calendário


#METODOS PARA ESCREVER NO ICS


def ics_header(cidade_file,estado_file,zona):
    with open("ics/"+estado_file+"_"+cidade_file + ".ics", "w") as ics:
        ics.write("BEGIN:VCALENDAR")
        ics.write("\nVERSION:2.0")
        ics.write("\nCALSCALE:GREGORIAN")
        ics.write("\nMETHOD:PUBLISH")
        ics.write("\nX-WR-CALNAME:Maré " + cidade_file.capitalize())
        ics.write("\nX-WR-TIMEZONE:"+zona)
        ics.write("\nBEGIN:VEVENT")
        ics.write("\nDTSTART:"+"20220101")
        dia_fim  = "20220102"
        ics.write("\nDTEND:"+dia_fim)
        ics.write("\nRRULE:FREQ=DAILY")
        ics.write("\nUID:calmareh@rqf.fr")
        ics.write("\nDESCRIPTION:")
        ics.write("\nLOCATION:")
        ics.write("\nSTATUS:CONFIRMED")
        ics.write("\nSUMMARY:"+ "🌊 Maré -  " + cidade_file.capitalize() + " 🎣 🤿 🏄‍♂️")
        ics.write("\nEND:VEVENT")
        
        inicio = True
        ics.close()

def ics_mareh_dia(cidade_file,estado_file,zona, dia_full, mareh, alarm,inicio_ics):
    nome_mareh = "🌊 Maré -  " + cidade_file.capitalize() + " 🎣 🤿 🏄‍♂️"
        
    with open("ics/"+estado_file+"_"+cidade_file + ".ics", "a") as ics:
        descricao_mareh = ""
        mareh_array = literal_eval(mareh)
        seta1 = "🔺"
        seta2 = "🔹"
        troca = ""

        if mareh_array[0][1] < mareh_array[1][1]:
            troca = seta1
            seta1 = seta2
            seta2 = troca

        mareh_array[0][1] =  mareh_array[0][1] + "m " + seta1
        mareh_array[1][1] =  mareh_array[1][1] + "m " + seta2
        mareh_array[2][1] =  mareh_array[2][1] + "m " + seta1
        mareh_array[3][1] =  mareh_array[3][1] + "m " + seta2

        for m in mareh_array:
            if m[0] ==  ("m " + seta2):
                break
            
            descricao_mareh = descricao_mareh + m[0] + " - " + m[1]+"\\n"


        ics.write("\nBEGIN:VEVENT")
        
        ics.write("\nDTSTART:"+dia_full)
        dia_fim  = dia_full[:-2] + str(int(dia_full[-2:]) + 1)
        ics.write("\nDTEND:" + str(dia_fim).zfill(2))

        ics.write("\nUID:calmareh@rqf.fr")
        ics.write("\nRECURRENCE-ID;VALUE=DATE:"+dia_full)
        
        
        #ics.write("\nDTSTAMP;TZID="+zona+":"+"20220101"+"T"+"000001")
       
        #ics.write("\nCREATED;TZID="+zona+":"+"20220101"+"T"+"010100")
        ics.write("\nDESCRIPTION:" + descricao_mareh)
        #ics.write("\nLAST-MODIFIED;TZID="+zona+":"+modificacao+"T"+"010100")
        ics.write("\nLOCATION:" + cidade_file.capitalize())
        ics.write("\nSTATUS:CONFIRMED")
        ics.write("\nSUMMARY:"+ nome_mareh)
        ics.write("\nEND:VEVENT")
           
        ics.close()

def ics_end(cidade_file,estado_file):
    with open("ics/" + estado_file+"_"+cidade_file + ".ics", "a") as ics:
        ics.write("\nEND:VCALENDAR")
        ics.close()



calendario_cidade("recife")