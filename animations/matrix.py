#!/usr/bin/env python2

import sys
import signal

from random import randint
from time import sleep

from twinklclient import TwinklSocket, TwinklMessage

WIDTH = 6
HEIGHT = 8

# As viewn from the inside   
BOX_MAP = [
			[357,  18, 369, 186, 249, 228,  51],
			[279,  9,  57, 159, 300, 108, 204],
			[261,  42, 183, 201, 273, 246,  15],
			[306, 168,  24, 138, 309, 165,  39],
			[258, 222,  87, 363, 291, 231, 243],
			[252, 114, 180,  75, 282, 141, 33],
			[264, 288, 120, 135, 255,  99, 105],
			[285, 207, 102,  45, 297, 216,  63],
		]


msg = TwinklMessage()
socket = None
priority = 0

def set_box(x,y,r,g,b):
	if x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT:
		base_address = BOX_MAP[y][x]
		msg[base_address] = int(r)
		msg[base_address + 1] = int(g)
		msg[base_address + 2] = int(b)
	

def clear():
	for x in range(0, WIDTH):
		for y in range(0, HEIGHT):
			set_box(x, y, 0, 0, 0)


class Column(object):
	def __init__(self):
		self.x = randint(0, WIDTH)
		self.y = randint(-HEIGHT/2, -1)
		self.speed = randint(1, 10)
		self.length = randint(4, HEIGHT)
		self.count = 0
	
	def render(self):
		for y in range(self.y - self.length, self.y):
			green = 255 - (255.0 / self.length) * (self.y - y)
			set_box(self.x, y, 0, green, 0)

		set_box(self.x, self.y, 64, 255, 64)

	def update(self):
		self.count = (self.count + 1) % self.speed
		if(self.count == 0):
			self.y += 1



def terminate(signal, frame):
	msg.reset()
	msg.set_priority(priority)
	socket.send(msg)

	if socket:
		socket.close()
	msg.destroy()
	sys.exit(0)


signal.signal(signal.SIGINT, terminate)

if len(sys.argv) != 3:
	print "Usage: %s host priority" % sys.argv[0]
	sys.exit(1)

socket = TwinklSocket(sys.argv[1], "1337")

priority = int(sys.argv[2])
msg.set_priority(priority)

columns = []
# Add some initial collums
for i in range(0, 16):
	columns.append(Column())


while(True):
	clear();
	
	columns = sorted(columns, key = lambda c: -c.y)

	for i in range(0,len(columns)):
		if columns[i].y - columns[i].length > HEIGHT:
			columns[i] = Column()
		columns[i].update()
		columns[i].render()

	socket.send(msg)
	sleep(0.05)
