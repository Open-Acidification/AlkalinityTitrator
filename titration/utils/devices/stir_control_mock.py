"""
The file for the stir control mock
"""
import math
from titration.utils import constants

# pylint: disable = W0613


class StirControl:
    """
    The class for the stir control mock
    """

    def __init__(
        self,
        pwm_pin,
        duty_cycle=constants.STIR_DUTY_CYCLE,
        frequency=constants.STIR_FREQUENCY,
        debug=False,
    ):
        """
        The constructor for the mock Stir Control
        """
        self.duty_cycle = 0
        self.debug = debug

    def set_motor_speed(self, target, gradual=False):
        """
        The function to set the mock motor speed
        """
        if gradual is True:
            direction = math.copysign(1, target - self.duty_cycle)

            # It won't move under 1000, so this speeds up the process
            if direction == 1 and self.duty_cycle < 1000:
                self.duty_cycle = 1000
                if self.debug:
                    print(f"Stirrer set to {self.duty_cycle}")

            while self.duty_cycle != target:
                next_step = min(abs(target - self.duty_cycle), 100)
                self.duty_cycle = self.duty_cycle + (next_step * direction)
                if self.debug:
                    print(f"Stirrer set to {self.duty_cycle}")
        else:
            self.duty_cycle = target
            if self.debug:
                print(f"Stirrer set to {self.duty_cycle}")

    def motor_speed_fast(self):
        """
        The function to set the motor speed to fast
        """
        self.set_motor_speed(constants.STIR_PWM_FAST, gradual=True)

    def motor_speed_slow(self):
        """
        The function to set the motor speed to slow
        """
        self.set_motor_speed(constants.STIR_PWM_SLOW, gradual=True)

    def motor_stop(self):
        """
        The function to stop the motor
        """
        self.set_motor_speed(0)
