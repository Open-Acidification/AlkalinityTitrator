"""
The file to test the mock temperature controller
"""
import time

from titration.devices.library import board, TemperatureControl, TemperatureProbe


def create_temperature_controller():
    """
    The function to create a mock temperature controller for tests
    """
    sensor = TemperatureProbe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    return TemperatureControl(board.D1, sensor)


def test_temperature_control_create():
    """
    The function to test create a temperature controller
    """
    temperature_controller = create_temperature_controller()

    assert temperature_controller is not None


def test_temperature_control_update():
    """
    The function to test updating the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.update()
    time.sleep(1)
    temperature_controller.update()


def test_temperature_control_enable_print():
    """
    The function to test enabling the temperature controller's print
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.enable_print()


def test_temperature_control_disable_print():
    """
    The function to test disabling the temperature controller's print
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.disable_print()


def test_temperature_control_at_temperature():
    """
    The function to test the at_temperature function
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.at_temperature()


def test_temperature_control_last_temperature():
    """
    The function to get the last temperature from the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.get_last_temperature()


def test_temperature_control_activate():
    """
    The function to activate the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.activate()


def test_temperature_control_deactivate():
    """
    The function to deactivate the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.deactivate()
