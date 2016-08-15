#!/usr/bin/env python2

import sys
import signal
import colorsys

from random import randint
from time import sleep

from twinklclient import TwinklSocket, TwinklMessage

WIDTH = 12
HEIGHT = 8

MAX_GENS = 180

cells = []

msg = None
socket = None
priority = 0

def set_box(x,y,r,g,b):
	if x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT:
		base_address = (y * WIDTH + x) * 3
	 	msg[base_address] = b
		msg[base_address + 1] = r
		msg[base_address + 2] = g


def clear():
	for x in range(0, WIDTH):
		for y in range(0, HEIGHT):
			set_box(x, y, 0, 0, 0)


def terminate(signal, frame):
	if msg:
		msg.reset()
		msg.set_priority(priority)
		socket.send(msg)
		msg.destroy()

	if socket:
		socket.close()
	sys.exit(0)


class CellStates(object):
	DEAD = 0
	BORN = 1
	ALIVE = 2
	LONELY = 3
	CROWED = 4



class Cell(object):
	def __init__(self, x, y):
		self._x = x
		self._y = y
		self._status = CellStates.DEAD
		self._next_status = CellStates.DEAD

	def randomize(self):
		if randint(0,10) % 2 == 0:
			self._next_status = CellStates.BORN

	def _get_neighbour(self, dx, dy):
		x = self._x + dx
		if x >= WIDTH:
			x = x - WIDTH
		if x < 0:
			x = x + WIDTH

		y = self._y + dy
		if y >= HEIGHT:
			y = y - HEIGHT
		if y < 0:
			y = y + HEIGHT

		return cells[x][y]

	def _count_neighbours(self):
		count = 0
		for dx in [-1, 0, 1]:
			for dy in [-1, 0, 1]:
				if self._get_neighbour(dx, dy).is_alive() and not (dx == 0 and dy == 0):
					count = count + 1
		return count


	def calculate_next_status(self):
		neighbours = self._count_neighbours()
		if self._status == CellStates.DEAD or self._status == CellStates.LONELY or self._status == CellStates.CROWED:
			if neighbours == 3:
				self._next_status = CellStates.BORN
			else:
				self._next_status = CellStates.DEAD

		elif self._status == CellStates.ALIVE or self._status == CellStates.BORN:
			if neighbours < 2:
				self._next_status = CellStates.LONELY
			elif neighbours > 3:
				self._next_status = CellStates.CROWED
			else:
				self._next_status = CellStates.ALIVE

	def flip(self):
		self._status = self._next_status

	def is_alive(self):
		return self._status == CellStates.ALIVE or self._status == CellStates.BORN

	def get_status(self):
		return self._status



if __name__== "__main__":

	signal.signal(signal.SIGINT, terminate)

	if len(sys.argv) != 3:
		print "Usage: %s host priority" % sys.argv[0]
		sys.exit(1)

	socket = TwinklSocket(sys.argv[1], "1337")
	msg = TwinklMessage()

	priority = int(sys.argv[2])
	msg.set_priority(priority)

	for x in range(0, WIDTH):
		collumn = []
		for y in range(0, HEIGHT):
			cell = Cell(x,y)
			cell.randomize()
			collumn += [cell]
		cells += [collumn]

	gens = 0
	while(True):

		stale = True
		clear()
		for x in range(0, WIDTH):
			for y in range(0, HEIGHT):
				cells[x][y].flip()

				if cells[x][y].get_status() == CellStates.DEAD:
					set_box(x, y, 0, 0, 0)
				elif cells[x][y].get_status() == CellStates.BORN:
					set_box(x, y, 0, 0, 255)
					stale = False
				elif cells[x][y].get_status() == CellStates.ALIVE:
					set_box(x, y, 0, 255, 0)
				elif cells[x][y].get_status() == CellStates.LONELY:
					set_box(x, y, 255, 255, 0)
					stale = False
				elif cells[x][y].get_status() == CellStates.CROWED:
					set_box(x, y, 255, 0, 255)
					stale = False

		socket.send(msg)
		sleep(0.5)
		#raw_input()

		print gens

		for x in range(0, WIDTH):
			for y in range(0, HEIGHT):
				if stale or gens > MAX_GENS:
					cells[x][y].randomize()
				else:
					cells[x][y].calculate_next_status()

		if stale or gens > MAX_GENS:
			gens = 0
		else:
			gens = gens + 1
