import sys
import threading
import time
sys.path.append('D:\pyserial-3.2.1')
	
import serial
from time import sleep
import viz
ser = serial.Serial('COM3') #check device manager for
#the port number for arduino
ser.baudrate = 115200 #use the same baudrate as

viz.addChild('sky_day.osgb')

#the sender
viz.go()

global exitFlag 
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        

    def run(self):
        print "Starting"
        updateDistance(self.name, self.counter, 1000)
        print "Exiting"

heartRate = 0

def updateDistance(threadName, delay, counter):
    while not viz.done():
        time.sleep(delay)
        heartRate = ser.readline()
        print heartRate
        counter -= 1

#while not viz.done():
#	print int(ser.readline())
#	ser.flush()
#	sleep(0.1) #don’t read TOO frequently
#	viz.frame()

def bye():
    exitFlag = 1

vizact.onexit(bye)

# Create new threads
threadTreadmill = myThread(1, "Thread-1", 0.05)

# Start new Threads
threadTreadmill.start()

	

