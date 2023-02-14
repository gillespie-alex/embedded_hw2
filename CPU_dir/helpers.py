import sys

import helpers
import constants as c

sys.path.insert(0, '/home/alex/Desktop/embedded_hw2/Sensor')
print("about to print path")
print(sys.path)
from Sensor import TempSensor

#def initialize(cls):
#    for c in range(c.NUM_CONTROLLERS):
#        # Get all sensor ID's
#        sensors = []
#        for s in range(c.NUM_SENSORS):
#            data = 0
#            # Initialize sensor object
#            temp = TempSensor(master=c, bus_id=s)
#            temp.get_id()
#            sensors.append(temp)
#
#        CPU.Factory_LUT.append(sensors)
#


''' checkpoint '''
def find_ids():
    res = []
    for c in range(c.NUM_CONTROLLERS):
        sensors = []
        for s in range(c.NUM_SENSORS):
            data = 0
            # Initialize sensor object
            temp = TempSensor(master=c, bus_id=s)
            temp.get_id()
            sensors.append(temp)

        CPU.Factory_LUT.append(sensors)


