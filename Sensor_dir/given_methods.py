import random


# All these methods already have software drivers written for them
def Write(busId: int, address: int, data: int) -> None:
    # This function doesn't return anything
    pass


def Read(busId: int, address: int) -> int:
    # Return a random 32 bit word to mimic register reading
    data = random.randint(0, 4_294_967_295)
    return data


def Linear_Function(raw_temp_data):
    return random.randint(-100, 100)


def Read0(busId: int, address: int) -> int:
    data = 0x00
    return data


def Read1(busId: int, address: int) -> int:
    data = 0x01
    return data
