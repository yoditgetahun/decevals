#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:46:08 2020

@author: dohertyguirand
"""


import tabula
from mining import ContactFinding as cf
import pandas as pd

text = tabula.read_pdf('PA00WPHQ.pdf', pages = 'all')
#text = cf.splitlines(str(text))
text = cf.remove(str(text))
text = cf.splitlines(str(text))

ner = cf.runNER(str(text))
ppl = cf.findTag(ner, 'PER')

NERppl = pd.DataFrame({
    'NER People': ppl,
    }) 
NERppl.to_csv('NERppl.csv') 

file = open('tables.txt', 'w')
file.write(str(text))
file.close()