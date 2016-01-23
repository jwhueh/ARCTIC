#! /usr/bin/python

import os
import time
from ctypes import *
import random
import numpy as np

class FilterWheel(object):
	def __init__(self):
                self.filter = CDLL(os.path.join(os.getenv("FILTERDIR"), "filter_motor.so"))
		self.id = 0
		self.fw = None
		self.desPos = None
		self.debug = False
		self.abortStatus = False
		self.filterDelta = 1325
		self.homingState = False


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

	def abort(self, toggle = None):
		"""
		set the abort flag
		"""
		self.abortStatus = toggle
		return toggle

	def debugMode(self, toggle = None):
		"""
		set the debug flag
		"""
		self.debug = toggle
		return toggle

	def home(self):
		"""
		home filter wheel and set the filter wheel id
		"""

		crossArr = []
		self.homingState = True
		while self.abortStatus == False:
			print time.strftime("%Y%m%dT%H%M%S  homing: starting home routine")
			self.zero()
			self.moveArb("20000")
			time.sleep(1) #so that it always completes one revolution even if at home
			for x in range(2000):
				stat = self.status()
				hall = stat['hall']
				if hall != '0111' and hall != '1111' and len(crossArr) > 4:
					print time.strftime("%Y%m%dT%H%M%S  homing: at home position")
					self.stop()
					time.sleep(.5)
					self.zero()

					print time.strftime("%Y%m%dT%H%M%S  homing: motor stopped, deteriming ID")
					id_inverse = ""
					for r in range(3):
<<<<<<< HEAD
						h = hall[3-r]
=======
						h = hall[r+1]
>>>>>>> baac3f0f374328c6e5fa1d0c19031123e97a15df
						id_inverse = id_inverse + str(1 - int(h))
					self.id = int(str(id_inverse),2)
                			if(self.id != 0):
                        			self.fw = 0
                				print time.strftime("%Y%m%dT%H%M%S  homing: Filter ID") + (" %s, %s" % (id_inverse, self.id))

					diffArr=[]
					for i,c in enumerate(crossArr):
						try:
							diff = crossArr[i+1] - c
							if diff < 1500 and diff > 1300:
								diffArr.append(diff)
						except IndexError:
							break
					self.filterDelta = np.mean(diffArr)
					print time.strftime("%Y%m%dT%H%M%S  homing: filterDelta:"), self.filterDelta
					print self.status()
					self.homingState = False
					print time.strftime("%Y%m%dT%H%M%S  homing: complete")
                			return True 
				if hall == '0111':
					try:
						st = stat['currentEncoder']
						print time.strftime("%Y%m%dT%H%M%S  homing:  recording filter position"), st
						posArr = len(crossArr) - 1
						if len(crossArr) == 0 or st > crossArr[posArr] + 1000:
                                                        crossArr.append(stat['currentEncoder'])
						elif len(crossArr) > 0 and  st < crossArr[posArr] + 1000 :
							crossArr[posArr] = np.mean([st, crossArr[posArr]])
					except IndexError:
						print 'not in crossArr'
			return False

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
		self.filter.moveMotor(str(pos))

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
		stepPos = self.filter.moveToFilter(int(pos), int(self.filterDelta))
		self.desPos = stepPos
		st = self.status()
		if self.debug:	
			while  st['currentStep'] != st['desiredStep']:
				st = self.status()
				self.log(st)
				if st['desiredStep'] == None:
					return stepPos
		
		return stepPos

	def status(self):
		"""
		return current status of filter wheel
		"""
		dict = {'id':self.id,'currentStep':None, 'currentStep':None, 'desiredStep':None, 'power':None,'motor':None, 'hall':None, 'position':None, 'filterDelta':None}
		dict['power'] = self.filter.driverStatus()
		dict['currentEncoder']  = self.filter.currentEnc()
		dict['motor'] = self.filter.motorStatus()
		hall = self.filter.hallStatus()
		dict['hall'] = str(hall).zfill(4)
<<<<<<< HEAD
		dict['position'] = int(round(dict['currentEncoder'] / self.filterDelta))
=======
		dict['position'] = int(dict['currentEncoder'] / self.filterDelta)
>>>>>>> baac3f0f374328c6e5fa1d0c19031123e97a15df
		dict['desiredStep'] = self.desPos
		dict['currentStep'] = self.filter.currentPos()
		dict['filterDelta'] = self.filterDelta
		return dict

	def log(self, txt = None):
		"""
		save commands to file
		"""
		t = time.strftime("%Y%m%dT%H%M%S")
		fin = open(time.strftime("%Y%m%d.log"),'a')
		fin.write(t + ', ' + str(txt)+'\n')
		fin.close()


if __name__ == "__main__":
	f = FilterWheel()
	f.connect()
	#f.zero()
	print f.status()
	#f.moveToPosition(3)
	f.home()
	#f.moveToPosition(2)
	#for x in range(50):
	#	f.moveToPosition(random.randrange(0,5,1))
	#	time.sleep(5)
	#f.moveToPosition(0)
