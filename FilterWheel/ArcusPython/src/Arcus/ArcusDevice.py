"""
Arcus controller python interface.
Only works if one ARCUS device is connected. 
Including Arcus Configuration cables.
Open ArcusDevice.py in Python IDE --> Run --> Enter Terminal Commands
"""
import threading
import Arcus
import copy
import sys

class ArcusDevice(object):
    """
    This is interface class to Arcus stepper controller
    @author Lukas Zubal
    @version 1.0
    """
    def __init__(self):
        """
        @brief Constructor
        @param self object instance
        """
        self.device = Arcus.Arcus()
        if self.device.Connect() == 1:
            print ' '
        else:
            print "Cannot open stepper device on port "
            sys.exit()
        self.outputBuffer = "                                                                "
        self.lock = threading.Lock()  # thread safety
        self.verbose = 0

    def close(self):
        """
        @brief Closes Arcus device connection
        @param self object instance
        @return bool Returns a 1 if successful
        """
        self.lock.acquire()
        self.device.Close()
        self.lock.release()
        del self.device
        return 1

    def write(self, data):
        """
        @brief Command-response call to Arcus device
        @see Arcus controller manual for complete list of interactive commands
        @param self object instance
        @param data string containing interactive commands to arcus
        @return str Returns string containing response of controller
        """
        self.lock.acquire()
        self.device.SendAndRecive(data, self.outputBuffer)
        resp = copy.deepcopy(self.outputBuffer[:])
        self.lock.release()
        resp = resp.split('\x00')[0]
        if self.verbose == 1:
            print resp
        return resp

if __name__ == '__main__':

    arc = ArcusDevice()

    response = arc.write('DN')  # Send Terminal Command to return device name.
    print ("Connected to device: " + response) # Notify user

    print "Input ASCII command here or type 'end' to exit: "    # User Directions

    command = "" # This gets a command from the user.
    while command != "end":  # Loop until the user is done.
        command = raw_input("")
        response = arc.write(command)   # Process Command and save Controller Response
        print "Response: " + response   # Print Controller Response to User

    arc.close() # Close Device.
    del arc