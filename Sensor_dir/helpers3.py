import time

import given_methods
import constants3 as c


# Check SENSORBUS_STATUS[0]
def wrapper_sensorbus_status_read(mimic_value, controller_id):

    if mimic_value == 0x00:
        status = given_methods.Read0(controller_id, c.FASTBUS_SENSOR_STATUS)

    elif mimic_value == 0x01:
        status = given_methods.Read1(controller_id, c.FASTBUS_SENSOR_STATUS)

    status &= 0x01
    return status


# Creating the 32-bit 'data'
def create_word(SENSORBUS_BUSID: int, SENSORBUS_ADDR: int, SENSORBUS_DATA: int, SENSORBUS_OP: int):

    SENSORBUS_BUSID = c.SBUS_ID(SENSORBUS_BUSID)
    SENSORBUS_ADDR  = c.SBUS_ADDR(SENSORBUS_ADDR)
    SENSORBUS_DATA  = c.SBUS_DATA(SENSORBUS_DATA)
    SENSORBUS_OP    = c.SBUS_OP(SENSORBUS_OP)

    data = SENSORBUS_BUSID |  SENSORBUS_ADDR |  SENSORBUS_DATA  | SENSORBUS_OP    

    return data


def get_time():
    t = time.perf_counter() * 1_000_000
    return int(t)


# Checks toggling of SENSORBUS_STATUS register within reasonable amount of time
def check_sbus_status(desired_status, controller_id):
    start_check_t = get_time()

    while get_time() - start_check_t < c.TIMEOUT:

        status = wrapper_sensorbus_status_read(desired_status, controller_id)
        if (status & 0x01) == desired_status:
            return True

    return False


# This Function does multiple things:
    # First, Ensures that SENSORBUS_STATUS is not busy
    # Second, Creates 32-bit word to write and writes word to memory
    # Third, checks to SENSORBUS_STATUS toggling to ensure complete write
def wrapper_write(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int, SENSORBUS_DATA: int, SENSORBUS_OP: int) -> None:

    status = wrapper_sensorbus_status_read(0, controller_id)
    if (status & 0x01) == 0x01:
        return c.ERROR

    data = create_word(SENSORBUS_BUSID, SENSORBUS_ADDR, SENSORBUS_DATA, SENSORBUS_OP)

    given_methods.Write(controller_id, c.FASTBUS_BASE_ADDR, data) 

    if not check_sbus_status(1, controller_id):
        return c.ERROR

    if not check_sbus_status(0, controller_id):
        return c.ERROR

    return 1


# Steps:
    # First step in SensoBus reading is to perform a SensorBus write
    # If Write is successful, wait until data is ready to be read
    # Once SENSORBUS_STATUS toggles, data is ready to be read from
    # Mask for the data byte and return data
def wrapper_read(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int) -> int:

    res_of_operation = wrapper_write(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR, 0x0, c.READ)
    if res_of_operation == c.ERROR:
        return c.ERROR

    if not check_sbus_status(1, controller_id):
        return c.ERROR

    if not check_sbus_status(0, controller_id):
        return c.ERROR

    data = given_methods.Read(controller_id, c.FASTBUS_BASE_ADDR)

    return ((data & 0x00FF0000) >> 16)




#------------------------------------------------------------------------------------------#
'''OLD'''
## SensorBus Write
#def wrapper_write(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int, SENSORBUS_DATA: int, SENSORBUS_OP: int) -> None:
#
#    # Ensure that SENSORBUS_STATUS is not busy
#    status = wrapper_sensorbus_status_read(0, controller_id)
#    if status == 0x01:
#        # Meaning ERROR
#        return c.ERROR
#
#    data = create_word(SENSORBUS_BUSID, SENSORBUS_ADDR, SENSORBUS_DATA, SENSORBUS_OP)
#
#    # Write this to Controller memory
#    given_methods.Write(controller_id, c.FASTBUS_BASE_ADDR, data) 
#
#    # Wait for SENSORBUS_STATUS[0] to go high
#    while True:
#        # (ADD TIMEOUT HERE)
#        val = wrapper_sensorbus_status_read(1, controller_id)
#        val &= 0x01
#        if val == 0x01:
#            break
#
#    # Wait for the SENSORBUS_STATUS[0] to go low again
#    while True:
#        val = wrapper_sensorbus_status_read(0, controller_id)
#        val &= 0x01
#        if val == 0x00:
#            break


## SensorBus Read
#def wrapper_read(controller_id: int, SENSORBUS_BUSID: int, SENSORBUS_ADDR: int) -> int:
#    # First step in SensoBus reading is to perform a SensorBus write
#    res_of_operation = wrapper_write(controller_id, SENSORBUS_BUSID, SENSORBUS_ADDR, 0x0, c.READ)
#    if res_of_operation == c.ERROR:
#        return c.ERROR
#
#    '''At this point data has been requested from the sensor, so now we wait''' 
#
#    # Wait for SENSORBUS_STATUS[0] to go high
#    while True:
#        val = wrapper_sensorbus_status_read(1, controller_id)
#        val &= 0x01
#        if val == 0x01:
#            break
#
#    # Wait for the SENSORBUS_STATUS[0] to go low again
#    while True:
#        val = wrapper_sensorbus_status_read(0, controller_id)
#        val &= 0x01
#        if val == 0x00:
#            break
#
#    # Now data is populated at BUS_DATA and can be read from
#    data = given_methods.Read(controller_id, c.FASTBUS_BASE_ADDR)
#
#    # Return an 8-bit data value
#    return ((data & 0x00FF0000) >> 16)
#------------------------------------------------------------------------------------------#

