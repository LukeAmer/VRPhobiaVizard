import sys
import threading
import time
import vizact
sys.path.append('D:\pyserial-3.2.1') # Find external dependency within the D drive including 'serial' 
	
import serial
from time import sleep
import viz

connected = False

try: # Instead of causing errors if the Arduino is not connected, the try function avoids this and simply returns a debug message
    ser = serial.Serial("COM3")
    ser.baudrate = 115200
    connected = True
    print "Arduino connected!"
except serial.serialutil.SerialException:
    print "Arduino not connected!"

global exitFlag 
exitFlag = 0

global heartRate
heartRate = 10

class hrThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        print "Starting"
        updateHeartRate(self.name, self.counter, 1000)
        print "Exiting"

def updateHeartRate(threadName, delay, counter):
    while not viz.done():
        time.sleep(delay)
        heartRate = 0
        global connected
        if connected:
            heartRate = int(ser.readline())
            
        SetHeartRate(heartRate)
        counter -= 1

def SetHeartRate(hr):
	global heartRate
	heartRate = hr
	#print hr


# Create new threads
threadHeartRate = hrThread(1, "Thread-1", 0.05)

# Start new Threads
threadHeartRate.start()

