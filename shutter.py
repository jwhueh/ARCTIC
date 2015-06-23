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
        self.pin_r = 77
	self.pin_l = 76
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
	'''
	calls shutter_watch methods to observe for changes in pin values, returns value pins changed to, initiates opening and closing of the shutters depending on position and pin value, does nothing if already in requested state
	currently, after any motion will ask user if they want to continue
	Args:
		None
	Returns:
		None
	'''

	while self.running == True:
	    print "heading to loop"
	    signal_value = self.waiting.loop()
	    if signal_value == 1:
		if self.open != True:
		    if self.home == True:
			self.toPosRight(self.pin_r)
			self.right = True
			self.home = False
			self.open = True
			print "opening by moving right shutter to the right"
		    else:
			self.toPosLeft(self.pin_l)
			self.right = False
			self.home = False
			self.open = True
			print "opening by moving left shutter to the left"
	    else:
		if self.open == True:
		    if self.right == True:
			self.toPosRight(self.pin_l)
			self.right = False
			self.home = False
			self.open = False
			print "closing by moving left shutter to the right"
		    else:
			self.toPosLeft(self.pin_r)
			self.right = True
			self.home = True
			self.open = False
			print "closing by moving right shutter to the left"
	    #continuing = self.userInput()
	    '''if continuing == "n":
		self.running = False'''   
	return


    def toPosRight(self,shutter):
	'''
	moves a single shutter to the reverse home position
	Args:
		shutter pin identifier
	Returns:
		None
	'''

	self.shutter.moveShutter(shutter,1)
        return
    

    def toPosLeft(self,shutter):
	'''
	moves a single shutter to the home position
	Args:
                shutter pin identifier
        Returns:
                None
        '''

	self.shutter.moveShutter(shutter,0)
	return


    def close(self):
        print "sample"
        self.shutter.closeConnection(1,2)
        print "\nend sample"
        return


    def userInput(self):
	continuing = raw_input("Continue? y or n\n")
	print "\n"
	return continuing

if __name__ == "__main__":
	s=shutterControl()
	s.sendHome()
	#s.exerciseRoutine()
	s.changeSense()
	s.sendHome()
