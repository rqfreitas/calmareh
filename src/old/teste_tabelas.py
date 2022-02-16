from ast import Not
import csv 
import re
import sys
from matplotlib.pyplot import csd
import pandas as pd
import sys
import tabula

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
#from tabulate import tabulate


source = 'src/marinha/pdfmare.pdf'
binomios = []
linha = []
dias_bloco = []
blocos = []

bloco = 0
ehmare = False
nodia = 1
quatropordia = 1

#EXTRAI TABELA DO ARQUIVO PDF E TRANSFORMA EM CSV
def marinha_extract(arquivo):
    arquivo_final = arquivo[:-4] + "a.csv"
    tabula.convert_into(arquivo, arquivo_final, output_format="csv", pages='all')
    return arquivo_final

#LIMPA CSV SUJO E SALVA EM NOVO CSV
def limpa_csv(arquivo):
    with open(arquivo, 'r') as read_obj:
        texto_todo = read_obj.read()
        texto_novo = re.sub(r'( )(SAB|DOM|SEG|TER|QUA|QUI|SEX),', ' ', texto_todo)
        texto_novo = re.sub(r'(SAB|DOM|SEG|TER|QUA|QUI|SEX)', '', texto_novo)
        texto_novo = re.sub(r'HORA ALT \(m\) HORA ALT \(m\)', '', texto_novo)
        #10020.2,10300.1
        texto_novo = re.sub(r'(\d\d\d\d\d\.\d)(,)(\d\d\d\d\d\.\d)', r'\1 \3', texto_novo)
        texto_novo = re.sub(r'  ', ' ', texto_novo)
        texto_novo = re.sub(r'(\d\d,){7,9}\d\d\n', '', texto_novo)
        #texto_novo = re.sub(r'(\d\d\d\d\d\.\d),(\d\d),', r'\1,,', texto_novo)
        texto_novo = re.sub(r'( )\d\d(,)', r' ', texto_novo)#03512.1 17,04132.2
        texto_novo = re.sub(r'(,)\d\d(,)', r',,', texto_novo)
        texto_novo = re.sub(r'( )\d\d( )', r' ', texto_novo)
        texto_novo = re.sub(r'(\d\d\d\d\d\.\d) (\d\d) ', r'\1 ', texto_novo)
        texto_novo = re.sub(r'\n(..|),', '\n', texto_novo)
        texto_novo = re.sub(r',,', ';', texto_novo)
        texto_novo = re.sub(r'\n(.|,){2,23}\n', '\n', texto_novo)
        
        texto_novo = texto_novo[(texto_novo.find("\n")+1):]
        arquivo_final = arquivo[:-4] + "_limpo.csv"
        with open(arquivo_final, 'w') as novo_arq:
            novo_arq.write(texto_novo)


def transforma_csv(arquivo):
    #Sao 16 blocos. Dentro do bloco tem 2 datas repetidas 4 vezes, a data1 e a data+16
    #se o quatro por dia foi zerado, é por que é o inicio de um novo bloco.
    # pass the file object to reader() to get the reader object
    linha = 1
    with open(arquivo, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            flaglinhamare = False #comecou uma linha nova
            mareporlinha = 0 #comecou uma linha nova
            if quatropordia == 4:
                #comecou um novo dia
                dias_bloco.append(binomios)
                binomios = []
                bloco = bloco + 1
                

            for pedaco in row:
                parte = pedaco.split(" ")
                for p in parte:
                    ehmare = re.match("\d\d\d\d\d\.\d", p)
                    if ehmare:
                        mareporlinha = mareporlinha + 1
                        binomios.append(p)
                        if not flaglinhamare:
                            flaglinhamare = True
                            quatropordia = quatropordia + 1 #leu a quarta de algum dia da linha, é a ultima linha do bloco.

            


    mes = 1

    for b in binomios:
        print(b)

#csv_sujo = marinha_extract(source)
limpa_csv("src/marinha/pdfmarea.csv")



#TUTORIAL SITE PASSO A PASSO
def encontra_tabelas():
    i=0

    #read your file
    file=r'src/marinha/figuramare.png'
    img = cv2.imread(file,0)
    img.shape #thresholding the image to a binary image
    thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)#inverting the image 
    img_bin = 255-img_bin
    cv2.imwrite('figuramare2.png',img_bin)#Plotting the image to see the output
    plotting = plt.imshow(img_bin,cmap='gray')
    plt.show()


    # Length(width) of kernel as 100th of total width
    kernel_len = np.array(img).shape[1]//100# Defining a vertical kernel to detect all vertical lines of image 
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))# Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))# A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    #Use vertical kernel to detect and save the vertical lines in a jpg
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    cv2.imwrite("figuramare3.jpg",vertical_lines)#Plot the generated image
    plotting = plt.imshow(image_1,cmap='gray')
    plt.show()


    #Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
    cv2.imwrite("figuramare4.jpg",horizontal_lines)#Plot the generated image
    plotting = plt.imshow(image_2,cmap='gray')
    plt.show()

    # Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)#Eroding and thesholding the image
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("figuramare5.png", img_vh)
    bitxor = cv2.bitwise_xor(img,img_vh)
    bitnot = cv2.bitwise_not(bitxor)#Plotting the generated image
    plotting = plt.imshow(bitnot,cmap='gray')
    plt.show()

    # Detect contours for following box detection
    contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
        reverse = False
        i = 0    # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True    # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1    # construct the list of bounding boxes and sort them from top to
        # bottom
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
            key=lambda b:b[1][i], reverse=reverse))    # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    # Sort all the contours by top to bottom.
    contours, boundingBoxes = sort_contours (contours, method = "top-to-bottom" )

    #Creating a list of heights for all detected boxes
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]#Get mean of heights
    mean = np.mean(heights)

    #Create list box to store all boxes in  
    box = []# Get position (x,y), width and height for every contour and show the contour on image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)    
        if (w<1000 and h<500):
            image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            box.append([x,y,w,h])

    #Creating two lists to define row and column in which cell is located
    row=[]
    column=[]
    j=0    
    if(i==0):
        column.append(box[i])
        previous=box[i]    
    else:
        if(box[i][1]<=previous[1]+mean/2):
            column.append(box[i])
            previous=box[i]            
            if(i==len(box)-1):
                row.append(column)        
            else:
                row.append(column)
            column=[]
            previous = box[i]
            column.append(box[i])

    #calculating maximum number of cells
    countcol = 0
    for i in range(len(row)):
        countcol = len(row[i])
        if countcol > countcol:
            countcol = countcol

    #Retrieving the center of each column

    finalboxes = []
    #Regarding the distance to the columns center, the boxes are arranged in respective order
    for i in range(len(row)):
        lis=[]
        for k in range(countcol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])

        finalboxes.append(lis)

    outer = []
    #from every single image-based cell/box the strings are extracted via pytesseract and stored in a listouter=[]
    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner=''
            if(len(finalboxes[i][j])==0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                    finalimg = bitnot[x:x+h, y:y+w]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel,iterations=1)
                    erosion = cv2.erode(dilation, kernel,iterations=1)

                    
                    out = pytesseract.image_to_string(erosion)
                    if(len(out)==0):
                        out = pytesseract.image_to_string(erosion, config='--psm 3')
                    inner = inner +" "+ out

    #Creating a dataframe of the generated OCR list
    arr = np.array(outer)
    dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
    print(dataframe)
    data = dataframe.style.set_properties(align="left")#Converting it in a excel-file
    print(type(data))
    data.to_csv("figuramare.csv")

#METODO USANDO LIB TABULA
def encontra_tabelas2():
    table = tabula.read_pdf("src/marinha/pdfmare.pdf",pages=1)
    prima = table[0]
    print(prima)
    abc = "abc"