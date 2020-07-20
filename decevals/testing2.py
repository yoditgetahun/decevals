#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 09:28:04 2020

@author: dohertyguirand
"""
 # importing modules
import cv2
import pytesseract
image = cv2.imread("image20.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(threshold_img)
print(details.keys())
total_boxes = len(details['text'])
for sequence_number in range(total_boxes):
	if int(details['conf'][sequence_number]) >30:
		(x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
		threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
parse_text = []
word_list = []
last_word = ''
for word in details['text']:
    if word!='':
        word_list.append(word)
        last_word = word
    if (last_word!='' and word == '') or (word==details['text'][-1]):
        parse_text.append(word_list)
        word_list = []
import csv
with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)
    
pytesseract.image_