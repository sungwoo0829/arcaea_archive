import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
from openpyxl import Workbook

wb = Workbook()
wr= wb.active
wr.append(["song","artist","difficulty","note","bp","version","img"])

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

url = "https://wikiwiki.jp/arcaea/%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB%E9%A0%86"
res = requests.get(url,headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

basetable = soup.find_all('table')
tds = []
for i in range(len(basetable)):
    if i == 0:
        pass
    else:
        tds.append(basetable[i].find_all('a'))

print(tds)


for td in tds:
    
    past=[]
    present=[]
    future=[]
    beyond=[]
    beyond2=[]

    link = td.get("href")
    res1 = requests.get("https://wikiwiki.jp"+str(link),headers=headers)
    res1.raise_for_status()
    soup1 = BeautifulSoup(res1.text, "lxml")

    tables = soup1.find_all("table")

    artist=str(a[0]).split(">")[1].replace("</a","")
    pack=str(a[3]).split(">")[1].replace("</a","")

    p = re.compile("譜面定数 : \d+[.]\d+")
    rbp=p.findall(str(soup1))
    rbpp= re.compile("\d+[.]\d+")[0]

    mt=tables[0]
    a=mt.find_all("a")
    trs=mt.find_all("tr")
    notes=trs[4].find_all("td")

    if len(rbp)>=3:
        past_bp=rbpp.findall(rbp[0])
        present_bp=rbpp.findall(rbp[1])
        future_bp=rbpp.findall(rbp[2])

        past_note=str(notes[0]).split(">")[1].replace("</td","")
        present_note=str(notes[1]).split(">")[1].replace("</td","")
        future_note=str(notes[2]).split(">")[1].replace("</td","")
        version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")
        
        past=[artist,"PST",past_note,past_bp,version]
        present=[artist,"PRS",present_note,present_bp,version]
        future=[artist,"FTR",future_note,future_bp,version]

    if len(rbp)>=4:
        beyond_bp=rbpp.findall(rbp[3])

        beyond_note=str(notes[3]).split(">")[1].replace("</td","")
        version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")
        
        if "Beyond" in str(soup1):
            beyond=[artist,"BYD",beyond_note,beyond_bp,version]
        else:
            beyond=[artist,"ETR",beyond_note,beyond_bp,version]
    if len(rbp)==5:
        beyond2_bp=rbpp.findall(rbp[4])

        beyond2_note=str(notes[4]).split(">")[1].replace("</td","")
        version=str(trs[-2].find_all("td")[0]).split(">")[1].replace("<br class=\"spacer\"/","").replace("ver.","")

        beyond2=[artist,"BYD",beyond2_note,beyond2_bp,version]

    if len(tables) ==2:

        img=mt.find_all("img")[0]
        title=img.get("title")
        img_url=img.get("src")
        img_link = img_url.split("jpg")[0]+"jpg"
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

    elif len(tables)==5:
        i=0
        ppf=[]
        if len(rbp)==3:
            ppf=[past,present,future]
        elif len(rbp)==5:
            ppf=[[past,present,future],beyond,beyond2]
        for t in tables[2:]:

            img=t.find_all("img")[0]
            title=img.get("title")
            img_url=img.get("src")
            img_link = img_url.split("jpg")[0]+"jpg"
            Image.open(requests.get(img_link, stream=True).raw).save("jacket/"+pack+"/"+img_link.split("/")[-1])
            if len(ppf[i])==1:
                wr.append([title]+ppf[i]+[img_link.split("/")[-1]])
            else:
                for pp in ppf[i]:
                    wr.append([title]+pp+[img_link.split("/")[-1]])
            i=i+1



