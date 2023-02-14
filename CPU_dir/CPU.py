import random
##
import constants1

import sys


sys.path.insert(0, '/home/alex/Desktop/embedded_hw2/Sensor_dir')
print("about to print path")
print(sys.path)
from Sensor import TempSensor


#from sensor import TempSensor
#from controller import Controller
#import tokenizer.helpers as h
#import CPU_dir.constants as c
#import .constants


class CPU():

    Factory_LUT = []

    def __init__(self):
        pass

    def p(self):
        #print(self.Factory_LUT)
        print(CPU.Factory_LUT)

    @classmethod
    def initialize(cls):
        for c in range(constants1.NUM_CONTROLLERS):
            # Get all sensor ID's
            sensors = []
            for s in range(constants1.NUM_SENSORS):
                # Initialize sensor object
                temp = TempSensor(master=c, bus_id=s)
                temp.get_id()
                sensors.append(temp)

            CPU.Factory_LUT.append(sensors)
        #print(CPU.Factory_LUT)
        for stuff in CPU.Factory_LUT:
            print(stuff)
            for thingy in stuff:
                print(thingy.unique_id)

CPU.initialize()
#CPU.poll()

def magical_function():
    # random stuff
    return random.randint(0, 255)

