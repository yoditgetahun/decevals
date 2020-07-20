#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 10:40:51 2020

@author: dohertyguirand
"""


from mining import ContactFinding
import sys
sys.stdout = open('dataFrame.txt', 'w')



text = "This evaluation could not have been possible without the contributions of the dedicated U.S. Agency for International Development (USAID) and implementing partner staff whose inputs were instrumental to the evaluation team’s efforts. The team expresses its deepest gratitude to Agreement Officer’s Representative Ramesh Adhikari and Program Development Specialist (M&E) Bishwas Rana of the Democracy and Governance Office for their exceptional support and guidance throughout the evaluation."

'''text = "James Fremming, Evaluation Team Leader\n Indu Tuladhar, National Expert (GESI Specialist)\n\
Ajaya Bhadra Khanal, National Expert (Politics and Governance Specialist)\n\
Anamika Pradhan, Research Consultant\n\
Puja Bharati, Research Consultant\n\
Padam Bdr Bk (Sushil), Field Researcher\n\
Sumana Devkota, Field Researcher\n\
Srijana Giri, Field Researcher\n\
Laxmi Thapa, Field Researcher\n\
Nilam Bhandari, Field Researcher\n\
USAID/Nepal’s Monitoring, Evaluation, and Learning (MEL) Support\n\
Kshitiz Shrestha, Evaluation Specialist (Senior Level)\n\
Marc Shapiro, Chief of Party\n\
Manorama Adhikari, Deputy Chief of Party\n"'''


titles = ContactFinding.findTitles(text)
dictionary = ContactFinding.findNameWithTitle(titles)
del dictionary['Lines']
print(dictionary)

