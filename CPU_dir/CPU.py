import sys

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


    # Initializes all Controller and Sensor ID's and writes to inventory file
    @classmethod
    def initialize(cls):
        for c in range(constants1.NUM_CONTROLLERS):

            sensors = []
            for s in range(constants1.NUM_SENSORS):

                temp_sensor = TempSensor(master=c, bus_id=s)
                temp_sensor.get_id()
                sensors.append(temp_sensor)

            cls.Factory_Sensors_LUT.append(sensors)

            temp_ctlr = Controller(bus_id=c, sensor_list=sensors)
            temp_ctlr.get_id()

            cls.Factory_Controllers_LUT.append(temp_ctlr)

        helpers1.file_write_inventory(cls.Factory_Controllers_LUT, cls.Factory_Sensors_LUT)


    # Continuously polls sensor data and writes to file for as long as program runs
    @classmethod
    def poll(cls):
        while(True):
            cls.generator_index = helpers1.generator(cls.generator_index, cls.Factory_Controllers_LUT)
            cls.inspector_index, output = helpers1.inspector(cls.inspector_index, cls.Factory_Controllers_LUT)
            helpers1.file_write_logs(output)

