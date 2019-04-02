#This is a python script I wrote to combine the object pictures to be used in the map editor
from PIL import Image
import sys

#Global vars
path = 'art/sprites/128/wolf3d sprites/'
resultPath = 'art/sprites/128/'
wallsPath = 'art/walls-shaded/64/'

# Paste images onto resulting image
# result = image to be pasted onto
# yPos = Y position of paste
# img1 = first image to paste
# img2 = second image to paste (optional), will be blended with the first
# Returns: Nothing
def pasteImages(result, yPos, img1, img2 = None):
    if(img2 != None):
        imgBlended = Image.blend(img1, img2, 0.7)
        result.paste(imgBlended, (0, yPos), mask = imgBlended)
    else:
        result.paste(img1, (0, yPos), mask = img1)

# Replace color in image
# img = Image to replace color in
# before = color to replace
# after = color to replace with
# Returns: Nothing
def replaceColor(img, before, after):
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == before:
                pixdata[x, y] = after

# Load image
# Loads and performs all special operations on image
# Returns: new Image
def loadImage(filename):
    img = Image.open(path + filename).convert('RGBA')
    replaceColor(img, (152, 0, 136, 255), (0, 0, 0, 0))
    return img


## MAIN CODE EXECUTION ##
result = Image.new('RGBA', (64, 259 * 64), (0, 0, 0, 0))
imgArrow = Image.open(path + 'up_arrow.png')
imgMoving = Image.open(path + 'moving.png')


# 19 - Start (North)
img = loadImage('Sprite-514.bmp')
pasteImages(result, 64 * 19, img, imgArrow)
# 20 - Start (East)
pasteImages(result, 64 * 20, img, imgArrow.rotate(270))
# 21 - Start (South)
pasteImages(result, 64 * 21, img, imgArrow.rotate(180))
# 22 - Start (West)
pasteImages(result, 64 * 22, img, imgArrow.rotate(90))

# These are all in order pretty much
i = 23
while(i <= 70):
    img = loadImage('Sprite-' + str(i + 85) + '.bmp')
    pasteImages(result, 64 * i, img)
    i += 1

# 90 - East turn
pasteImages(result, 64 * 90, imgArrow.rotate(270))
# 91 - North-East turn
pasteImages(result, 64 * 91, imgArrow.rotate(315))
# 92 - North turn
pasteImages(result, 64 * 92, imgArrow)
# 93 - North-West turn
pasteImages(result, 64 * 93, imgArrow.rotate(45))
# 94 - West turn
pasteImages(result, 64 * 94, imgArrow.rotate(90))
# 95 - South-West turn
pasteImages(result, 64 * 95, imgArrow.rotate(135))
# 96 - South turn
pasteImages(result, 64 * 96, imgArrow.rotate(180))
# 97 - South-East turn
pasteImages(result, 64 * 97, imgArrow.rotate(315))
# 98 - Secret door
img = loadImage('secret.png')
pasteImages(result, 64 * 98, img)
# 99 - End game trigger
img = loadImage('endgame.png')
pasteImages(result, 64 * 99, img)

#          East, North, West South
directions = [ 270, 0, 90, 180 ]

# 108 - 111 - Guard 1 standing
img = loadImage('Sprite-156.bmp')
for i in range(4): #Get all four directions
    pasteImages(result, 64 * (108 + i), img, imgArrow.rotate(directions[i]))

# 112 - 115 - Guard 1 moving
for i in range(4):
    pasteImages(result, 64 * (112 + i), img, imgMoving.rotate(directions[i]))

# 116 - 119 - Officer 1 standing
img = loadImage('Sprite-344.bmp')
for i in range(4):
    pasteImages(result, 64 * (116 + i), img, imgArrow.rotate(directions[i]))

# 120 - 123 - Officer 1 moving
for i in range(4):
    pasteImages(result, 64 * (120 + i), img, imgMoving.rotate(directions[i]))

# 124 - Dead guard
img = loadImage('Sprite-201.bmp')
pasteImages(result, 64 * 124, img)

# 126 - 129 - SS 1 standing
img = loadImage('Sprite-244.bmp')
for i in range(4):
    pasteImages(result, 64 * (126 + i), img, imgArrow.rotate(directions[i]))

# 130 - 133 - SS 1 moving
for i in range(4):
    pasteImages(result, 64 * (130 + i), img, imgArrow.rotate(directions[i])) 

# 138 - 141 - Dog 1 moving
img = loadImage('Sprite-215.bmp')
for i in range(4):
    pasteImages(result, 64 * (138 + i), img, imgArrow.rotate(directions[i]))

result.save(resultPath + 'objects.png')

#Combine with walls image
imgWalls = Image.open(wallsPath + 'walls_trimmed.png')
imgCombined = Image.new('RGBA', (64, imgWalls.height + result.height), (0, 0, 0, 0))
imgCombined.paste(imgWalls, (0,0))
imgCombined.paste(result, (0, imgWalls.height))

imgCombined.save(wallsPath + 'walls.png')