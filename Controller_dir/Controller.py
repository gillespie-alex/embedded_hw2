import random

import constants2 as c
import helpers2 as h


class Controller():
    def __init__(self, unique_id=None, sensor_list = [None], status=c.IDLE, time_start=0, sns_index=0, valid=True):
        self.unique_id = unique_id
        self.sensor_list = sensor_list
        self.status = status
        self.time_start = time_start
        self.sns_index = sns_index
        self.valid = valid

    def get_id(self):
        self.unique_id = random.randint(0,10000000)

    def next_sensor(self):
        self.sns_index += 1 if self.sns_index+1 < len(self.sensor_list) else 0

    def printme(self):
        print("hello crom controller module")
    
    def check_sensor_status(self):
        pass
