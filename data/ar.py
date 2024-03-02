import requests
from bs4 import BeautifulSoup
from PIL import Image

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

url = "https://wikiwiki.jp/arcaea/%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB%E9%A0%86"
res = requests.get(url,headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')


tds = soup.find_all('a')

i=0
for td in tds:
    i=i+1
    if i ==1:
        pass
    elif str(td.get("class"))=="['rel-wiki-page']":
        title = td.get("title")
        link = td.get("href")
        res1 = requests.get("https://wikiwiki.jp"+str(link),headers=headers)
        res1.raise_for_status()
        soup1 = BeautifulSoup(res1.text, "lxml")

        imgs = soup1.find_all("img")

        for img in imgs:
            img_url = img.get("src")
        
            if img.get("width")==img.get("height") and "https://cdn.wikiwiki.jp/to/w/arcaea/" in img_url:
                if "https://cdn.wikiwiki.jp/to/w/arcaea/FrontPage" in img_url:
                    pass
                else:
                    img_link = ""
                    if "webp"in img_url:
                        img_link = img_url.split(".webp")[0]
                    else:
                        img_link = img_url.split("?rev=")[0]
                    Image.open(requests.get(img_link, stream=True).raw).save(img_link.split("/")[-1])
                    print(img_url)
                    
            else:
                pass
            
        else:
            pass




