import sys
import time

import constants1 as c


# Get time and convert to milliseconds
def get_time():
    t = time.perf_counter() * 1_000_000
    return int(t)

def generate(ctlr_obj):
    # if controller idle, begin requesting from its current sensor index
    if ctlr_obj.status == c.IDLE:
        ctlr_obj.status = c.BUSY
        ctlr_obj.time_start = get_time()
        ctlr_obj.request_sensor_data()

    elif ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.ALLOWED_TIME:
        print("Encountered an invalid sensor")
        print(ctlr_obj.__dict__)
        # This means the sensor is bad so move on to next sensor by resetting controller
        reset_ctlr(ctlr_obj)
        print("after change:")
        print(ctlr_obj.__dict__)


# Producer
def generator(index, controllers):
    start_us = get_time()
    while (get_time() - start_us) < c.TIME_QUANTUM:
        # Mark the clipboards
        generate(controllers[index])

        index = index+1 if (index+1) < len(controllers) else 0

        #print(f"generator time at index {index}")
        #time.sleep(0.0001)
    return index

def reset_ctlr(ctlr_obj):
    ctlr_obj.status = c.IDLE
    ctlr_obj.valid = False
    ctlr_obj.sns_data = 0.0
    ctlr_obj.next_sensor()

def inspect(ctlr_obj):
    sensor_tuple = (-1,-1,-1)
    # Try and read from the sensor as enough avg time has passed
    if ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.AVG_TIME:
        # The value passed is equal to how much time we are past the AVG_TIME
        if ctlr_obj.check_sensor_status(get_time() - ctlr_obj.time_start - c.AVG_TIME):
            data = ctlr_obj.sns_data 
            sensor_tuple = (ctlr_obj.bus_id, ctlr_obj.sensor_list[ctlr_obj.sns_index].bus_id, data)
            reset_ctlr(ctlr_obj)
    return sensor_tuple

# Consumer
def inspector(index, controllers):
    start_us = get_time()
    sensor_measurements = []
    while (get_time() - start_us) < c.TIME_QUANTUM:
        sensor_measurements.append(inspect(controllers[index]))
        # Mark the clipboards
        index = index+1 if (index+1) < len(controllers) else 0
        #print(f"inspector time at index {index}")
    return (index, sensor_measurements)


def console_output(measurements):
    for measure in measurements:
        if measure == (-1,-1,-1):
            continue
        C_id, S_id, Temp = measure
        print(f"Controller: {C_id} Sensor: {S_id} reads Temperature: {Temp}")

def file_write_inventory(controller_list, sensor_list):
    inventory = open("inventory.txt", "w")
    for i, controller in enumerate(controller_list):
        inventory.write(f"Controller {i}: {controller.unique_id}\n")
        for j, sensor in enumerate(sensor_list[i]):
            inventory.write(f"  Sensor {j}: {sensor.unique_id}\n")


def file_write_logs():
    pass

