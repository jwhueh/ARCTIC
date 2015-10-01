#! /usr/bin/python

from ctypes import *

class FilterWheel(object):
	def __init__(self):
		self.filter = CDLL("./filter_motor.so")
		self.id = 0
		self.fw = None
		self.desPos = None

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
		status = self.filter.moveToFilter(int(pos))
		self.desPos = status
		
		return status

	def status(self):
		"""
		return current status of filter wheel
		"""
		dict = {'id':self.id,'currentEncoder':None, 'desiredEncoder':None, 'power':None,'motor':None, 'hall':None, 'position':None}
		dict['currentEncoder']  = self.filter.currentPos()
		dict['power'] = self.filter.driverStatus()
		dict['motor'] = self.filter.motorStatus()
		hall = self.filter.hallStatus()
		dict['hall'] = str(hall).zfill(4)
		dict['position'] = self.filter.filterPos()
		dict['desiredEncoder'] = self.desPos
		#print dict
		return dict


if __name__ == "__main__":
	f = FilterWheel()
	f.setup()
	#f.home()
	print f.moveToPosition(1)
	print f.status()
	print f.moveToPosition(8)
	print f.status()
	f.stop()
