#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:45:41 2020

@author: dohertyguirand
"""


from bert import Ner
import PyPDF2 as p2

import sys
sys.stdout = open('log32.txt', 'w')

PDFfile = open("PDACW260.pdf", "rb")
pdfread = p2.PdfFileReader(PDFfile)
model = Ner("out_large/")

i = 0
fullText = ""
while i< pdfread.getNumPages():
    pageinfo = pdfread.getPage(i)
    fullText += str(pageinfo.extractText())
    i = i + 1

dic = {}
n = 500
chunks = [fullText[i:i+n] for i in range(0,len(fullText), n)]
seen = []
for c in chunks:
    output = model.predict(c)
    line = ""
    tag = ""
    for i in output:
        if i['confidence'] < .95 :
            print(i)
            if(i['tag'][0:1] == "B"):
                if line != "":
                    dic[line] = i['tag']
                line = ""

            line += " " + i['word']
            tag = i['tag']
            
for i in dic:
    print(i)
    print("\n")
         


