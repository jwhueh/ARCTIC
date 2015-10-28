#! /usr/bin/python

import os
import time
from ctypes import *

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

	def logit(self, text):
		fout = open(time.strftime("%Y%m%d.home"), 'a')
		t = time.strftime("%Y%m%dT%H%M%S")
		fout.write(t+'\t'+str(text)+'\n')

		fout.close()

	def runHomePythonic(self):
		"""
		let's make this non-blcoking by threading it
		"""
		thread.start_new_thread(homePythonic,())

	def homePythonic(self):
		"""
		create a non-blocking homing routine using the low level ctypes
		for testing purposes lets log and time everything to make sure it will work
		"""
		quit = 0
		x = 0
		self.logit('starting home')
		self.logit('starting motor move to 410000')
		self.moveMotor("410000")
		self.logit('watch those hall effects, this might be tricky')
		while(!quit):
			state = self.status()
			self.logit(str(state))
			if dict['hall'] != '0000' or dict['hall'] != '1000':
				self.stopMotor()
				quit = 1
				self.logit('hey, found it')
			if x>10000:
				return -1
			x+=
		self.zero()
		self.filter.homeVelocity()
		return
				

	def stop(self):
		"""
		stop filter wheel motion
		"""
		self.filter.stopMotor()
		return

	def zero(self):
		self.filter.zero()
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
	print f.status()
	f.home()
	f.moveToPosition(5)
        print f.status()
