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


    # Will Read the unique 32 bit UNIQUE_IDs in controller address space and set id
    def get_id(self):

        data  = h.wrapper_read(self.bus_id, c.UNIQUE_ID1_ADDR) 
        data |= (h.wrapper_read(self.bus_id, c.UNIQUE_ID2_ADDR) << 32)

        self.unique_id = data


    # Will increment the next sensor to request data from on Controller
    def next_sensor(self):
        self.sns_index = self.sns_index+1 if self.sns_index+1 < len(self.sensor_list) else 0
    
    
    # Checks if valid data exists from sensor, and if enough time has passed for sensor
    def check_sensor_status(self, time):
        return self.valid and time > self.noise


    # Adds random noise to each new sensor reading
    def random_noise(self):
        self.noise = h.calc_noise()


    # First, creates random noise for the sensor
    # Will request data from a specific sensor and check if data is valid
    # If data is valid, change Controller's valid flag (indicating Controller has new data)
    def request_sensor_data(self):
        self.random_noise()

        sensor_data = self.sensor_list[self.sns_index].temp_readings()

        if sensor_data == -999:
            return
        else:
            self.valid = True
            self.sns_data = sensor_data

