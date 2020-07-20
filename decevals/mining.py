#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 14:17:06 2020

@author: dohertyguirand
"""



from bert import Ner
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
import urllib.request
import re
from collections import Counter
import pandas as pd
import math
import sys
import timeit



class ContactFinding():
   
    
    def getTextFromPDF(url):
        open = urllib.request.urlopen(url).read()
        memoryFile = io.BytesIO(open)
        
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
        
        with memoryFile as fh:
        
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)
        
            text = fake_file_handle.getvalue()
        
        # close open handles
        converter.close()
        fake_file_handle.close()
        return text
        
    def splitlines(text):
        lines = []
        for line in text.splitlines():
            if (not line.isspace()) and( not line == ""):
                lines.append(line)
        return lines
    
    def findtitlematches(text, titleDictionary = {}):
        fin = open('job-titles.txt','r')
        data = fin.read()
        fin.close()
        titles = data.splitlines()
        lines = ContactFinding.splitlines(text)
        #chunks = ContactFinding.splitIntoChunks(text)
        lineDictionary = {}
        for title in titles:
            for i in range(0, len(lines)):
                if title in lines[i]:
                    threeLines = lines[i]
                    if i > 0 and i < (len(lines) - 2):
                        threeLines = lines[i-1] +" "+ lines[i] +" " +lines[i+1]
                    if i == 0 and len(lines) > 2 :
                        threeLines = lines[i] +" "+lines[i+1]
                    if i == (len(lines) - 1) and len(lines) > 2:
                        threeLines = lines[i-1] + " " + lines[i]
                    if len(lines) == 2:
                        threeLines = lines[0] + " " + lines[1]
                        
                    if title in titleDictionary.keys():
                        titleDictionary[title].append(threeLines)
                        lineDictionary[title].append(lines[i])
                    else:
                        titleDictionary[title] = [threeLines]
                        lineDictionary[title] = [lines[i]]
        df = pd.DataFrame(list(titleDictionary.items()), columns = ['Title', 'Lines'])
        print("Done with title matches")
        return df,titleDictionary
    
    def findTitles(text):
            titles = re.compile(r'\bMission(\s[A-Z][a-z]*)+|\bAOR\b|\bAdministrative(\s[A-Z][a-z]*)*|\bCOR\b|\bCO\b|([A-Z][a-z]*\s?)+Officer|([A-Z][a-z]*\s?)+Representative|([A-Z][a-z]*\s?)*Chief\sof\sParty|([A-Z][a-z]*\s?)+Lead|([A-Z][a-z]*\s?)+Specialist|([A-Z][a-z]*\s?)*Expert|([A-Z][a-z]*\s?)+Advisor|([A-Z][a-z]*\s?)+Manager|([A-Z][a-z]*\s?)+Assistant')
            titleList = []
            if re.search(titles,text):
                for titleFound in re.finditer(titles, text):
                    titleFound = titleFound.group()
                    titleList.append(titleFound)
            return titleList
    
    def findNameWithTitle(df):
        titleNameList = []
        nerOutputList = []
        names = []
        curr = 0
        total = len(df.index)
        for row in df.itertuples():
            title = row.Title
            lines = row.Lines
            #print(lines)
            nerList = []
            nameList = []
            for i in range(0, len(lines)):
                nerOutput = ContactFinding.runNER(lines[i])
                nerList.append(nerOutput)
                nameDict = ContactFinding.findTag(nerOutput, "PER")
                nameProxNumList = []
                nameList.append(nameDict)
                
                for name in nameDict.keys():
                    proximity = ContactFinding.findProximity(name, title, lines[i])
                    nameProxNumList.append({ 'Name':name ,'Proximity':proximity,'Count':nameDict[name]})
            names.append(nameList)
            nerOutputList.append(nerList)
            titleNameList.append(ContactFinding.sortByProximity(nameProxNumList))
            print(str(curr) + "/" + str(total))
            curr += 1
        df['NameProximityCount'] = titleNameList
        df['NERoutput'] = nerOutputList
        df['Names'] = names
        return df
    
    def removeIgnoredOrgs(orgs):
        returnOrgs = []
        orgsToIgnore = []
        for org in orgs:
            if org not in orgsToIgnore:
                returnOrgs.append(org)
        return returnOrgs
        
    '''def findPeopleAndOrgs(text):
        output = ContactFinding.runNER(text)
        people = []
        orgs = []
        line = ""
        
        for i in output:
            if "PER" in i['tag']:
                 if(i['tag'][0:1] == "B") and (line != "") :
                     people.append(line)
                     line = ""
                 line += " " + i['word']

            if "ORG" in i['tag']:
                if(i['tag'][0:1] == "B") and (line != "") :
                     orgs.append(line)
                     line = ""
                line += " " + i['word']
                
        people = list(dict.fromkeys(people))
        orgs = list(dict.fromkeys(orgs))
        return people, orgs'''
    
    def findTag(nerOutput, tag):
        line = ""
        foundWithTag = []
        for i in nerOutput:
            if(i['tag'][0:1] != "I") and (line != ""):
                foundWithTag.append(line.lstrip())
                line = ""
            if tag in i['tag']:
                line += " " + i['word']
        if(line != ""): foundWithTag.append(line.lstrip())
        if len(foundWithTag) == 0: return {}
        return Counter(foundWithTag)


    #does not do anything yet

    def sortByProximity(list):
        sortedList = sorted(list, key = lambda i : (i['Proximity'], i['Count']))
        return sortedList
            
        
    #todo fix so that it can actually split into sentances 
    def splitIntoChunks(text):
        textSplit = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s",text)
        chunks = []
        chunk = ""
        finalchunks = []
        
        for sent in textSplit:
            if (len(chunk) +1+ len(sent)) < 500:
                chunk += " " + sent
            else:
                chunks.append(chunk)
                chunk = sent
        chunks.append(chunk)
        for i in chunks:
            if len(i) < 500:
                finalchunks.append(i)
            else:
                split = [i[l:l+500] for l in range(0,len(text), 500)]
                for sp in split:
                    finalchunks.append(sp)
        finalchunks = ContactFinding.removeEmptyIndcies(finalchunks)
        return finalchunks
    
    def splitSent(text):
        textSplit = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s",text)
        return textSplit
    
    def merge(dict1, dict2): 
        res = {**dict1, **dict2} 
        return res
    
    def findProximity(name, title, line):
        namePattern = re.compile(name)
        titlePattern = re.compile(title)
        nameStartingIndecies = [m.start() for m in re.finditer(namePattern, line)]
        titleStartingIndecies = [m.start() for m in re.finditer(titlePattern, line)]
        nameEndingIndecies = [m.end() for m in re.finditer(namePattern, line)]
        titleEndingIndecies = [m.end() for m in re.finditer(titlePattern, line)]
        result = sys.maxsize
        if len(nameStartingIndecies) >= 1 and len(nameEndingIndecies) >=1 and len(titleStartingIndecies) >=1 and len(titleEndingIndecies) >=1:
            titleIndex = 0
            nameIndex = 0
            
            if nameStartingIndecies[0] < titleStartingIndecies[0]:
                nameIndex = nameEndingIndecies[0]
                titleIndex = titleStartingIndecies[0]
            elif nameStartingIndecies[0] > titleStartingIndecies[0]:
                nameIndex = nameStartingIndecies[0]
                titleIndex = titleEndingIndecies[0]
            result = abs(nameIndex - titleIndex)
        return result
    
    def removeEmptyIndcies(list):
        cleanList = []
        for i in list:
            if i != '':
                cleanList.append(i)
        return cleanList
                
    
    def runNER(text):
        model = Ner("out_large/")
        chunks = ContactFinding.splitIntoChunks(text)
        output = model.predict(chunks[0])
        for i in range(1, len(chunks)):
            output = output + (model.predict(chunks[i]))
        return output
    
if __name__ == '__main__':
    start = timeit.default_timer()
    fin = open('output.txt','r')
    text = fin.read() + "\n"
    fin.close()
    text += ContactFinding.getTextFromPDF("https://pdf.usaid.gov/pdf_docs/PA00WPHQ.pdf")
    df,titleDictionary = ContactFinding.findtitlematches(text)
    #text2 = cf.getTextFromPDF("https://pdf.usaid.gov/pdf_docs/PA00WPHQ.pdf")
    stop1 = timeit.default_timer()
    print('Titles Time: ', stop1 - start) 
    #df2,titleDictionary2 = cf.findtitlematches(text2,titleDictionary)
    start2 = timeit.default_timer()
    df = ContactFinding.findNameWithTitle(df)
    df.to_csv('peopleandlines28.csv')
    stop2 = timeit.default_timer()
    print('Names Time: ', stop2 - start2)  
    print('Total Time: ', stop2 - start)  
   
            
        
        
            