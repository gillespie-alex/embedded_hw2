# Import
import helpers3 as h

# Lambda function to shift the bits
shift = lambda x, byte : x << (byte*8) 


# Parent Class
class Sensor():

    # Class Attributes
    factory_class_id_addr = [0x20, 0x21, 0x22, 0x24]

    def __init__(self, master: int, bus_id: int, unique_id=0, status=0):
        self.master = master
        self.bus_id = bus_id
        self.unique_id = unique_id
        self.status = status

    def get_id(self):
        data = 0
        for byte in range(4):
            id_bits = h.wrapper_read(self.master, self.bus_id, Sensor.factory_class_id_addr[byte])
            data |= shift(id_bits, byte)
        self.unique_id = data

    def request_data(self, controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR):
        data = h.wrapper_read(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR)
        return data


# Child Class
class TempSensor(Sensor):

    # Class Attributes
    Factory_temp_addr = [0x45, 0x46]

    def __init__(self, master: int, bus_id: int, unique_id=0, status=0, temp_data=0.0):
        # Now have access to all of parent's attributes
        super().__init__(
                master, bus_id, unique_id, status
                )
        #self.temp_data = temp_data
        #self.high_low_byte = high_low_byte

    def temp_readings(self):
        low_byte_temp = self.request_data(self.master, self.bus_id, cls.Factory_temp_addr[0])
        high_byte_temp = self.request_data(self.master, self.bus_id, cls.Factory_temp_addr[1])
        if low_byte_temp == -999 or high_byte_temp == -999:
            return -999
        raw_temp_data = low_byte_temp | (high_byte_temp << 8)
        self.temp_data = given_methods.Linear_Function(raw_temp_data)
        # This value is basically just a placeholder
        return self.temp_data

