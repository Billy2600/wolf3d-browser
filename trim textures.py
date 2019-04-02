#This is a python script I wrote to strip out the darker variations of textures
from PIL import Image
textures = Image.open('art/walls-shaded/64/walls_orig.png')
width, height = textures.size

result = Image.new('RGB', (width, int(height/2)))

for y in range(0, height, 128):
    crop = textures.crop((0,y,64,y + 64))
    result.paste(crop, (0, max(0, int(y / 2))))

result.save('result.png')
#result.show()
