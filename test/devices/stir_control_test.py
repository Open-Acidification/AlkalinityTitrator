"""
The file to test the StirControl class
"""
from unittest import mock
from unittest.mock import call

from titration.devices.library import StirControl


def test_create_stir_controller():
    """
    The function to test the creation of a stir controller
    """
    stir_controller = StirControl()

    assert stir_controller._motor is not None
    assert stir_controller._motor.duty_cycle == 0
    assert stir_controller._motor.frequency == 100


def test_set_speed():
    """
    The function to test the _set_speed function
    The three asserts test the three use cases of _set_speed()
    at STIR_PWM_FAST and STIR_PWM_SLOW
    """
    stir_controller = StirControl()

    stir_controller._set_speed(5000)
    assert stir_controller._motor.duty_cycle == 5000

    stir_controller._set_speed(3000)
    assert stir_controller._motor.duty_cycle == 3000

    stir_controller._set_speed(0)
    assert stir_controller._motor.duty_cycle == 0


@mock.patch.object(StirControl, "_set_speed")
def test_set_speed_fast(_set_speed):
    """
    The function to test the set motor speed fast function
    """
    stir_controller = StirControl()

    stir_controller.set_fast()

    _set_speed.assert_called_with(5000)


@mock.patch.object(StirControl, "_set_speed")
def test_set_speed_slow(_set_speed):
    """
    The function to test the set motor speed slow function
    """
    stir_controller = StirControl()

    stir_controller.set_slow()

    _set_speed.assert_called_with(3000)


def test_set_stop():
    """
    The function to test the motor stop function
    """
    stir_controller = StirControl()

    stir_controller._motor.duty_cycle = 3000

    stir_controller.set_stop()
    assert stir_controller._motor.duty_cycle == 0


@mock.patch.object(StirControl, "_set_speed")
def test_degas(_set_speed):
    """
    The function to test the stir controller's degas function
    """
    stir_controller = StirControl()

    stir_controller.degas(0)

    calls = [call(5000), call(3000)]
    _set_speed.assert_has_calls(calls)
