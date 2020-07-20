#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:14:30 2020

@author: yoditgetahun
"""
import pandas
import base64
import urllib.parse


#creates a URL that opens to a CSV file with the requested data
data = "datecreated:([20150101000000 TO 20201231000000]) (Documents.Bibtype_Name:(('Special Evaluation') OR ('Final Evaluation Report')))"

encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedB64 = str(encodedBytes, "utf-8")
encodedURL = urllib.parse.quote(encodedB64)

begin = "https://dec.usaid.gov/api/qsearch.ashx?q="
end = "&rtype=CSV"
finalURL = begin + encodedURL + end




#pulls the column in the spreadsheet with all of the pdf urls
col_list = ["Abstract", "Ancillary_Data", "Bibliographic_Type", 
            "ContentType", "Contract_Grant_Number", "Credit", "Date_Resource_Created",
            "Description", "Descriptors_Topical", "Descriptors_Geographic", "File", "File_Size",
            "Inst_Author", "Inst_Publisher", "Inst_Sponsor", "Language", "Mime_Type",
            "New_Thesaurus_Terms", "Notes", "Personal_Author", "Primary_Subject", 
            "Publication_Date_Freeform", "Related_Doc_Links", "Report_Number", "Series_Title",
            "Title", "Title_Translated", "Unique_ID", "URI", "USAID_Geography", "USAID_Project_Number" ]


cols = pandas.read_csv(finalURL, usecols=col_list)
pdfList= cols["File"]
urls = [pdfList[i] for i in range(0,len(pdfList))]




#creates new spread sheet with preferred columns
f = pandas.read_csv(finalURL)
keep_col = ["Abstract", "Ancillary_Data", "Bibliographic_Type", 
            "Contract_Grant_Number","Date_Resource_Created",
            "Descriptors_Topical", "Descriptors_Geographic", "File",
            "Inst_Author", "Inst_Publisher", "Inst_Sponsor",
           "Personal_Author", "Primary_Subject", 
            "Publication_Date_Freeform",
            "Title","Unique_ID",]

new_f = f[keep_col]
new_f.to_csv("newDECSearch.csv", index=False)



#print(urls)
