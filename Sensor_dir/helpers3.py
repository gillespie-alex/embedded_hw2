import random

import given_methods
import constants3 as c


# Check SENSORBUS_STATUS
def wrapper_sensorbus_status_read(mimic_value, controller_id):
    if mimic_value == 0x00:
        status = given_methods.Read0(controller_id, c.FASTBUS_SENSOR_STATUS)
    elif mimic_value == 0x01:
        status = given_methods.Read1(controller_id, c.FASTBUS_SENSOR_STATUS)
    status &= 0x01
    return status

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

def check_wrapper_read():
    pass

# Controller Read (magical read function)
def wrapper_read(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int) -> int:
    # Normally should make sure that SENSORBUS_STATUS is not busy, but will assume so on startup
    status = wrapper_sensorbus_status_read(0, controller_id)
    if status == 0x01:
        # Meaning ERROR
        return -999

    # SENSORBUS_DATA set to 0 as we're not really writing data there
    wrapper_write(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR, 0x0, c.READ)

    while True:
        val = wrapper_sensorbus_status_read(1, controller_id)
        val &= 0x01
        if val == 0x01:
            break

    while True:
        val = wrapper_sensorbus_status_read(0, controller_id)
        val &= 0x01
        if val == 0x00:
            # Register is now ready to be read from
            break

    # NEED TO CHECK STATUS STUFF AGAIN
    # Now the sensor is no longer busy and we can read from SENSORBUS_DATA
    data = given_methods.Read(controller_id, c.FASTBUS_BASE_ADDR)

    # Return an 8-bit data value
    return ((data & 0x00FF0000) >> 16)



