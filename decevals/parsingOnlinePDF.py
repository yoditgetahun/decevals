#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:30:04 2020

@author: dohertyguirand
"""

from bert import Ner
import urllib.request
import io
import PyPDF2 as p2

import sys
sys.stdout = open('log32.txt', 'w')

url = 'https://pdf.usaid.gov/pdf_docs/PA00WPD5.pdf'

open = urllib.request.urlopen(url).read()
memoryFile = io.BytesIO(open)
pdfread = p2.PdfFileReader(memoryFile)
#model = Ner("out_large/")

i = 0
fullText = ""
#while i< pdfread.getNumPages():
pageinfo = pdfread.getPage(pdfread.getNumPages()-1)
fullText += str(pageinfo.extractText())
   # i = i + 1
print(fullText)

    
dic = {}
n = 500
chunks = [fullText[i:i+n] for i in range(0,len(fullText), n)]


'''for c in chunks:
    output = model.predict(c)
    print(output)
    line = ""
    tag = ""
    for i in output:
        if "PER" in i['tag']:
            print(i)
            if(i['tag'][0:1] == "B"):
                if line != "":
                    dic[line] = i['tag']
                line = ""
                
            line += " " + i['word']
            tag = i['tag']
            
for i in dic:
    print(i)
    print("\n")'''