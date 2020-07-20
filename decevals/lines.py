#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:58:30 2020

@author: dohertyguirand
"""

from mining import ContactFinding as cf
import pandas
import timeit

start = timeit.default_timer()
cols = pandas.read_csv("./newDECSearch.csv",error_bad_lines=False)
pdfList= cols["File"]
urls = [pdfList[i] for i in range(0,len(pdfList))]
file = open('newTitles.txt','a+')
alltitles = []
curr = 0
tot = len(pdfList)
for i in range(30,60):
    lap = timeit.default_timer()
    print('Lap Time: ', lap - start)  
    print(str(curr) +"/"+ str(tot))
    titles = cf.findTitles(cf.getTextFromPDF(pdfList[i]))
    alltitles = alltitles + titles
    curr += 1
alltitles = list(dict.fromkeys(alltitles))
for item in alltitles:
        file.write("%s\n" % item)
file.close()
stop = timeit.default_timer()
print('Names Time: ', stop - start)  

''' url = 'https://pdf.usaid.gov/pdf_docs/PA00WPHQ.pdf'
    bucketname = 'decevaluations'
    objectname = 'test'
    open = urllib.request.urlopen(url).read()
    memoryFile = io.BytesIO(open)
    
    s3 = boto3.client('s3')
    s3.upload_fileobj(memoryFile, bucketname, objectname)'''