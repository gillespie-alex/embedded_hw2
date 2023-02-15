# Lambdas
SBUS_ID = lambda val: val
SBUS_ADDR = lambda val: val << 8
SBUS_DATA = lambda val: val << 16
SBUS_OP = lambda val: val << 24

# Addresses
FASTBUS_BASE_ADDR     = 0x21112000
FASTBUS_SENSOR_STATUS = 0x21112004


# Constants
READ = 0x00
NUM_CONTROLLERS = 16
