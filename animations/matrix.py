#!/usr/bin/env python2

from random import randint
from time import sleep
from subprocess import Popen, PIPE

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

	output_channels()
	sleep(0.050)
