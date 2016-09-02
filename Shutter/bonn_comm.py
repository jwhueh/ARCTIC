#! /usr/bin/python

import time
import serial
#import temp

class bonn(object):
	def __init__(self):
		self.ser = None
		self.serial = '/dev/ttyUSB0'
		#self.m = temp.Metrology()

	def connect(self):
                self.ser = serial.Serial(self.serial,19200)
                return

	def disconnect(self):
		self.ser.close()
		return
	
	def closeShutter(self):
		self.ser.write('cs\r')

	def openShutter(self):
		self.ser.write('os\r')

	def shutterReset(self):
		self.ser.write('rs\r')


	def coldParam(self):
		accel = 'ac 3\r'
		vel = 'vm 10000\r'
		self.ser.write(accel)
		time.sleep(2)
		self.ser.write(vel)
		time.sleep(2)
		self.shutterReset()
		time.sleep(10)
		self.ser.write('sh\r')

		return
		
	
	def shutterStatus(self):
		self.ser.write('ss\r')
		line =  self.ser.readline()
		l = line.split()	
		l = str(l[0].lstrip('c>c>'))
		#self.log(l)
		print l
		if l == 0:
			self.shutterReset()
			self.log('shutter reset')
			time.sleep(30)
		return

	def log(self, text = None):
		t = time.strftime("%Y%m%dT%H%M%S")
		fin = open(time.strftime("%Y%m%d.log"), 'a')
		te = self.m.readTemp('1C00000365971D28')
		te = None
		fin.write(t + ', ' + str(text) + ', ' + str(te) +'\n')
		fin.close()

if __name__ == "__main__":
	b = bonn()
	b.connect()
	time.sleep(2)
	b.shutterStatus()
	"""time.sleep(2)
	b.coldParam()
	time.sleep(2)
	b.closeShutter()
	for x in range(1000):
		b.openShutter()
		time.sleep(1)
		b.shutterStatus()
		time.sleep(1)
		b.closeShutter()
		time.sleep(1)
		b.shutterStatus()
		time.sleep(1)
	"""
