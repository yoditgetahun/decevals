#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 11:54:08 2020

@author: dohertyguirand
"""


from bert import Ner
import urllib.request
import io
import PyPDF2 as p2

import sys
sys.stdout = open('ex13', 'w')

url = 'https://pdf.usaid.gov/pdf_docs/PA00WPD5.pdf'

open = urllib.request.urlopen(url).read()
memoryFile = io.BytesIO(open)
pdfread = p2.PdfFileReader(memoryFile)
docInfo = pdfread.getNamedDestinations()
print(docInfo)
#model = Ner("out_large/")

i = 0
fullText = ""
textArr = []
#while i< pdfread.getNumPages():
pageinfo = pdfread.getPage(2)
newText = str(pageinfo.extractText())
fullText +=newText


'''textArr.append(newText)
    i = i + 1'''

    
foundTitles = []
relevantTitles = [" COP", " DCdocOP", " AOR", " COR", " AOR/COR", " Chief of Party", " CHIEF OF PARTY", " Deputy Chief of Party", " DEPUTY CHIEF OF PARTY", " Evaluation Specialist", " Evaluation Team Leader", " National Expert", " Research Consultant", " Field Researcher"]
'''for i in textArr:
    pageArr = i.split("\n")
    for k in pageArr:
        for t in relevantTitles:
            if t in k:
                foundTitles.append(k)
print(foundTitles)'''
'''dic = {}
n = 500
chunks = [fullText[i:i+n] for i in range(0,len(fullText), n)]


for c in chunks:
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