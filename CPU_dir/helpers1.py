import sys
import time

import constants1 as c


# Get time and convert to milliseconds
def get_time():
    t = time.perf_counter() * 1000
    return int(t)

def generate(ctlr_obj):
    # if controller idle, begin requesting from its current sensor index
    if ctlr_obj.status == c.IDLE:
        ctlr_obj.status = c.BUSY
        ctlr_obj.time_start = get_time()
        ctlr_obj.request_sensor_data()

    elif ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.ALLOWED_TIME:
        # This means the sensor is bad so move on to next sensor
        ctlr_obj.next_sensor()
        # Change the start time
        ctlr_obj.time_start = get_time()
        # Now request the new sensor's data
        ctlr_obj.request_sensor_data()


# Producer
def generator(index, controllers):
    start_ms = get_time()
    while (get_time() - start_ms) < c.TIME_QUANTUM:
        # Mark the clipboards
        generate(controllers[index])

        index += 1 if index+1 < len(controllers) else 0

        print("generator time")
        time.sleep(0.0001)
    print(get_time() - start_ms)
    return index

def reset_ctlr(ctlr_obj):
    ctlr_obj.status = c.IDLE
    ctlr_obj.valid = False
    ctlr_obj.sns_data = 0.0
    ctlr_obj.next_sensor()

def inspect(ctlr_obj, sensor_measurements):
    if ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.AVG_TIME:
        # Try and read from the sensor as enough time has passed
        if ctlr_obj.valid:
            data = ctlr_obj.sns_data 
            sensor_tuple = (ctlr_obj.unique_id, ctlr_obj.sensor_list[ctlr_obj.sns_index], data)
            sensor_measurements.append(sensor_tuple)
            reset_ctlr(ctlr_obj)
    return sensor_measurements

# Consumer
def inspector(index, controllers):
    start_ms = get_time()
    sensor_measurements = []
    while (get_time() - start_ms) < c.TIME_QUANTUM:
        inspect(controllers[index], sensor_measurements)
        # Mark the clipboards
        index += 1 if index+1 < len(controllers) else 0
        print("inspector time")
        time.sleep(0.0001)
    print(get_time() - start_ms)
    return index




