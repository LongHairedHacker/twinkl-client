#!/usr/bin/env python2
import random

for chan in range(0,512):
	print "%d : %d" % (chan, random.randint(0,255))
