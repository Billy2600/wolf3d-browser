import json
import struct
from io import BytesIO

#Read map data
with open('js/maps.json') as json_file:
    data = json.load(json_file)
    for key, value in data.items():
        f = BytesIO(str.encode(value)) #Convert string to binary stream, as if we're reading a file
        print(struct.unpack('I', f.read(4))[0])
        print(struct.unpack('h', f.read(2))[0])
        print(bin(struct.unpack('h', f.read(2))[0]))
        print(struct.unpack('h', f.read(2))[0])
        print(struct.unpack('B', f.read(1))[0])
        print(' ')