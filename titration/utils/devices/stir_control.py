"""
The file for the StirControl class
"""
import math
from titration.utils import constants

if constants.IS_TEST:
    from titration.utils.devices import board_mock as board
    from titration.utils.devices import pwm_out_mock as pwmio
else:
    import board  # type: ignore
    import pwmio  # type: ignore

STIR_PWM_FAST = 5000
STIR_PWM_SLOW = 3000
STIR_FREQUENCY = 100
STIR_DUTY_CYCLE = 0


class StirControl:
    """
    The class for the stir controller device
    """

    def __init__(self):
        """
        The constructor for the mock stir controller class
        Initializes the pump's motor
        """
        self.motor = pwmio.PWMOut(
            board.D13, duty_cycle=STIR_DUTY_CYCLE, frequency=STIR_FREQUENCY
        )

    def set_motor_speed(self, target, gradual=False):
        """
        The function to set the motor speed
        """
        if gradual is True:
            direction = math.copysign(1, target - self.motor.duty_cycle)

            if direction == 1 and self.motor.duty_cycle < 1000:
                self.motor.duty_cycle = 1000

            while self.motor.duty_cycle != target:
                next_step = min(abs(target - self.motor.duty_cycle), 100)
                self.motor.duty_cycle = self.motor.duty_cycle + (next_step * direction)
        else:
            self.motor.duty_cycle = target

    def motor_speed_fast(self):
        """
        The function to set the motor speed to a fast setting
        """
        self.set_motor_speed(STIR_PWM_FAST, gradual=True)

    def motor_speed_slow(self):
        """
        The function to set the motor speed to a slow setting
        """
        self.set_motor_speed(STIR_PWM_SLOW, gradual=True)

    def motor_stop(self):
        """
        The function to stop the motor
        """
        self.set_motor_speed(0)
