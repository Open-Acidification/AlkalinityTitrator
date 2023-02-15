"""
The file to test the mock serial peripheral
"""
from AlkalinityTitrator.titration.utils import constants
from AlkalinityTitrator.titration.utils.devices.serial_mock import Serial


def create_arduino():
    """
    The function to create a mock arduino peripheral
    """
    return Serial(
        port=constants.ARDUINO_PORT,
        baudrate=constants.ARDUINO_BAUD,
        timeout=constants.ARDUINO_TIMEOUT,
    )


def test_serial_create():
    """
    The function to test mock serial creation
    """
    arduino = create_arduino()
    assert arduino is not None


def test_serial_output_buffer():
    """
    The function to test mock serial output buffer
    """
    arduino = create_arduino()
    arduino.reset_output_buffer()


def test_serial_input_buffer():
    """
    The function to test mock serial input buffer
    """
    arduino = create_arduino()
    arduino.reset_input_buffer()


def test_serial_writeable():
    """
    The function to test if mock serial is writeable
    """
    arduino = create_arduino()
    assert arduino.writable()


def test_serial_flush():
    """
    The function to test mock serial flush
    """
    arduino = create_arduino()
    arduino.flush()


def test_serial_readline():
    """
    The function to test serial readline
    """
    arduino = create_arduino()
    assert arduino.readline() == b"DONE\r\n"
