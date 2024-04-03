from urllib import parse
import os
import cv2
import numpy as np


"""img=cv2.imread("data\jacket\\0xe0e1ccull.jpg")
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist([img_gray], [0], None,[256],[0,256])
print(hist)"""

d={}

dir_path="jacket\\"

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.jpg' in file:
            img=cv2.imread("jacket\\"+file)
            img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([img_gray], [0], None,[1024],[0,1024])
            name=""
            for a in parse.unquote(file).split(".")[0:-1]:
                if name == "":
                    name=name+a
                else:
                    name=name+"."+a
            d[name]=list(hist)
    np.save('img_data.npy', d)