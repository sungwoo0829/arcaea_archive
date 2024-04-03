from urllib import parse
import cv2
import numpy as np



d = np.load('img_data.npy',allow_pickle='TRUE').item()


keys=list(d.keys())

f= open("test.txt",'w',encoding="utf-8")
size = len(keys)
for i in range(0,size):
    for j in range(i+1,size):
        
        hist1=np.array(d[keys[i]])
        hist2=np.array(d[keys[j]])
        
        f.write(str(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL))+"|"+str(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR))+keys[i]+"&"+keys[j]+"\n")
    

