#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:24:35 2020

@author: dohertyguirand
"""

fin = open('job-titles.txt','r')
data = fin.read()
lines = data.splitlines()
lines.sort(key = lambda s: len(s))
repeatdictionary = {}
seen= []
for i in range(0,len(lines)):
    if lines[i] not in seen:
        repeatdictionary[lines[i]] = []
        for l in lines:
            if lines[i] in l:
                seen.append(l)
                diff = l.replace(lines[i], '')
                repeatdictionary[lines[i]].append(diff)
            
newdict = {}
patterns = []
for i in repeatdictionary.keys():
    values = repeatdictionary[i]
    if len(values) == 1:
        patterns.append('\b'+i+'\b|')
    elif len(values) > 1:
        beginningpattern = '(\s?('
        for v in range(1,len(values)):
            beginningpattern += values[v]
            if v != (len(values) -1):
                beginningpattern += '|'
        beginningpattern+= ')\s?)*'
        pattern = beginningpattern + i + beginningpattern
        patterns.append(pattern)

finalpattern = ""

for i in range(0,len(patterns)):
    finalpattern += patterns[i]
    if i != (len(patterns) -1):
        finalpattern += '|'

'''pattern = ""
for line in lines:
    pattern += "\b"+line+"\b|"'''
    
fout = open('titlepattern.txt','w')
fout.write(finalpattern)
fout.close()
fin.close()
