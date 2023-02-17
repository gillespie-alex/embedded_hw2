import helpers3 as h
import constants3 as c
import given_methods

# Lambda function to shift the sensor_id bits
shift = lambda x, byte : x << (byte*8) 


# Parent Class
class Sensor():

    # Class Attributes
    factory_class_id_addr = [0x20, 0x21, 0x22, 0x24]

    def __init__(self, master: int, bus_id: int, unique_id=0):
        self._master = master
        self._bus_id = bus_id
        self._unique_id = unique_id


    # Reads from 4 Sensor UNIQUE_ID addresses to get unique_id
    def get_id(self):
        data = 0
        for byte in range(4):
            id_bits = h.wrapper_read(self.master, self.bus_id, Sensor.factory_class_id_addr[byte])
            data |= shift(id_bits, byte)
        self._unique_id = data


    # Getters to read the protected members
    @property
    def unique_id(self):
        return self._unique_id

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def master(self):
        return self._master


    # Retrieves data from specified SENSORBUS_BUSID and SENSORBUS_ADDR
    def request_data(self, controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR):
        data = h.wrapper_read(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR)
        return data


# Child Class
class TempSensor(Sensor):

    # Class Attributes
    Factory_temp_addr = [0x45, 0x46]

    def __init__(self, master: int, bus_id: int, unique_id=0, temp_data=0.0):

        super().__init__(
                master, bus_id, unique_id
                )


    # Reads both the high and low byte of temp data and will only return if both are valid
    # If one of the data bytes was invalid, the entire operation is invalid, return ERROR
    def temp_readings(self):
        low_byte_temp = self.request_data(self.master, self.bus_id, TempSensor.Factory_temp_addr[0])
        high_byte_temp = self.request_data(self.master, self.bus_id, TempSensor.Factory_temp_addr[1])
        
        if low_byte_temp == c.ERROR or high_byte_temp == c.ERROR:
            return c.ERROR
        
        raw_temp_data = low_byte_temp | (high_byte_temp << 8)
        self.temp_data = given_methods.Linear_Function(raw_temp_data)
        
        return self.temp_data

