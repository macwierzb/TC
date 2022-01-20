import PIL
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw, ImageFilter

Reference = Image.open(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\reference.png")

Client = Image.open (r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\photo1.png")

Inspection = ImageChops.difference(Reference, Client)

Inspection = Inspection.save(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\Inspection.png")

Inspected = Image.open(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\Inspection.png")

rgba = Inspected.convert("RGBA")
datas = rgba.getdata()
  
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
        # storing a transparent value when we find a black colour
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)  # other colours remain unchanged
  
rgba.putdata(newData)
rgba.save(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\Transparent_image.png")

Transparent= Image.open(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\Transparent_image.png")

back_Reference = Reference.copy()
back_Reference.paste(Transparent, (0,0), Transparent)
back_Reference.save(r"C:\Users\wierz\Desktop\TUM\TECH Challenge\TC_AIproject\\Complete_Inspection.png")


#if Inspection.getbbox() :
  #  Inspection.show() 