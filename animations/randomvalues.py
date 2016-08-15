#!/usr/bin/env python2

import sys
import signal

from colorsys import hsv_to_rgb
from random import randint
from time import sleep

from twinklclient import TwinklSocket, TwinklMessage

msg = TwinklMessage()
socket = None
priority = 0

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


while(True):
	for i in range(0, 512/3):
		rgb = hsv_to_rgb(randint(0, 1024) / 1024.0, 1.0, randint(0, 1024) / 1024.0)
		msg[i * 3] = int(rgb[0] * 255)
		msg[i * 3 + 1] = int(rgb[1] * 255)
		msg[i * 3 + 2] = int(rgb[2] * 255)

	socket.send(msg)
	sleep(0.25)
