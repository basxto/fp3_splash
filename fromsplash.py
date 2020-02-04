#!/usr/bin/env python3
"""
Copyright (c) 2020 Sebastian "basxto" Riedel <git@basxto.de>

Based on fbcon_extract_to_screen() from fbcon.c of little kernel
https://web.archive.org/web/20200203204634/https://source.codeaurora.org/quic/la/kernel/lk/tree/dev/fbcon/fbcon.c?h=LA.UM.8.6.r1-03400-89xx.0#n495
https://web.archive.org/web/20200203205934/https://source.codeaurora.org/quic/la/kernel/lk/tree/include/dev/fbcon.h?h=LA.UM.8.6.r1-03400-89xx.0

 * Copyright (c) 2008, Google Inc.
 * All rights reserved.
 *
 * Copyright (c) 2009-2015, 2018, 2019 The Linux Foundation. All rights reserved.
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
from PIL import Image

with open('splash', 'rb') as fl:
    data = fl.read()

if data[:0x8] != b'SPLASH!!':
    exit("Wrong magic number in splash image")

# header takes up 512 bytes and starts with magic number
magic, width, height, itype, blocks, offset = struct.unpack("<8s5I", data[:28])

print("magic: ", magic, "; width: ", width, "; height: ", height, "; type: ", itype, "; blocks: ", blocks, "; offset: ", offset)

pos = 0x200 + offset
x = 0
y = 0

img = Image.new( 'RGB', (width,height), "black") # create a new black image
pixels = img.load() # create the pixel map

while y < height:
    run = data[pos]
    repeat_run = (run & 0x80)
    runlen = (run & 0x7f) + 1
    pos += 1
    for runpos in range(0, runlen):
        pixels[x,y] = (data[pos], data[pos+1], data[pos+2])
        if x < width:
            x += 1
        if not repeat_run:
            pos += 3
    if repeat_run:
        pos += 3
    if x >= width:
        y += 1
        x = 0

img.save("splash.png")
