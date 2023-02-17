"""
The file to test the StirControl class
"""
from titration.utils.devices.stir_control import StirControl


def create_stir_controller():
    """
    The function to create a test stir controller
    """
    return StirControl()


def test_create_stir_controller():
    """
    The function to test the creation of a stir controller
    """
    stir_controller = create_stir_controller()

    assert stir_controller.motor is not None
    assert stir_controller.motor.duty_cycle == 0
    assert stir_controller.motor.frequency == 100


def test_set_motor_speed_gradual():
    """
    The function to test the set motor speed function with the gradual option
    """
    stir_controller = create_stir_controller()

    stir_controller.set_motor_speed(4000, gradual=True)

    assert stir_controller.motor.duty_cycle == 4000


def test_set_motor_speed_not_gradual():
    """
    The function to test the set motor speed function without the gradual option
    """
    stir_controller = create_stir_controller()

    stir_controller.set_motor_speed(4000)

    assert stir_controller.motor.duty_cycle == 4000


def test_motor_speed_fast():
    """
    The function to test the set motor speed fast function
    """
    stir_controller = create_stir_controller()

    stir_controller.motor_speed_fast()

    assert stir_controller.motor.duty_cycle == 5000


def test_motor_speed_slow():
    """
    The function to test the set motor speed slow function
    """
    stir_controller = create_stir_controller()

    stir_controller.motor_speed_slow()

    assert stir_controller.motor.duty_cycle == 3000


def test_motor_stop():
    """
    The function to test the motor stop function
    """
    stir_controller = create_stir_controller()

    stir_controller.motor.duty_cycle = 5000

    stir_controller.motor_stop()

    assert stir_controller.motor.duty_cycle == 0
