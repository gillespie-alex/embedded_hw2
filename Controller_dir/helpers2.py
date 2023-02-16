import random

import constants2 as c


# Given Read Method
def Given_Read(busId: int, address: int) -> int:
    # Return a random 32 bit word to mimic register reading
    data = random.randint(0, 4_294_967_295)
    return data

def wrapper_read(controller_id: int, UNIQUE_ID_ADDR: int) -> int:
    return Given_Read(controller_id, UNIQUE_ID_ADDR)

# Outlier chance of sensor taking more than thousand microseconds 
def calc_noise():
    noise = random.randint(0,50)
    # Only 4% chance
    if noise >= 49:
        noise += c.OUTLIER_T
    return noise
