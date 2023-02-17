import sys
import time

import constants1 as c


# Get time and convert to microseconds
def get_time():
    t = time.perf_counter() * 1_000_000
    return int(t)


# Checks if Controller is idle, if so begin generating data
# If Controller is past allowed time, moves to next Controller
def generate(ctlr_obj):

    if ctlr_obj.status == c.IDLE:
        ctlr_obj.status = c.BUSY
        ctlr_obj.time_start = get_time()
        ctlr_obj.request_sensor_data()

    elif ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.ALLOWED_TIME:
        reset_ctlr(ctlr_obj)


# Acts as the Producer, requests data from sensors and marks clipboard of start_time
def generator(index, controllers):

    start_us = get_time()
    while (get_time() - start_us) < c.TIME_QUANTUM:

        generate(controllers[index])

        index = index+1 if (index+1) < len(controllers) else 0

    return index


# If the Controller is bad or it has given data to Inspector, it resets
def reset_ctlr(ctlr_obj):

    ctlr_obj.status = c.IDLE
    ctlr_obj.valid = False
    ctlr_obj.sns_data = 0.0
    ctlr_obj.next_sensor()


# Checks if Controller has had enough time to get data
# If Controller has the data, Inspector records data, and resets Controller
def inspect(ctlr_obj):

    sensor_tuple = (-1,-1,-1)

    if ctlr_obj.status == c.BUSY and (get_time() - ctlr_obj.time_start) > c.AVG_TIME:

        if ctlr_obj.check_sensor_status(get_time() - ctlr_obj.time_start - c.AVG_TIME):
            data = ctlr_obj.sns_data 
            sensor_tuple = (ctlr_obj.bus_id, ctlr_obj.sensor_list[ctlr_obj.sns_index].bus_id, data)
            reset_ctlr(ctlr_obj)

    return sensor_tuple


# Acts as the Consumer checking if Controller's have ready temp_data
def inspector(index, controllers):
    start_us = get_time()
    sensor_measurements = []

    while (get_time() - start_us) < c.TIME_QUANTUM:
        sensor_measurements.append(inspect(controllers[index]))

        index = index+1 if (index+1) < len(controllers) else 0

    return (index, sensor_measurements)


# Writes inventory id's
def file_write_inventory(controller_list, sensor_list):
    inventory = open("inventory.txt", "w")
    for i, controller in enumerate(controller_list):
        inventory.write(f"Controller {i}: {controller.unique_id}\n")
        for j, sensor in enumerate(sensor_list[i]):
            inventory.write(f"  Sensor {j}: {sensor.unique_id}\n")


# Writes temperature data to log file
def file_write_logs(measurements):
    logs = open("logs.txt", "a")
    for measure in measurements:
        if measure == (-1,-1,-1):
            continue
        C_id, S_id, Temp = measure
        logs.write(f"Controller: {C_id} Sensor: {S_id} reads Temperature: {Temp}\n")

# If user wants to see output on console
def console_output(measurements):
    for measure in measurements:
        if measure == (-1,-1,-1):
            continue
        C_id, S_id, Temp = measure
        print(f"Controller: {C_id} Sensor: {S_id} reads Temperature: {Temp}")


