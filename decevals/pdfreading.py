#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 17:43:19 2020

@author: dohertyguirand
"""

import PyPDF2 as p2
from bs4 import BeautifulSoup
import requests
import re
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

PDFfile = open("PA00WPHQ.pdf", "rb")
pdfread = p2.PdfFileReader(PDFfile)
outputfile = open("spacyoutput.txt", 'a')

i = 0

names = []

while i < pdfread.getNumPages():
    pageinfo = pdfread.getPage(i)
    newText = str(pageinfo.extractText())
    article = nlp(newText)
    labels = [(X.text, X.label_) for X in article.ents]
    outputfile.write(str(labels))
    i = i + 1
                           