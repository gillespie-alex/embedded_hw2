import sys
import time

import constants1
import helpers1

sys.path.insert(0, '/home/alex/Desktop/embedded_hw2/Sensor_dir')
sys.path.insert(0, '/home/alex/Desktop/embedded_hw2/Controller_dir')
from Sensor import TempSensor
from Controller import Controller


class CPU():

    Factory_Sensors_LUT     = []
    Factory_Controllers_LUT = []
    generator_index = 0
    inspector_index = 0

    def __init__(self):
        pass

    @classmethod
    def initialize(cls):
        for c in range(constants1.NUM_CONTROLLERS):
            # Get all sensor ID's
            sensors = []
            for s in range(constants1.NUM_SENSORS):
                # Initialize sensor object
                temp_sensor = TempSensor(master=c, bus_id=s)
                temp_sensor.get_id()
                sensors.append(temp_sensor)

            cls.Factory_Sensors_LUT.append(sensors)
            # Initialize Controller object
            temp_ctlr = Controller(bus_id=c, sensor_list=sensors)
            temp_ctlr.get_id()
            cls.Factory_Controllers_LUT.append(temp_ctlr)
        #for i, C in enumerate(cls.Factory_Controllers_LUT):
         #   print(f"Controller {i} id: {C.unique_id}")
          #  for j, S in enumerate(C.sensor_list):
           #     print(f"\tSensor {S.bus_id} id: {S.unique_id}")


    @classmethod
    def poll(cls):
        for _ in range(35):
            cls.generator_index = helpers1.generator(cls.generator_index, cls.Factory_Controllers_LUT)
            cls.inspector_index, output = helpers1.inspector(cls.inspector_index, cls.Factory_Controllers_LUT)
            print('\n')
            helpers1.console_output(output)

CPU.initialize()
CPU.poll()
#time.sleep(0.1)
