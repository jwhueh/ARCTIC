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
        
	self.waiting = CDLL("./shutter_watch.so")
	self.expTime = 0.1
        self.pin_r = 39
	self.pin_l = 40
	self.delay = 1
	self.check = 33
	self.running = None  # once set, 1 corresponds to True, 0 to False
	print "opening connection"
    
    def changeSense(self):
	print "starting changeSense\n"
	self.waiting.loop()	
	print "ending changeSense\n"
	return

if __name__ == "__main__":
	s=shutterControl()
	s.changeSense()
