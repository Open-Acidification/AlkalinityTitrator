"""
The file to test the mock temperature controller
"""
import time

from titration.devices.library import Heater, TemperatureControl, TemperatureProbe


def create_temperature_controller():
    """
    The function to create a mock temperature controller for tests
    """
    return TemperatureControl(TemperatureProbe(1), Heater(12))


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


def test_temperature_control_deactivate():
    """
    The function to deactivate the temperature controller
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.deactivate()

    assert temperature_controller.control_active is False
    assert temperature_controller.heater.value == 0


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


def test_temperature_control_at_temperature():
    """
    The function to test the temperature controller's at_temperature function
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(30.5)
    assert temperature_controller.at_temperature() is True

    temperature_controller.temperature_probe.sensor.set_temperature(30.6)
    assert temperature_controller.at_temperature() is False

    temperature_controller.temperature_probe.sensor.set_temperature(29.5)
    assert temperature_controller.at_temperature() is True

    temperature_controller.temperature_probe.sensor.set_temperature(29.4)
    assert temperature_controller.at_temperature() is False


def test_temperature_control_active_below_set_point():
    """
    The function to test the response of the temperature controller
    when it is active and below the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(25)

    temperature_controller.activate()
    assert temperature_controller.control_active is True

    temperature_controller.update()
    assert temperature_controller.heater.value is True


def test_temperature_control_active_above_set_point():
    """
    The function to test the response of the temperature controller
    when it is active and above the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(35)

    temperature_controller.activate()
    assert temperature_controller.control_active is True

    temperature_controller.update()
    assert temperature_controller.heater.value is False


def test_temperature_control_active_at_set_point():
    """
    The function to test the response of the temperature controller
    when it is active and at the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(30)

    temperature_controller.activate()
    assert temperature_controller.control_active is True

    temperature_controller.update()
    assert temperature_controller.heater.value is False


def test_temperature_control_inactive_below_set_point():
    """
    The function to test the response of the temperature controller
    when it is inactive and below the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(25)

    temperature_controller.deactivate()
    assert temperature_controller.control_active is False

    temperature_controller.update()
    assert temperature_controller.heater.value is False


def test_temperature_control_inactive_above_set_point():
    """
    The function to test the response of the temperature controller
    when it is inactive and above the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(35)

    temperature_controller.deactivate()
    assert temperature_controller.control_active is False

    temperature_controller.update()
    assert temperature_controller.heater.value is False


def test_temperature_control_inactive_at_set_point():
    """
    The function to test the response of the temperature controller
    when it is inactive and at the set point
    """
    temperature_controller = create_temperature_controller()

    temperature_controller.temperature_probe.sensor.set_temperature(30)

    temperature_controller.deactivate()
    assert temperature_controller.control_active is False

    temperature_controller.update()
    assert temperature_controller.heater.value is False
