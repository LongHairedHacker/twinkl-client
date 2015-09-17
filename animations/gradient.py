#!/usr/bin/env python2

from random import randint
from time import sleep
from subprocess import Popen, PIPE

HEIGHT = 8
WIDTH = 6

# As viewn from the inside   
BOX_MAP = [
			[357,  18, 369, 186, 249, 228,  51],
			[279,  9,  57, 159, 300, 108, 204],
			[261,  42, 183, 201, 273, 246,  15],
			[306, 168,  24, 138, 309, 165,  39],
			[258, 222,  87, 363, 291, 231, 243],
			[252, 114, 180,  75, 282, 141, 033],
			[264, 288, 120, 135, 255,  99, 105],
			[285, 207, 102,  45, 297, 216,  63],
		]


channels = {}

def set_box(x,y,r,g,b):
	if x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT:
		base_address = BOX_MAP[y][x]
		channels[base_address] = r
		channels[base_address + 1] = g
		channels[base_address + 2] = b


def output_channels():
	for channel, value in channels.items():
		print "%d : %d" % (channel, value)
	print ""


for x in range(0, WIDTH):
	for y in range(0, HEIGHT):
		set_box(x,y, 100 + (155 / WIDTH) * (x + 1), 100 + (155 / HEIGHT) * (y + 1), 0)


output_channels()
