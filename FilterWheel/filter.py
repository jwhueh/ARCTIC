#! /usr/bin/python

from ctypes import *

class FilterWheel(object):
	def __init__(self):
		self.filter = CDLL("./filter_motor.so")
		self.filter.setup();
		self.filter.home();

f = FilterWheel()
