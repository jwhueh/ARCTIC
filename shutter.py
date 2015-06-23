#! /usr/bin/python

"""
shutter.py

This program connects to the pc104 shutter_interface c file and does the high level commanding and computation of the shutter
"""

__author__ = ["Caitlin Doughty", "Joseph Huehnerhoff"]
__copyright__ = "NA"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "NA"
__email__ = "NA"
__status__ = "Development"

import time
from ctypes import *

class shutterControl(object):
    def __init__(self):
	"""
	shutter solenoids defined as pin 39, and 40 on the PC104
	pin_l refers to the pin controlling the left shutter, pin_r the right
	when the airhoses are located to the right of the apparatus	
	"""
        
	self.shutter = CDLL("./shutter_interface.so")
	self.waiting = CDLL("./shutter_watch.so")
	self.expTime = 0.1
        self.pin_r = 76
	self.pin_l = 77
	self.delay = 1
	self.home = True
	self.open = False
	self.right = True	# directional variable, next motion is right when true
	self.running = True
	print "opening connection"
        self.shutter.openConnection()
	time.sleep(.1)  #I tend to sleep after opening any connection because it may have some time dependent routines it needs feedback from
	#self.shutter.moveShutter(61,1)  #needed for initialization of PC104
	print "exercising low level commands"
	print "this should really be moved to a higher level test if we want one."

        print "testing build"

    def exerciseRoutine(self):
	self.shutter.moveShutter(self.pin_r,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_l,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_l,1)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,1)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_l,0)
        time.sleep(self.delay)
	return

    def sendHome(self):
	""" Moves shutter to forward home position
	Args:
		None
	Returns:
		True if task completed
	"""

        self.shutter.moveShutter(self.pin_l,0)
        time.sleep(0.5)
        self.shutter.moveShutter(self.pin_r,0)
        self.home = True
	self.open = False
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
    
    def changeSense(self):
	while self.running == True:
	    print "heading to loop"
	    self.waiting.loop()
	    if self.right == True:
		if self.home == True:
		    #self.toPosRight(pin_r)
		    self.home = False
		    self.open = True 
		    print "now open and direction is right"
		else:
		    #self.toPosRight(pin_l)
		    self.open = False
		    self.right = False
		    print "now closed in reverse home and direction is left"
	    else:
		if self.open == True:
		    #self.toPosLeft(pin_r)
		    self.open = False
		    self.home = True
		    self.right = True
		    print "now closed in home and direction is right"
		else:
		    #self.toPosLeft(pin_l)
		    self.open = True
		    self.home = False
		    print "now open and direction is left"
	    continuing = self.userInput()
	    if continuing == "n":
		self.running = False   
	return

    def toPosRight(self,shutter):
	self.shutter.moveShutter(shutter,1)
        return
    
    def toPosLeft(self,shutter):
	self.shutter.moveShutter(shutter,0)
	return

    def close(self):
        print "sample"
        self.shutter.closeConnection(1,2)
        print "\nend sample"
        return

    def userInput(self):
	continuing = raw_input("Continue? y or n\n")
	return continuing

if __name__ == "__main__":
	s=shutterControl()
	#s.sendHome()
	#s.exerciseRoutine()
	s.changeSense()
	#s.sendHome()
