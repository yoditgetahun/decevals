#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:57:09 2020

@author: dohertyguirand
"""

from mining import ContactFinding as cf
import pandas as pd
import timeit

start = timeit.default_timer()
fin = open('PA00WPHQ-pdf-text.txt','r')
text = fin.read()
fin.close()
'''
text = cf.getTextFromPDF("https://pdf.usaid.gov/pdf_docs/PA00TCR5.pdf")
df,titleDictionary = cf.findtitlematches(text)
#text2 = cf.getTextFromPDF("https://pdf.usaid.gov/pdf_docs/PA00WPHQ.pdf")
stop1 = timeit.default_timer()
print('Titles Time: ', stop1 - start) 
#df2,titleDictionary2 = cf.findtitlematches(text2,titleDictionary)
start2 = timeit.default_timer()
#df = cf.findNameWithTitle(df)
df.to_csv('peopleandlines34.csv')
stop2 = timeit.default_timer()
print('Names Time: ', stop2 - start2)  
print('Total Time: ', stop2 - start)  
'''
df,titleDictionary = cf.findtitlematches(text);
#df = cf.findNameWithTitle(df)
df.to_csv('PA00WPHQ-pdf-titles.csv')

