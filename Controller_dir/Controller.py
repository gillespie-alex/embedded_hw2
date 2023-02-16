import constants2 as c
import helpers2 as h


class Controller():

    def __init__(self, bus_id: int, sensor_list, unique_id=None,  status=c.IDLE, time_start=0, sns_index=0, valid=False, sns_data=0.0, noise=0):
        self.bus_id = bus_id
        self.unique_id = unique_id
        self.sensor_list = sensor_list
        self.status = status
        self.time_start = time_start
        self.sns_index = sns_index
        self.valid = valid
        self.sns_data = sns_data
        self.noise = noise

    def get_id(self):

        data  = h.wrapper_read(self.bus_id, c.UNIQUE_ID1_ADDR) 
        data |= (h.wrapper_read(self.bus_id, c.UNIQUE_ID2_ADDR) << 32)

        self.unique_id = data

    def next_sensor(self):
        self.sns_index = self.sns_index+1 if self.sns_index+1 < len(self.sensor_list) else 0
    
    def check_sensor_status(self, time):
        # Return boolean value
        return self.valid and time > self.noise


    def random_noise(self):
        self.noise = h.calc_noise()


    def request_sensor_data(self):
        self.random_noise()
        sensor_data = self.sensor_list[self.sns_index].temp_readings()
        # This could be -999 indicating ERROR
        if sensor_data == -999:
            return
        else:
            self.valid = True
            self.sns_data = sensor_data

    '''
    Steps for Requesting Sensor Data:
    1. Check SENSORBUS_STATUS is low
    if low:
    2. Perform SensorBus Write specifying sensorID, sensorADDR(low byte of temp data), sensorREAD
    3. Check for SENSORBUS_STATUS to go high
    if it goes high:
    4. Check for SENSORBUS_STATUS to go low

    # Perform Read
    1. 

    '''
