#!/usr/bin/env python3
"""
 * Copyright (c) 2020 Sebastian "basxto" Riedel <git@basxto.de>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the 
 *    distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
"""

import struct
import math
from PIL import Image


im = Image.open('splash.png')
pixels = im.load()
width, height = im.size
magic = b'SPLASH!!'
itype = 1 # 1 since we compress
blocks = 0
offset = 0

size = 11534336 #11MiB
with open('splash', 'wb') as fl:
    # fill with zeros
    fl.seek(size-1)
    fl.write(bytearray(1))
    # write image
    fl.seek(0x200)
    for y in range(0, height):
        last = pixels[0,y]
        # pixels can be repeated with 0x80
        reps = 0
        for x in range(1, width):
            if reps == 127 or pixels[x,y][0] != last[0] or pixels[x,y][1] != last[1] or pixels[x,y][2] != last[2]:
                fl.write(bytearray([reps | 0x80, last[2], last[1], last[0]]))
                blocks += 4
                last = pixels[x,y]
                reps = 0
            else:
                reps += 1
        fl.write(bytearray([reps | 0x80, last[2], last[1], last[0]]))
        blocks += 4
    blocks = math.ceil(blocks/512)
    # write header to beginning
    header = struct.pack("<8s5I", magic, width, height, itype, blocks, offset)
    fl.seek(0)
    fl.write(header)

print("Blocks:", blocks)