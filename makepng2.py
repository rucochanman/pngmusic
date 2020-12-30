# -*- coding: utf-8 -*-
from sys import stdout
from struct import pack
from zlib import crc32, compress

width, height = 5, 5
depth, cType = 8, 2

#signature
outfile = open('out.png','wb')
outfile.write(b'\x89PNG\r\n\x1a\n')

#IHDR
ihdrSize = pack('!I', 13)
ihdrType = pack('!4s', b'IHDR')
ihdrData = pack('!IIBBBBB', width, height, depth, cType, 0, 0, 0)
ihdrCrc = pack('!I', crc32(ihdrType + ihdrData))
ihdrChunk = ihdrSize + ihdrType + ihdrData + ihdrCrc
outfile.write(ihdrChunk)


#IDAT
rgb = [255, 0, 0]
line = []
filType = 0

for i in range(height):
    line.append(filType)
    for k in range(width):
        for j in range(3):
            line.append(rgb[j])

data = pack("%dB" % len(line), *line)


idatSize = pack('!I', len(data))
idatType = pack('!4s', b'IDAT')
idatData = compress(data, 0)
idatCrc = pack('!I', crc32(idatType + idatData))
idatChunk = idatSize + idatType + idatData + idatCrc
outfile.write(idatChunk)


#IEND#
iendSize = pack('!I', 0)
iendType = pack('!4s', b'IEND')
iendCrc = pack('!I', crc32(iendType))
iendChunk = iendSize + iendType + iendCrc
outfile.write(iendChunk)

outfile.close()
