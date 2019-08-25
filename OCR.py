import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import urllib
import cv2
import json

Images = []
Numberplates = []

def Extractor(df):
    for index, Row in df.iterrows():
        Response = urllib.request.urlopen(Row[0])
        Img = np.array(Image.open(Response)) #image from URL
        Images.append(Img) # Storing images permanently
        xh = Row[1][0]['x'] * Img.shape[1]
        yh = Row[1][0]['y'] * Img.shape[0]
        xb = Row[1][1]['x'] * Img.shape[1]
        yb = Row[1][1]['y'] * Img.shape[0]
        n_Image = Image.fromarray(Img)

        noplateImage = n_Image.crop((xh, yh, xb, yb)) #Cropping number-plate from Image
        Numberplates.append(np.array(noplateImage)) # Stored cropped image
        noplateImage.save('image.png')
        img = cv2.imread('image.png')
        img = cv2.resize(img, (int(img.shape[1] * 4), int(img.shape[0] * 4))) #increased size of image
        data = pytesseract.image_to_string(Img) # using pytesseract to extract characters
        print(data)

if __name__ == "__main__":
    df = pd.read_json('Indian_Number_plates.json', lines=True) #Reading the JSON file (removing problem of trailling data)
    #print(df)
    df['cords'] = df.apply(lambda row: row['annotation'][0]['points'], axis=1)
    del df['extras']
    del df['annotation']
    Extractor(df)
