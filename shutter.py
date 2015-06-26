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
from time import gmtime, strftime
from ctypes import *

class shutterControl(object):
    def __init__(self):
	"""
	pin_l refers to the pin controlling the left shutter, pin_r the right
	when the airhoses are located to the right of the apparatus	
	"""
        
	self.shutter = CDLL("./shutter_interface.so")
	self.waiting = CDLL("./shutter_watch.so")
        self.pin_r = 76
	self.pin_l = 77
	self.delay = 0.5
	current_time = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
        self.logfile = open("/root/ARCTIC/"+current_time+"logfile.txt", 'w')	
	self.home = None
	self.open = None
	self.right = None	# directional variable, next motion is right when true
	self.running = True
	print "opening connection"
        self.shutter.openConnection()
	time.sleep(.1)  #I tend to sleep after opening any connection because it may have some time dependent routines it needs feedback from
	#self.shutter.moveShutter(61,1)  #needed for initialization of PC104
	print "exercising low level commands"
	print "this should really be moved to a higher level test if we want one."

        print "testing build"

    def exerciseRoutine(self):
	self.shutter.moveShutter(self.pin_l,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,1)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_l,1)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_l,0)
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,0)
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
        time.sleep(self.delay)
        self.shutter.moveShutter(self.pin_r,0)
        self.checkStatus()
	return

    def checkStatus(self):
	""" Checks the positional status of the shutter blades
	Args:
		None
	Returns:
		True if on track 1, False if on track 2.
	"""
	time.sleep(self.delay)
	hallArray = self.hallArrayMake()
	if hallArray[3][1] == hallArray[4][1]:
	    if hallArray[3][1] == 0:
		print 'at forward home position'
		self.home = True
		self.open = False
		self.right = True
	    else:
		print 'at reverse home position'
		self.home = False
		self.open = False
		self.right = False
	else: 
	    print 'open'
	    self.home = False
	    self.open = True
	return

    def changeSense(self):
	'''
	calls shutter_watch methods to observe for changes in pin values, returns value pins changed to, initiates opening and closing of the shutters depending on position and pin value, does nothing if already in requested state
	currently, after any motion will ask user if they want to continue
	Args:
		None
	Returns:
		None
	'''
	start_time = 0;
        end_time = 0;

	while self.running == True:
	    print "heading to loop"
	    #signal_value = int(self.waiting.loop(c_int(33)))
	    #print signal_value
	    signal_value = self.waiting.loop()
	    if signal_value == 1:
	        if self.home == True and self.right == True and self.open == False:
		    print 'got signal to open from home'
	            self.toPosRight(self.pin_r)
		    start_time = float(self.waiting.timing(c_int(26)))
		    self.checkStatus()
		elif self.home == False and self.right == False and self.open == False:
		    print 'got signal to open from reverse home'
		    self.toPosLeft(self.pin_l)
		    start_time = float(self.waiting.timing(c_int(30)))
		    self.checkStatus()
	    else:
		if self.right == True and self.home == False and self.open == True:
		    print 'got signal to close moving right'
		    self.toPosRight(self.pin_l)
	            end_time = float(self.waiting.timing(c_int(31)))
		    self.checkStatus()
		    self.printLog(start_time,end_time)
		elif self.right == False and self.home == False and self.open == True:
		    print 'got signal to close moving left'
	            self.toPosLeft(self.pin_r)
		    end_time = float(self.waiting.timing(c_int(27)))
		    self.checkStatus()
		    self.printLog(start_time,end_time)
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

    def hallArrayMake(self):
	hallArray = []
	for i in range(25,33):
	    value = int(self.waiting.getVal(c_int(i)))
	    pair = [i,value]
	    hallArray.append(pair)
	return hallArray

    def printLog(self, start_time, end_time):	
	expTime = float(end_time-start_time)
	hallArray = self.hallArrayMake()
	for pin in hallArray:
	    self.logfile.write("%s:%s"%(pin[0],pin[1]))
	self.logfile.write("%s\n" %expTime)
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
	s.hallArrayMake()
	s.sendHome()
	s.exerciseRoutine()
	s.changeSense()
	file.close()
	#s.sendHome()
