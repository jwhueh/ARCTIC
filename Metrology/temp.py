#! /usr/bin/python

import serial
import time

class Metrology(object):
	def __init__(self):
		pass
		self.ser = None
		self.serial = '/dev/ttyS0'
		self.temp1 = '1C00000365971D28'
		self.delay = 0.2


	def start(self):
		self.ser = serial.Serial(self.serial,9600, timeout=.1)
		return

	def readTemp(self, dev):
		self.deviceSelect(dev)
		self.serWrite('M')
		self.serWrite('W0144')
		time.sleep(3)
		self.deviceSelect(dev)
		output = self.serWrite('W0ABEFFFFFFFFFFFFFFFFFF')
		self.convert(output)	
		return

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
		out = self.ser.readline()
		print out
		return out

	def convert(self, sig):
		print sig
		print sig[2:4], sig[4:6], sig[14:16], sig[16:18] 
		lsb = int("0x%s"  % sig[2:4],0)
		msb = int("0x%s" % sig[4:6],0)
		rem = int("0x%s" % sig[14:16],0)
		count = int("0x%s" % sig[16:18],0) 
		print lsb, msb, rem, count
		temp = (lsb - 0.25 + ((count - rem)/count))/2 
		print temp

if __name__ == "__main__":
	m = Metrology()
	m.start()
	m.readTemp('1C00000365971D28')
