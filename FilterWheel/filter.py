#! /usr/bin/python

import os
import time
from ctypes import *
import random

class FilterWheel(object):
	def __init__(self):
		#self.filter = CDLL("./filter_motor.so")
                self.filter = CDLL(os.path.join(os.getenv("FILTERDIR"), "filter_motor.so"))
		self.id = 0
		self.fw = None
		self.desPos = None

	def connect(self):
		"""
		initiate filter wheel communication
		"""
		self.filter.setup()
		return

	def disconnect(self):
                """
                close filter wheel communication
                """
                self.filter.close()
                return

	def home(self):
		"""
		home filter wheel and set the filter wheel id
		"""
		id_binary = self.filter.home()
		self.id = int(str(id_binary),2)
		if(self.id != 0):
			self.fw = 0
		print "Filter ID: %s, %s" % (id_binary, self.id)
		return self.id

	def stop(self):
		"""
		stop filter wheel motion
		"""
		self.filter.stopMotor()
		return

	def zero(self):
		self.filter.zero()
		return

	def moveArb(self, pos = None):
		"""
		move to an arbitrary position in step space
		arguments:
			int pos - steps to move
		return: 
			0 - fail
			1 - completed
			-1 - fail
		"""
		self.filter.moveMotor(int(pos))

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
		stepPos = self.filter.moveToFilter(int(pos))
		print stepPos
		self.desPos = stepPos
		st = self.status()
		print st
		#for x in range(100):
		#	print self.status()
		
		while  st['currentStep'] != st['desiredStep']:
			st = self.status()
			print st
			if st['desiredStep'] == None:
				return stepPos
		
		return stepPos

	def status(self):
		"""
		return current status of filter wheel
		"""
		dict = {'id':self.id,'currentStep':None, 'currentStep':None, 'desiredStep':None, 'power':None,'motor':None, 'hall':None, 'position':None}
		dict['power'] = self.filter.driverStatus()
		dict['currentEncoder']  = self.filter.currentEnc()
		dict['motor'] = self.filter.motorStatus()
		hall = self.filter.hallStatus()
		dict['hall'] = str(hall).zfill(4)
		dict['position'] = self.filter.filterPos()
		dict['desiredStep'] = self.desPos
		dict['currentStep'] = self.filter.currentPos()
		#print dict
		return dict


if __name__ == "__main__":
	f = FilterWheel()
	f.connect()
	#f.zero()
	print f.status()
	#f.home()
	f.moveToPosition(random.randrange(0,5,1))
	#f.moveToPosition(0)
