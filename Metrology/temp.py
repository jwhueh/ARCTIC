#! /usr/bin/python

import serial
import time

"""Make it so that the temp sensors are read from file but at the same time the file can be updated with routine"""

class Metrology(object):
	def __init__(self):
		self.ser = None
		self.serial = '/dev/ttyS0'
		self.sensors=[]
		self.delay = .5
		self.start()
		self.findTempSensors()
		self.setupSensors()

	def run(self):
		while True:
			fout = open(time.strftime("%Y%m%d.temp"),'a')
			output=time.strftime("%Y%m%dT%H%M%S")
			for s in self.sensors:
				output = output+','	
				temp = self.readTemp(s)
				output = output+str(temp)
			fout.write(output+'\n')
			fout.close()
			
			time.sleep(10)	


	def setupSensors(self):
		for s in self.sensors:
			self.setResolution(s)
			self.readTemp(s)
		return
			

	def findTempSensors(self):
		self.sensors.append(self.serWrite('S\r').rstrip('\r'))
		time.sleep(5)
		while True:
			out = self.serWrite('s\r')
			if len(out) <=3:
                                break
			self.sensors.append(out.rstrip('\r'))
		print self.sensors
		return


	def setResolution(self,dev):
		self.deviceSelect(dev)
		self.serWrite('W044E4B467F')
		self.serWrite('R')

	def start(self):
		self.ser = serial.Serial(self.serial,9600, timeout=.5)
		return

	def readTemp(self, dev):
		self.deviceSelect(dev)
		self.serWrite('M')
		self.serWrite('W0144')
		time.sleep(1)
		self.serWrite('M')
		output = self.serWrite('W0ABEFFFFFFFFFFFFFFFFFF')
		print output
		t = self.convert(output)	
		return t

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
		return out

	def convert(self, sig):
		lsb = sig[2:4]
		msb = sig[4:6]
		lm = msb+lsb
		neg = sig[4:5]
		count_remain = sig[14:16]
		count_c = sig[16:18]
		print lsb, msb, neg, count_remain, count_c
		#make into binary
		binary = bin(int(lm, 16))[2:].zfill(16)
		
		if neg == 'F':
			print binary
			outbin = ""
			for b in binary:
				if b == '1':
					outbin = outbin + '0'
				else:
					outbin = outbin + '1'

			outhex = (int(outbin, 2))
			print outhex
			temp = -int('%s' % outhex,0)/16. 
			return temp

			
		else:
			print lm
			temp = int('0x%s' % str(lm),0)/16.
			return temp	
		return 

if __name__ == "__main__":
	m = Metrology()
	#m.setResolution('1C00000365971D28')
	#time.sleep(2)
	#print m.readTemp('1C00000365971D28')
	m.run()
