#!/usr/bin/env python2

from ctypes import *

_TWINKL_CLIENT = cdll.LoadLibrary("../bin/twinklclient.so")

_TWINKL_CLIENT.twinklmsg_create.argtypes = []
_TWINKL_CLIENT.twinklmsg_create.restype = c_void_p

_TWINKL_CLIENT.twinklmsg_destroy.argtypes = [c_void_p]
_TWINKL_CLIENT.twinklmsg_destroy.restype = None

_TWINKL_CLIENT.twinklmsg_reset.argtypes = [c_void_p]
_TWINKL_CLIENT.twinklmsg_reset.restype = None

_TWINKL_CLIENT.twinklmsg_set_priority.argtypes = [c_void_p, c_ubyte]
_TWINKL_CLIENT.twinklmsg_set_priority.restype = None

_TWINKL_CLIENT.twinklmsg_set_value.argtypes = [c_void_p, c_ushort, c_ubyte]
_TWINKL_CLIENT.twinklmsg_set_value.restype = None

_TWINKL_CLIENT.twinklmsg_unset_value.argtypes = [c_void_p, c_ushort]
_TWINKL_CLIENT.twinklmsg_unset_value.restype = None

_TWINKL_CLIENT.twinklsocket_close.argtypes = [c_int]
_TWINKL_CLIENT.twinklsocket_close.restype = None

_TWINKL_CLIENT.twinklsocket_open.argtypes = [c_char_p, c_char_p]
_TWINKL_CLIENT.twinklsocket_open.restype = c_int

_TWINKL_CLIENT.twinklsocket_send.argtypes = [c_int, c_void_p]
_TWINKL_CLIENT.twinklsocket_send.restype = c_int


class TwinklSocket(object):
	def __init__(self, host, port):
		self._socket = _TWINKL_CLIENT.twinklsocket_open(host, port)
		if self._socket < 0:
			print self._socket
			raise RuntimeError("Could not open socket.")

	def close(self):
		_TWINKL_CLIENT.twinklsocket_close(self._socket)

	def send(self, msg):
		result = _TWINKL_CLIENT.twinklsocket_send(self._socket, msg._pointer)
		if result < 0:
			raise RuntimeError("Could not send packet")


class TwinklMessage(object):
	def __init__(self):
		self._pointer = _TWINKL_CLIENT.twinklmsg_create()

	def destroy(self):
		_TWINKL_CLIENT.twinklmsg_destroy(self._pointer)

	def reset(self):
		_TWINKL_CLIENT.twinklmsg_reset(self._pointer)

	def set_priority(self, priority):
		_TWINKL_CLIENT.twinklmsg_set_priority(self._pointer, c_ubyte(priority))

	def set_value(self, channel, value):
		_TWINKL_CLIENT.twinklmsg_set_value(self._pointer, c_ushort(channel), c_ubyte(value))

	def unset_value(self, channel):
		_TWINKL_CLIENT.twinklmsg_unset_value(self._pointer, c_ushort(channel))


	def __setitem__(self, channel, value):
		if value == None:
			self.unset_value(channel)
		else:
			self.set_value(channel, int(value))




