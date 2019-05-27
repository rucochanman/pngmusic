# -*- coding: utf-8 -*-
from struct import pack
from PIL import Image

im = Image.open('Lenna_original.png')

outfile = open('Lenna_original.raw','w')

pix = im.getdata()
pixb = []


for i in range(len(pix)):
    for j in range(3):
        pixb.append(pix[i][j])


data = pack("%dB" % len(pixb), *pixb)

outfile.write(data)

outfile.close()

