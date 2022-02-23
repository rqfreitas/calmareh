from PyPDF2 import PdfFileReader
import re
import pandas as pd
import urllib
import os


pdf_source = 'src/etl/marinha/pdf_marinha/'
csv_dest = 'src/etl/marinha/csv_marinha/'
txt_dest = 'src/etl/marinha/txt_marinha/'

pdf_path =  'src/etl/marinha/pdfmare.pdf'

# PEGA TEXTO DA PAGINA E LIMPA COM REGEX
def trata_pagina(texto):
    texto_novo = re.sub(r'(HORA ALT \(m\)( {0,7}))', '', texto)
    texto_novo = re.sub(r'01([A-Z]{3})', '\nmes\n', texto_novo) #Quebra mês - 01SAB
    texto_novo = re.sub(r'(|&|c|z|v)\d\d([A-Z]{3})', '\n', texto_novo) #Quebra DIA - 01SAB
    texto_novo = re.sub(r'(&)', '\n', texto_novo) #ultimo caractere
    texto_novo = re.sub(r'(\d\.\d)(?!\n)', r'\1,', texto_novo) #Quebra Marés - 01SAB
    texto_novo = re.sub(r'(  ){2,4}', '-', texto_novo)
    texto_novo = re.sub(r'( )', '', texto_novo)
    inicio = texto_novo.find("mes")
    fim = texto_novo.find("DG6")
    pagina_tatada = texto_novo[inicio:fim]
    return (pagina_tatada + "\n")

#PASSA POR CADA PAGINA DO PDF, LIMPANDO COM REGEX, E DEVOLVE UM TEXTO TRATADO
def trata_pdf(path):
    texto = ""
    
    pdf = PdfFileReader(str(path))
    for i in range(0,pdf.numPages):
        pagina  = pdf.getPage(i).extractText()
        texto = texto + trata_pagina(pagina)
    
    pdf_tratado = texto
    pdf_tratado = re.sub(r'\n\n', '\n', pdf_tratado)
    pdf_tratado = re.sub(r',(|.)\n', '\n', pdf_tratado)

    return pdf_tratado

#PASSA UM PDF PARA SER LIMPO POR REGEX, PASSA PRA TXT, DEPOIS LE CADA LINHA DO TXT E TRANSFORMA EM CSV
def transforma_pdf(path, ano):
    print(path)
    extensao = path[-3:]
    if extensao == "pdf":
        mes = 0
        dia = 0
        data = ""
        colunas=['data', 'hora', 'mare']
        df = pd.DataFrame([], columns=colunas)
        pdf_tratado = trata_pdf(path)
        tratado_path =  path.split('/')[-1]
        tratado_path = tratado_path[:-4] +".txt"
        mares_dia = []
        
        with open(txt_dest + tratado_path, 'w') as novo_arq:
            novo_arq.write(pdf_tratado)

        with open(txt_dest + tratado_path, 'r') as tratado_file:
            linhas  = tratado_file.readlines()
            for linha in linhas:
                if linha == "mes\n":
                    mes = mes + 1
                    dia = 0
                else:
                    if linha != "":
                        linha_div = linha.replace("\n","").split(",")
                        dia = dia + 1
                        data = str(ano) +"-"+str(mes).zfill(2)+"-"+str(dia).zfill(2)
                        print(data)
                        for b in linha_div:
                            binomio = b.split("-")
                            print(binomio)
                            hora = binomio[0]
                            mare = binomio[1]                   
                            if mes>0 and linha !="mes\n":
                                df_mare =  pd.DataFrame({'data':data, 'hora':hora , 'mare': mare},index=[0])
                                #mares_dia = []
                                df = df.append(df_mare)
                    
            df.to_csv(csv_dest+ tratado_path[:-4]+".csv", sep=',',index=False)


def transforma_pasta(path, ano):
    csv_files = os.listdir(path)
    for file in csv_files:
        transforma_pdf(pdf_source+file,ano)
        


transforma_pasta(pdf_source,2022)



#transforma_pdf(pdf_path)