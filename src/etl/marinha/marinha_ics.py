
import numpy as np
import os
from ast import literal_eval
from csv import reader

csv_source = 'src/etl/marinha/csv_marinha/'
arquivo = 'Pernambuco - PORTO DE SUAPE - 2022.csv'

def csv_to_cal(arquivo,estilo):
    prefixo = arquivo[:(arquivo.rfind("."))] #nome do arquivo sem extensão
    sufixo = ""
    zona = "America/Sao_Paulo"
    if estilo != "mare_dia":
        sufixo = "_h"
        

    arq_ics = prefixo + sufixo
    #cidade_file,estado_file,zona,data_ini
    ics_header(arq_ics, zona, data_ini)
    #ics_header(cidade_file,estado_file, zona, data_ini)

   # pass the file object to reader() to get the reader object   
    with open(('csv/'+ arquivo), 'r') as read_obj:
        csv_reader = reader(read_obj)
        alarm  = False

        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            ano = data_ini[:4]
            dia = row[1]
            mes = row[2]
            mares = row[3]
            
            dia_full = ano+mes+dia
            if estilo == "mareh_dia":
                ics_mareh_dia(arq_ics,zona, dia_full, mares)
            else:
                ics_mareh_horas(arq_ics,zona, dia_full, mares)
        
        ics_end(arq_ics)
       

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

#MONTA DESSCRIÇÃO COM ICONES DE MARÉ BAIXA
def descricao_sinalizada(mareh_array):
    seta1 = "🔺"
    seta2 = "🔹"
    troca = ""
    indice_gravacao = 1
    descricao_mareh = ""
    
    if mareh_array[0][1] < mareh_array[1][1]:
        troca = seta1
        seta1 = seta2
        seta2 = troca
        indice_gravacao = 0
        
    

    mareh_array[0][1] =  mareh_array[0][1] + "m " + seta1
    mareh_array[1][1] =  mareh_array[1][1] + "m " + seta2
    mareh_array[2][1] =  mareh_array[2][1] + "m " + seta1
    mareh_array[3][1] =  mareh_array[3][1] + "m " + seta2


    for m in mareh_array:
        if m[0] ==  "":
            break
        
        descricao_mareh = descricao_mareh + m[0] + " - " + m[1]+"\n"
    
    descricao_mareh = descricao_mareh.replace("\n\n","\n")
    return descricao_mareh

#RECEBE AS 4 MARÉS DO DIA E RETORNA AS 2 BAIXAS
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

def tz(zona, utcdiff):
    tz_string = "\nBEGIN:VTIMEZONE\nTZID:"+ zona+ "\nX-LIC-LOCATION:"+ zona+ "America/Sao_Paulo\nBEGIN:STANDARD\nTZOFFSETFROM:-"+ str(utcdiff).zfill(2) +"00\nTZOFFSETTO:-"+ str(utcdiff).zfill(2) +"00\nTZNAME:-"+ str(utcdiff).zfill(2) +"\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE"
    return tz_string

#CRIA ARQUIVO INICIAL DO CALENDÁRIO
def ics_header(arq_ics,zona,data_ini):
    cidade = arq_ics.split("_")[1]
    calendario = arq_ics + ".ics"

    with open("ics/" + calendario, "w") as ics:
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

def ics_end(arq_ics):
    calendario = arq_ics + ".ics"

    with open("ics/" + calendario, "a") as ics:
        ics.write("\nEND:VCALENDAR")
        ics.close()

def ics_mareh_dia(arq_ics,zona, dia_full, mareh):
    cidade = arq_ics.split("_")[1]
    calendario = arq_ics + ".ics"
    nome_mareh = "🌊 Maré -  " + cidade.capitalize() + " 🎣 🤿 🏄‍♂️"

    with open("ics/" + calendario, "a") as ics:
        mareh_array = literal_eval(mareh)
        descricao_mareh = descricao_sinalizada(mareh_array)
        dia_fim  = dia_full[:-2] + str(int(dia_full[-2:]) + 1).zfill(2)
        
        ics.write("\nBEGIN:VEVENT")
        ics.write("\nDTSTART:"+dia_full)
        ics.write("\nDTEND:" + str(dia_fim).zfill(2))
        ics.write("\nUID:calmareh@rqf.fr")
        ics.write("\nRECURRENCE-ID;VALUE=DATE:" + dia_full)     
        ics.write("\nDESCRIPTION:" + descricao_mareh)
        ics.write("\nLOCATION:" + cidade.capitalize())
        ics.write("\nSTATUS:CONFIRMED")
        ics.write("\nSUMMARY:"+ nome_mareh)
        ics.write("\nEND:VEVENT")    
        ics.close()

def ics_mareh_horas(arq_ics,zona, dia_full, mareh):
    cidade = arq_ics.split("_")[1]
    calendario = arq_ics + ".ics"
    nome_mareh = "🌊 Maré Baixa -  " + cidade.capitalize() + " 🎣 🤿 🏄‍♂️ "

    with open("ics/" + calendario, "a") as ics:
        
        mareh_array = literal_eval(mareh)
        descricao_mareh = descricao_sinalizada(mareh_array)
        baixas = mareh_baixa(mareh_array)
        


        for mareh in baixas:
            tempo = mareh[0].split(":")
            #hora  = str((int(tempo[0]) + utcdiff)%24).zfill(2)
            hora  = tempo[0].zfill(2)
            minuto = tempo[1].zfill(2)

            #hora_fim = hora[:-2] + str(int(hora[-2:]) + 15 ).zfill(2)
            minuto_fim = str(int(minuto) + 10).zfill(2)
            if int(minuto) >49:
                minuto_fim = "59"

            ics.write("\nBEGIN:VEVENT")
            ics.write("\nDTSTART;TZID="+zona+":"+ dia_full + "T"+ hora + minuto  + "00")        
            ics.write("\nDTEND;TZID="+zona+":" + dia_full+ "T"+ hora + minuto_fim +  "00")           
            ics.write("\nUID:calmareh@rqf.fr")
            ics.write("\nRECURRENCE-ID;VALUE=DATE:" + dia_full)
            ics.write("\nDESCRIPTION:" + descricao_mareh)
            ics.write("LOCATION:" + cidade.capitalize())
            ics.write("\nSTATUS:CONFIRMED")
            ics.write("\nSUMMARY:"+ nome_mareh + mareh[1])
            ics.write("\nEND:VEVENT")
        
        ics.close()




#O ESTILO PODE SER "mareh_dia" OU "mareh_hora"
calendario_cidade("recife","mareh_hora")
