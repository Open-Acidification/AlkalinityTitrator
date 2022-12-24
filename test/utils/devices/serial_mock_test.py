"""
Module to test mock serial communication with arduino
"""

import titration.utils.constants as c
import titration.utils.devices.serial_mock as serial


def test_serial_create():
    """
    Function to test mock serial creation
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino is not None


def test_serial_output_buffer():
    """
    Function to test mock serial output buffer
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.reset_output_buffer()


def test_serial_input_buffer():
    """
    Function to test mock serial input buffer
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.reset_input_buffer()


def test_serial_writeable():
    """
    Function to test if mock serial is writeable
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino.writable()


#def test_serial_write(capsys):
#    """
#    Function to test a mock serial write
#    """
#    arduino = serial.Serial(
#        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
#    )
#    arduino.write("test string")

    # disabled due to printing on syringe_pump calls
    # captured = capsys.readouterr()
    # assert captured.out == "test string\n"


def test_serial_flush():
    """
    Function to test mock serial flush
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.flush()


def test_serial_readline():
    """
    Function to test serial readline
    """
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino.readline() == b"DONE\r\n"
