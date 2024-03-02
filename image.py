from PIL import Image, ImageDraw, ImageFilter

im=Image.open("test1.png")

mask = Image.new('L', im.size,0)
draw = ImageDraw.Draw(mask)
draw.rectangle([(30,150),(870,1046)],fill=255)
mask.save('mask.png')

blurred = im.filter(ImageFilter.GaussianBlur(10))

im.paste(blurred, mask=mask)
im.save("bImg.png")