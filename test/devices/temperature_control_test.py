"""
The file to test the mock temperature controller
"""
import time

from titration.devices.library import (
    TemperatureControl,
    TemperatureProbe,
    board,
)


def create_temperature_controller():
    """
    The function to create a mock temperature controller for tests
    """
    sensor = TemperatureProbe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    return TemperatureControl(sensor)


def test_temperature_control_create():
    """
    The function to test create a temperature controller
    """
    temperature_controller = create_temperature_controller()

    assert temperature_controller.control_active is False
    assert temperature_controller.k == 0
    assert temperature_controller.integral == 0
    assert temperature_controller.integral_prior == 0
    assert temperature_controller.derivative == 0
    assert temperature_controller.error == 0
    assert temperature_controller.error_prior == 0
    assert temperature_controller.k_p == 0.09
    assert temperature_controller.t_i == 0.000001
    assert temperature_controller.t_d == 9
    assert temperature_controller.step_count == 0
    assert temperature_controller.temperature_last == 0


def test_temperature_control_update():
    """
    The function to test updating the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.update()
    time.sleep(1)
    temperature_controller.update()


def test_temperature_control_at_temperature():
    """
    The function to test the at_temperature function
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.at_temperature()

    assert temperature_controller.at_temperature() is False


def test_temperature_control_last_temperature():
    """
    The function to get the last temperature from the temperature controller
    """
    temperature_controller = create_temperature_controller()

    assert temperature_controller.get_last_temperature() == 0


def test_temperature_control_deactivate():
    """
    The function to deactivate the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.deactivate()

    assert temperature_controller.control_active is False
    assert temperature_controller.relay.value == 0


def test_temperature_control_activate():
    """
    The function to test activating the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.activate()

    assert temperature_controller.control_active is True
    assert temperature_controller.k_p == 0.09
    assert temperature_controller.t_i == 0.000001
    assert temperature_controller.t_d == 9
