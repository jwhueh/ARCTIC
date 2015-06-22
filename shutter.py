#! /usr/bin/python

import time
from ctypes import *

class shutterControl(object):
    def __init__(self):
        self.shutter = CDLL("./shutter_interface.so")
        self.expTime = 1
	self.expReps = 3
        self.pin_r = 39
	self.pin_l = 40
	
	#the main == name function will be executed when running from terminal but not when imported.  it is a cleaner way of implementing command line tests

	print "opening connection"
        self.shutter.openConnection()
	time.sleep(.1)  #I tend to sleep after opening any connection becuase it may have some time dependent routines it needs feedback from


	print "exercising low level commands"
	self.shutter.moveShutter(self.pin_l,0)
	time.sleep(.1)
	self.shutter.moveShutter(self.pin_r,0)
	time.sleep(.1)
	self.shutter.moveShutter(self.pin_l,1)
	time.sleep(.1)
        self.shutter.moveShutter(self.pin_r,1)
	time.sleep(.1)	
	self.shutter.moveShutter(self.pin_l,0)
        time.sleep(.1)
        self.shutter.moveShutter(self.pin_r,0)
        time.sleep(.1)



	self.home = True
	#self.shut_r = 39
	#self.shut_l = 40
        print "testing build"

        time.sleep(1)
        #self.sendHome()
        time.sleep(0.5)
        self.takeImages()
	self.close()
        
    def sendHome(self):
	""" Moves shutter to forward home position
	Args:
		None
	Returns:
		True if task completed
	"""

        #self.shutter.moveShutter(self.pin_l,0)
        time.sleep(0.5)
        #self.shutter.moveShutter(self.pin_r,0)
        self.home = True
        return

    def checkStatus(self):
	""" Checks the positional status of the shutter blades
	Args:
		None
	Returns:
		True if on track 1, False if on track 2.
	"""

	if self.home == True:
		print 'at forward home position'
		return True
	elif self.home == False:
		print 'at reverse home position'
		return False
	else:
		RaiseException

    def takeImages(self):
	for i in range(self.expReps):
	    self.expose()
	    time.sleep(0.5)
	    print i
	return

    def expose(self):
	if self.home == True:
	    self.toPosRight(self.pin_r)
	    time.sleep(self.expTime)
            self.toPosRight(self.pin_l)
	    self.home = False        
	else:
            self.toPosLeft(self.pin_l)
	    time.sleep(self.expTime)
	    self.toPosLeft(self.pin_r)
	    self.home = True
	return

    def toPosRight(self,shutter):
	#self.shutter.moveShutter(shutter,1)
        return
    
    def toPosLeft(self,shutter):
	#self.shutter.moveShutter(shutter,0)
	time.sleep(0.5)
	return

    def close(self):
        print "sample"
        #self.shutter.closeConnection(1,2)
        print "\nend sample"
        return

if __name__ == "__main__":
	s=shutterControl()
