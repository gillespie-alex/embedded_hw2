import random

import given_methods
import constants as c


# Controller Write
def wrapper_write(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int, SENSORBUS_DATA: int, SENSORBUS_OP: int) -> None:

    # Creating the 32-bit 'data'
    SENSORBUS_BUSID = c.SBUS_ID(SENSORBUS_BUSID)
    SENSORBUS_ADDR  = c.SBUS_ADDR(SENSORBUS_ADDR)
    SENSORBUS_DATA  = c.SBUS_DATA(SENSORBUS_DATA)
    SENSORBUS_OP    = c.SBUS_OP(SENSORBUS_OP)

    data = SENSORBUS_BUSID |  SENSORBUS_ADDR |  SENSORBUS_DATA  | SENSORBUS_OP    

    # Write this to Controller memory
    given_methods.Write(controller_id, c.FASTBUS_BASE_ADDR, data) 

# Controller Read (magical read function)
def wrapper_read(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int) -> int:
    # Normally should make sure that SENSORBUS_STATUS is not busy, but will assume so on startup

    # SENSORBUS_DATA set to 0 as we're not really writing data there
    wrapper_write(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR, 0x0, c.READ)

    while True:
        val = given_methods.Read(controller_id, c.FASTBUS_SENSOR_STATUS)
        val &= 0x1
        if not val:
            # No longer busy
            break

    # Now the sensor is no longer busy and we can read from SENSORBUS_DATA
    data = random.randint(0, 4_294_967_295)#given_methods.Read(controller_id, c.FASTBUS_BASE_ADDR)
    # Return an 8-bit data value
    return ((data & 0x00FF0000) >> 16)



