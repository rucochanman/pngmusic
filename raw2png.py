# -*- coding: utf-8 -*-
from sys import stdout
from struct import pack
from zlib import crc32, compress
import random

outfile = open('Lenna_out.png','w')

width, height = 1280, 1280
depth, color_type = 8, 2
hflag = 0
bflag = 0
acount = 0
wcount = 0
count = 0
inflag = 4
bdata = []
block0 = [65527+4,65529+2,65531+4,65531+2,65531+4,65535+2,65535+4,65523+2,65531+4,65535+2]
block1 = [65535+4,65535+2,65535+4,65535+2,65535+4,65509+2,65529+4,65535+2,65535+4,65535+2]
block2 = [65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2]
block3 = [65535+4,65475+2,65531+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2]
block4 = [65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2]
block5 = [65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2,65535+4,65535+2]
block6 = [65535+4,65535+2,65535+4,65413+2,65529+4,65535+2,65535+4,65535+2,65535+4,65535+2]

block = block0 + block1 + block2 + block3 + block4 + block5 + block6 + block5 + block5 + block5 + block5 + block5 + block5

# グラデーションのベタデータ
test_data = open('Lenna_original.raw','r')

for i in range(height):

    wcount = 0

 
    if hflag == 0:
        bdata += [0,0,0,0]
        count += 4
        wcount += 4
        hflag = 1
    elif bflag == 1:
        bdata += [0,0,0,0,0,0,0,0,0,0]
        count += 10
        wcount += 10
        bflag = 0
    else:
        bdata += [0,0,0,0,0,0,0,0,0,0]
        count += 10
        wcount += 10
        hflag = 0
    
    for k in range(width*3):

        count += 1
        wcount += 1

        if count == block[acount]:
            count = 0
            acount += 1
            data = test_data.read(1)
            bdata.append(ord(data))
            inflag = 0
            if hflag == 1:
                bflag = 1
            else:
                hflag = 1
                                    
        else:            
            data = test_data.read(1)
            if inflag > 3:
                bdata.append(ord(data))
        inflag += 1
          

line = bdata

# data
def chunk(type, data):
  return pack('!I4s%dsi' % len(data), len(data), type, data, crc32(type + data))

# signiture
outfile.write('\x89PNG\r\n\x1a\n')

# header
outfile.write(chunk('IHDR', pack("!IIBBBBB", width+2, height, depth, color_type, 0, 0, 0)))

# pix data
img_data = ''.join(pack("%dB" % len(line), *line))
outfile.write(chunk("IDAT", compress(img_data,0)))

# end
outfile.write(chunk('IEND', ''))

outfile.close()
