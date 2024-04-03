from PIL import Image

img=Image.open("test1.png")
img=img.crop((51,655,685,1288)).resize((512,512))
img.save("img_crop.png",format="JPEG")