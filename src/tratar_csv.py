#resolver problema de + de 4 marés/dia
#rescrever csv
#transformar pra ics
from csv import reader
# open file in read mode
with open('mare2021.csv', 'r') as read_obj:
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
        print(tabua_dia)