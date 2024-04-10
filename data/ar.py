import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
from openpyxl import Workbook
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


wb = Workbook()
wr= wb.active
wr.append(["song","artist","pack","difficulty","note","bp","version","img"])

headers = {"User-Agent":"Mozilla/5.2 (Windows NT 10.0; Win64; x64) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

url = "https://wikiwiki.jp/arcaea/%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB%E9%A0%86"
res = requests.get(url,headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

basetable = soup.find_all('table')

for k in range(len(basetable)):
    if k==0:
        tds=[]
    else:
        tds=basetable[k].find_all('a',attrs={"class":"rel-wiki-page"})

    for td in tds:
        print(td)
        past=[]
        present=[]
        future=[]
        beyond=[]
        beyond2=[]

        link = td.get('href')
        res1 = requests.get("https://wikiwiki.jp"+str(link),headers=headers)
        res1.raise_for_status()
        soup1 = BeautifulSoup(res1.text, "lxml")

        tables1 = soup1.find_all("table")
        tables=[]

        for tb1 in tables1:
            if ".png" in str(tb1.find_all("img")):
                pass
            elif len(tb1.find_all("img"))>0:
                if "fold-container" in str(tb1.find_parent().find_parent()):
                    pass
                elif "ゲーム内に記載なし" in str(tb1):
                    pass
                elif len(tb1.find_all("tr"))>1:
                    tables.append(tb1)



        p = re.compile("譜面定数 : \d+[.]\d+")
        rbp=p.findall(str(soup1))

        rbpp=[]
        for x in rbp:

            rbpp.append(re.compile("\d+[.]\d+").findall(x)[0])
        
        mt=tables[0]

        trs=mt.find_all("tr")

        for tr in trs:
            tp=tr.find_all("th")[0].string
            if tp == "Composer":
                artist=tr.find_all("td")[0].text
            

        notes=trs[4].find_all("td")



        a=mt.find_all("a",attrs={"class":"rel-wiki-page"})

        artist=a[0].string

        if len(a)<8:
            try:
                pack=a[3].text.split(":")[0]
            except:
                pack=str(a[-1]).split(">")[1].replace("</a","").split("<")[0].split(":")[0]
        else:
            pack=str(a[-2]).split(">")[1].replace("</a","").split("<")[0].split(":")[0]


        

        if len(rbp)>=3:
            past_bp=rbpp[0]
            present_bp=rbpp[1]
            future_bp=rbpp[2]

            past_note=str(notes[0]).split(">")[1].replace("</td","")
            present_note=str(notes[1]).split(">")[1].replace("</td","")
            future_note=str(notes[2]).split(">")[1].replace("</td","")
            version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")
        
            past=[artist,"PST",pack,past_note,past_bp,version]
            present=[artist,"PRS",pack,present_note,present_bp,version]
            future=[artist,"FTR",pack,future_note,future_bp,version]

        if len(rbp)>=4:
            beyond_bp=rbpp[3]

            beyond_note=str(notes[3]).split(">")[1].replace("</td","")
            version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")
        
            if "Beyond" in str(soup1):
                beyond=[artist,"BYD",pack,beyond_note,beyond_bp,version]
            else:
                beyond=[artist,"ETR",pack,beyond_note,beyond_bp,version]
        if len(rbp)==5:
            beyond2_bp=rbpp[4]

            beyond2_note=str(notes[4]).split(">")[1].replace("</td","")
            version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")

            beyond2=[artist,"BYD",pack,beyond2_note,beyond2_bp,version]

        if len(tables) ==1:

            img=mt.find_all("img")[0]
            title=img.get("title")
            img_url=img.get("src")
            img_link = img_url.split("jpg")[0]+"jpg"
            createDirectory("jacket/"+pack)
            Image.open(requests.get(img_link, stream=True).raw).save("jacket/"+pack+"/"+img_link.split("/")[-1])
        
            past=[title]+past+[img_link.split("/")[-1]]
            present=[title]+present+[img_link.split("/")[-1]]
            future=[title]+future+[img_link.split("/")[-1]]  
            wr.append(past) 
            wr.append(present) 
            wr.append(future) 

            if len(rbp)==4:
                beyond=[title]+beyond+[img_link.split("/")[-1]]
                wr.append(beyond) 

        elif len(tables)==4:
            i=0
            ppf=[]
            if len(rbp)==3:
                ppf=[past,present,future]
            elif len(rbp)==5:
                ppf=[[past,present,future],beyond,beyond2]
            for t in tables[1:]:

                img=t.find_all("img")[0]
                title=img.get("title")
                img_url=img.get("src")
                img_link = img_url.split("jpg")[0]+"jpg"
                createDirectory("jacket/"+pack)
                Image.open(requests.get(img_link, stream=True).raw).save("jacket/"+pack+"/"+img_link.split("/")[-1])
                if len(ppf[i])==5:
                    if type(img_link)=="list":
                        wr.append([title]+ppf[i]+[img_link[i].split("/")[-1]])
                    else:
                        wr.append([title]+ppf[i]+[img_link.split("/")[-1]])
                else:
                    for pp in ppf[i]:
                        if type(img_link)=="list":
                            wr.append([title]+pp+[img_link[i].split("/")[-1]])
                        else:
                            wr.append([title]+pp+[img_link.split("/")[-1]])
                i=i+1

        elif len(tables)==3:
            i=0
            ppf=[[past,present,future],beyond]
            for t in tables[1:]:
                img=t.find_all("img")[0]
                title=img.get("title")
                img_url=img.get("src")
                img_link = img_url.split("jpg")[0]+"jpg"
                createDirectory("jacket/"+pack)
                Image.open(requests.get(img_link, stream=True).raw).save("jacket/"+pack+"/"+img_link.split("/")[-1])
                if len(ppf[i])==5:
                    if type(img_link)=="list":
                        wr.append([title]+ppf[i]+[img_link[i].split("/")[-1]])
                    else:
                        wr.append([title]+ppf[i]+[img_link.split("/")[-1]])
                else:
                    for pp in ppf[i]:
                        if type(img_link)=="list":
                            wr.append([title]+pp+[img_link[i].split("/")[-1]])
                        else:
                            wr.append([title]+pp+[img_link.split("/")[-1]])
                i=i+1

    
wb.save('data.xlsx')