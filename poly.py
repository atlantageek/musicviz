import math
from PIL import Image, ImageDraw
from PIL import ImagePath 
  
side = 6
xy = [ (0,0),(50,50),(0,100)
    ]  
  
image = ImagePath.Path(xy).getbbox()  
size = list(map(int, map(math.ceil, image[2:])))
  
img = Image.new("RGB", size, "#f9f9f9") 
img1 = ImageDraw.Draw(img)  
img1.polygon(xy, fill ="#eeeeff", outline ="blue") 
print(math.sin(math.radians(0)),math.sin(math.radians(90)),math.sin(math.radians(180)),math.sin(math.radians(270)))
img.show()