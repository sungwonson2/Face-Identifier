import zipfile

import PIL
from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')

images = []

find = "Christopher"

file = "readonly/small_img.zip"
zf = zipfile.ZipFile(file, 'r')
for entry in zf.infolist():
    with zf.open(entry) as file:
        img = Image.open(file)
        img.save('normal.jpg')
        img = img.convert('L')
        img.save('greyscale_noise.jpg')
        text = pytesseract.image_to_string(Image.open('greyscale_noise.jpg')) 
        
        cv_img=cv.imread('greyscale_noise.jpg', cv.IMREAD_GRAYSCALE)

        faces = face_cascade.detectMultiScale(cv_img, 2.00)
    
        pil_img=Image.open('greyscale_noise.jpg')
        normal_img=Image.open("normal.jpg")

        drawing=ImageDraw.Draw(pil_img)

        rec=faces.tolist()[0]

        for x,y,w,h in faces:
            drawing.rectangle((x,y,x+w,y+h), outline="white")
        drawing.rectangle((rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]), outline="white")
        
        contact_sheet=PIL.Image.new(normal_img.mode, (500,100*(int(len(faces)/5) + 1)))
        x=0
        y=0

        draw = ImageDraw.Draw(contact_sheet)  
        for a,b,c,d in faces:

                if c > 100 or d > 100:
                    contact_sheet.paste(normal_img.crop((a,b,a+c,b+d)).resize((100,100)), (x, y)) 
                else:
                    contact_sheet.paste(normal_img.crop((a,b,a+c,b+d)), (x, y)) 
                if x+100 == contact_sheet.width:
                    x=0
                    y=y+100
                else:
                    x=x+100
                         
        if find in text:
            print("Results found in file " + entry.filename)
            if len(faces) > 0:
                display(contact_sheet)
            else:
                print("But there were no faces in that file!")            

print("done")    

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

