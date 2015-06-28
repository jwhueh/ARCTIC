#! /usr/bin/python

import serial
import time

Class Metrology(object):
	def __init__(self):
		pass
		self.ser = None
		self.serial = '/dev/ttyS0'
		self.temp1 = '1C00000365971D28'
		self.delay = 0.2


	def start(self, serial):
		self.ser = serial.Serial(serial,,9600, timeout=.1)
		return

	def readTemp(self, dev):
		self.deviceSelect(dev)
		self.serWrite('M')
		self.serWrite('W0144')
		time.sleep(3)
		output = self.serWrite('W0ABEFFFFFFFFFFFFFFFFFF')
		



	def deviceSelect(self, dev):
		cmd = 'A%s\r' % str(dev)
		self.ser.write(cmd)
		time.sleep(self.delay)
		self.ser.readline()
		return

	def serWrite(self, text1 = None, text2 = None):
		if text2 == None:
			cmd = '%s\r' % text1
		self.ser.write(cmd)
		time.sleep(self.delay)
		out = self.readline()
		print out
		return out

if __name__ == "__main__":
	m = Metrology()
	m.startup()
	m.readTemp()
