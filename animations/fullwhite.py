#!/usr/bin/env python2

import sys

from random import randint
from time import sleep

from twinklclient import TwinklSocket, TwinklMessage

HEIGHT = 8
WIDTH = 6

# As viewn from the inside
BOX_MAP = [
			[357,  18, 369, 186, 249, 228,  51],
			[279,  10,  57, 159, 300, 108, 204],
			[261,  42, 183, 201, 273, 246,  15],
			[306, 168,  24, 138, 309, 165,  39],
			[258, 222,  87, 363, 291, 231, 243],
			[252, 114, 180,  75, 282, 141, 033],
			[264, 288, 120, 135, 255,  99, 105],
			[285, 207, 102,  45, 297, 216,  63],
		]


msg = TwinklMessage()

def set_box(x,y,r,g,b):
	if x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT:
		base_address = BOX_MAP[y][x]
		msg[base_address] = r
		msg[base_address + 1] = g
		msg[base_address + 2] = b



if len(sys.argv) != 3:
	print "Usage: %s host priority" % sys.argv[0]
	sys.exit(1)

socket = TwinklSocket(sys.argv[1], "1337")

msg.set_priority(int(sys.argv[2]))

for x in range(0, WIDTH):
	for y in range(0, HEIGHT):
		set_box(x,y, 255, 255, 255)


socket.send(msg)

sleep(5)

msg.reset()
msg.set_priority(0)
socket.send(msg)

msg.destroy()
socket.close()

