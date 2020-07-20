#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:11:41 2020

@author: dohertyguirand

"""
from pdf2image import convert_from_path, convert_from_bytes
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

images = convert_from_path('PA00WPHQ.pdf')

for i, image in enumerate(images):
        #read your file
    fname = 'image'+str(i)+'.png'
    image.save(fname, "PNG")
    file = fname
    img = cv2.imread(file,0)
    img.shape
    #thresholding the image to a binary image
    thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
    #inverting the image 
    img_bin = 255-img_bin
    cv2.imwrite('cv_inverted' + str(i)+ '.png',img_bin)
    #Plotting the image to see the output
    plotting = plt.imshow(img_bin,cmap='gray')
    # Length(width) of kernel as 100th of total width
    kernel_len = np.array(img).shape[1]//100
    # Defining a vertical kernel to detect all vertical lines of image 
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    # Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    # A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    #Use vertical kernel to detect and save the vertical lines in a jpg
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    cv2.imwrite('cv_virtical' + str(i)+ '.png',vertical_lines)
    #Plot the generated image
    plotting = plt.imshow(image_1,cmap='gray')

    
   
    '''im = cv2.imread(file)
    
    ret,thresh_value = cv2.threshold(im1,180,255,cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((5,5),np.uint8)
    dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)
    
    _,contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cordinates = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cordinates.append((x,y,w,h))
        #bounding the images
        if y< 50:
            
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
            
    plt.imshow(im)
    cv2.namedWindow('detecttable', cv2.WINDOW_NORMAL)
    cv2.imwrite('detecttable.jpg',im)'''