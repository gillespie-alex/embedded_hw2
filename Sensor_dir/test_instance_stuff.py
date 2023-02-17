import pytest
from unittest.mock import MagicMock

from Sensor import TempSensor
import helpers3 as h


@pytest.fixture
def my_sensor():
    return TempSensor(master=1,bus_id=1)

def test_get_id(my_sensor):
    my_sensor.get_id()
    print(my_sensor.unique_id)

def test_request_data(my_sensor):
    data = my_sensor.request_data(1, 1, 0x45)
    print(f"Data read from sensor: {data}")


# Grouping tests into sbus_ops
'''pytest ./my_test.py -m sbus_ops'''
@pytest.mark.sbus_ops
def test_check_sbus_status():
    print("\n Doing sbus status sbus_ops\n")
    assert h.check_sbus_status(1,1) == True

@pytest.mark.sbus_ops
def test_check_wrapper_write():
    print("\n Doing sbus wrapper_write sbus_ops\n")
    assert h.wrapper_write(1,1, 0x46, 0, 0) == 1

@pytest.mark.sbus_ops
def test_check_wrapper_read():
    print("\n Doing sbus wrapper_read sbus_ops\n")
    data = h.wrapper_read(1,1, 0x46)
    print(data)
    assert data != -999
