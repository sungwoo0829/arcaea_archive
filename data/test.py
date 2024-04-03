from urllib import parse
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image,ImageFilter,ImageDraw,ImageOps
import easyocr
import io

#img=Image.open("image.png")

#img=ImageOps.invert(img.convert('L'))


#img.save('im_test.png')

#result=pytesseract.image_to_string(img,config='digits')
#print(result)

reader = easyocr.Reader(['en'],gpu=True)
results = reader.readtext('test1.png', detail=0)
for re in results:
    print(re)