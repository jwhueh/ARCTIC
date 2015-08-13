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

from multiprocessing import Process
import time
from time import gmtime, strftime
from ctypes import *
import thread
import ctypes

class shutterControl(object):
    def __init__(self):
	"""
	pin_l refers to the pin controlling the left shutter, pin_r the right
	when the airhoses are located to the right of the apparatus	
	"""
        
	self.shutter = CDLL("./shutter_interface.so")
	self.waiting = CDLL("./shutter_watch.so")
	self.waiting.loop.restype = ctypes.c_char_p
        self.pin_r = 76
	self.pin_l = 77
	self.delay = 0.5
	self.home = None
	self.open = None
	self.right = None	# directional variable, next motion is right when true
	self.running = True
	print "opening connection"
        self.shutter.openConnection()
	time.sleep(.1)  #I tend to sleep after opening any connection because it may have some time dependent routines it needs feedback from
	#self.shutter.moveShutter(61,1)  #needed for initialization of PC104

    def end(self):
	while True:
	    exit = raw_input("Exit?")
	    print exit
	    if not exit:
		self.waiting.stopLoop()
	        self.running = False
		break

    def exerciseRoutine(self):
	print "Just exercising.\n"
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
		print 'Closed at home.\n'
		self.home = True
		self.open = False
		self.right = True
	    else:
		print 'Closed.\n'
		self.home = False
		self.open = False
		self.right = False
	else: 
	    print 'Exposing.\n'
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
	try:
	    while self.running == True:
		#v = ctypes.create_string_buffer(self.waiting.loop())
		v = self.waiting.loop()
		print v
	        if self.home == True:
		    self.toPosRight(self.pin_r)
		    self.waiting.loop()
		    self.toPosRight(self.pin_l)
		else:
		    self.toPosLeft(self.pin_l)
		    self.waiting.loop()
		    self.toPosLeft(self.pin_r)
		self.checkStatus()
	except KeyboardInterrupt:
		pass
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

    def close(self):
        print "sample"
        self.shutter.closeConnection(1,2)
        print "\nend sample"
        return

if __name__ == "__main__":
	s=shutterControl()
	s.hallArrayMake()
	s.sendHome()
	s.exerciseRoutine()
	s.changeSense()
	#s.sendHome()
