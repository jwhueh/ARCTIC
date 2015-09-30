#! /usr/bin/python

import time
from ctypes import *

class FilterWheel(object):
	def __init__(self):
		self.filter = CDLL("./filter_motor.so")
		self.id = 0

	def setup(self):
		"""
		initiate filter wheel communication
		"""
		self.filter.setup()
		return

	def home(self):
		"""
		home filter wheel and set the filter wheel id
		"""
		id_binary = self.filter.home()
		self.id = int(str(id_binary),2)
		print "Filter ID: %s, %s" % (id_binary, self.id)
		return

	def stop(self):
		"""
		stop filter wheel motion
		"""
		pass

	def moveToPosition(self, pos):
		"""
		move to a specific filter wheel position
		arguments: 
			int pos - filter position between 1 and 6
		status:
			0 - fail
			1 - succeed
			-1 - unknown
		"""
		status = self.filter.moveToFilter(pos)
		print "Filter Wheel Move Status: %s" % str(status)
		return status

	def status(self):
		"""
		return current status of filter wheel
		"""
		encPos = self.filter.currentPos()
		motorPower = self.filter.motorStatus()
		hall = self.filter.hallStatus()	

		print encPos, motorPower, str(hall).zfill(4)
		return


if __name__ == "__main__":
	f = FilterWheel()
	f.setup()
	#f.home()
	#f.moveToPosition(6)
	f.status()
