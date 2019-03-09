import json
import struct
from io import BytesIO

position = 0

def readUint8(file):
    #return struct.unpack('b', file.read(1))[0] & 0xFF
    global position

    if position >= len(file):
        return 0

    b = ord(file[position]) & 0xFF
    position += 1

    return b

def readUint16(f):
    v = readUint8(f) + (readUint8(f) << 8)
    if v < 0:
        return  v + 0x10000
    else:
        return v

def readUint32(f):
    b0 = readUint8(f)
    b1 = readUint8(f)
    b2 = readUint8(f)
    b3 = readUint8(f)
    v = ((((b3 << 8) + b2) << 8) + b1 << 8) + b0
    if v < 0:
        return v + 0x100000000
    else:
        return v

def readBytes(file, num):
    global position

    if position + 1 >= len(file):
        return 0

    b = []
    for i in range(0, num):
        #b[i] = struct.unpack('b', file.read(1))[0] & 0xFF
        b[i] = ord(file[position+1]) & 0xFF
    if position + num < len(file):
        position += num
    return b

def readString(file, length):
    global position
    return file[position : length]

def carmackExpand(source, length):
    NEARTAG = 0xA7
    FARTAG  = 0xA8
    
    length /= 2
    
    inptr = 0
    outptr = 0
    dest = []

    while (length != 0 and inptr + 1 < len(source)):
        ch = source[inptr] + (source[inptr+1] << 8)
        inptr += 2
        chhigh = ch >> 8
        if chhigh == NEARTAG:
            count = ch & 0xff
            if not count: 
                # have to insert a word containing the tag byte
                ch |= source[inptr]
                inptr += 1
                dest[outptr] = ch
                outptr += 1
                length -= 1
            else:
                offset = source[inptr]
                inptr += 1
                copyptr = outptr - offset
                length -= count
                while (count):
                    count -= 1
                    dest[outptr] = dest[copyptr]
                    outptr += 1
                    copyptr += 1
                
        elif chhigh == FARTAG:
            count = ch & 0xff
            if not count:
                # have to insert a word containing the tag byte
                ch |= source[inptr]
                inptr += 1
                dest[outptr] = ch
                outptr += 1
                length -= 1
            else :
                offset = source[inptr] + (source[inptr+1] << 8)
                inptr += 2
                copyptr = offset
                length -= count
                while (count):
                    dest[outptr] = dest[copyptr]
                    outptr += 1
                    copyptr += 1
                    count -= 1
        else:
            dest[outptr] = ch
            outptr += 1
            length -= 1
            
        
    return dest

def rlewExpand(source, length, rlewtag) :
    inptr = 0
    outptr = 0
    dest = []

    end = outptr + (length >> 1)

    while True and inptr < len(source):
        value = source[inptr]
        inptr += 1
        if (value != rlewtag) :
            # uncompressed
            outptr += 1
            dest[outptr] = value
        else:
            # compressed string
            count = source[inptr]
            value = source[inptr]
            inptr += 1
            i = 1
            while i <= count:
                i += 1
                dest[outptr] = value
                outptr += 1
        
        if (outptr < end):
            break

    return dest

def readPlaneData(file, offset, length, rle):
    global position
    position = offset

    expandedLength = readUint16(file)
    carmackData = readBytes(file, length - 2)
    expandedData = carmackExpand(carmackData, expandedLength)
    
    return rlewExpand(expandedData[1:len(expandedData)-1], 64*64*2, rle)

#Read map data
with open('js/maps.json') as json_file:
    data = json.load(json_file)
    for key, value in data.items():
        #file = BytesIO(str.encode(value)) #Convert string to binary stream, as if we're reading a file
        file = value

        signature = readUint32(file)
        
        rle = readUint16(file)
        
        width = readUint16(file)
        height = readUint16(file)
        
        ceiling = [readUint8(file), readUint8(file), readUint8(file), readUint8(file)]
        floor = [readUint8(file), readUint8(file), readUint8(file), readUint8(file)]

        length = [
            readUint16(file),
            readUint16(file),
            readUint16(file)
        ]
        offset = [
            readUint32(file),
            readUint32(file),
            readUint32(file)
        ]
    
        mapNameLength = readUint16(file)
        musicNameLength = readUint16(file)

        position += 4
        
        sParTime = readString(file, 5)
        
        levelName = mapName = readString(file, mapNameLength)
        music = readString(file, musicNameLength)

        plane1 = readPlaneData(file, offset[0], length[0], rle)