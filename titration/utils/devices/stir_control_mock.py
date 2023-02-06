"""
The file for the mock StirControl Class
"""
import math
from titration.utils.devices import board_mock as board

STIR_PWM_FAST = 5000
STIR_PWM_SLOW = 3000
STIR_FREQUENCY = 100
STIR_DUTY_CYCLE = 0


class StirControl:
    """
    The class for the mock stir controller
    """

    def __init__(
        self,
        debug=False,
    ):
        """
        The constructor for the mock stir controller class
        Initializes the pump's motor
        """
        self.motor = (board.D13, STIR_DUTY_CYCLE, STIR_FREQUENCY)
        self.duty_cycle = STIR_DUTY_CYCLE
        self.debug = debug

    def set_motor_speed(self, target, gradual=False):
        """
        The function to set the motor speed
        """
        if gradual is True:
            direction = math.copysign(1, target - self.duty_cycle)

            if direction == 1 and self.duty_cycle < 1000:
                self.duty_cycle = 1000
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.duty_cycle))

            while self.duty_cycle != target:
                next_step = min(abs(target - self.duty_cycle), 100)
                self.duty_cycle = self.duty_cycle + (next_step * direction)
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.duty_cycle))
        else:
            self.duty_cycle = target
            if self.debug:
                print("Stirrer set to {0:.0f}".format(self.duty_cycle))

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
