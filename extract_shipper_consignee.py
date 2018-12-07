#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import PythonMagick
import pytesseract

# converrt PDF to PNG
folder = "outputPNG"
def get_page_image_from_pdf(file_path, main_path):  
    print("IN method get_page_image_from_pdf")
    name = folder + "/" + file_path[:-4] + ".png"
    img = PythonMagick.Image()
    img.density("300")
    img.read(main_path + file_path.encode('utf-8'))
    img.write(name.encode('utf-8'))          

# function to perform OCR
def tesseractOCR(inputImage, outputTxt, psmMode, filename):  ## CV methods
    print("IN method tesseractOCR")
    # print(os.getcwd())
    img = cv2.imread(inputImage)
    # img = img[0:20,:]
    result = pytesseract.image_to_string(img, lang="eng")
    result = os.linesep.join([s for s in result.splitlines() if s])  # remove blank lines
    result = '\n'.join(result.split('\n')[1:])   # removing the first line from detected text because it will all be either "Sheepers name & address" or "consigees name & address"

    pre_string = result.split('\n')[0]
    post_string = result.split('\n')[1:]

    if((validateString(pre_string))):
        pre_string = ""

    result = ''.join(pre_string) + '\n' + '\n'.join(post_string)
    result = result.encode('utf-8') + '\n\n\n'
    path = outputTxt + ".txt"

    if not os.path.exists(path):
        f = open(path ,"w+")
    else:
        f = open(path ,"a")

    f.write(result)
    f.close()

# check for valid string while performing OCR
def validateString(s):
    letter_flag = False
    number_flag = False
    for i in s:
        if i.isalpha():
            letter_flag = True
        if i.isdigit():
            number_flag = True
    
    return ((letter_flag and number_flag) or (len(s.split()) == 1) or (s.isdigit())) 

def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    print("IN method box_extraction")
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image

    h, w = img.shape[:2]
    img = img[0:h-2500, 0:w/2]   #shp
    # cv2.imwrite(img_for_box_extraction_path ,img)

    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    # cv2.imwrite("Image_bin.jpg",img_bin)
   
    kernel_length = np.array(img).shape[1]//40     
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite("verticle_lines.jpg",verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    # cv2.imwrite(img_for_box_extraction_path[9:-4] + "img_final_bin.jpg",img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (contours, boundingBoxes) = sort_contours(contours, method="left-to-right")

    idx = 0
    i = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        if (w > 200 and h > 240 and w < 1800 and h < 720):
            idx += 1
            new_img = img[y:y+h, x:x+w]
            cv2.imwrite(cropped_dir_path + "/" + img_for_box_extraction_path[12:-4] + "_" +str(idx) + '.png', new_img)
            i += 1
            
    # For debugging
    # enable this line to see all contours.
    # for (i, c) in enumerate(contours):
    #   draw_contour(img, c, i)

# for debugging
def draw_contour(image, c, i):
    # compute the center of the contour area and draw a circle
    # representing the center
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
 
    # draw the countour number on the image
    cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
        1.0, (0, 0, 0), 2)

    cv2.imwrite("./Temp/"+str(i)+".jpg", image)


# convert to png, box & image extraction
main_path = "/home/charmi/Desktop/Shipmnts Hiring Challenge/box detector/input/"
for file in os.listdir(main_path):
    if file.endswith(".pdf"):
        # print(file)
        get_page_image_from_pdf(file, main_path)
        box_extraction("./outputPNG/" + file[:-4] + ".png", "./Cropped")

# text extraction
cropped_path = "/home/charmi/Desktop/Shipmnts Hiring Challenge/box detector/Cropped/"
for file in os.listdir(cropped_path):
    if file.endswith(".png"):        
        tesseractOCR("Cropped/" + file, "Cropped/" + file[:-6] , 3, file)