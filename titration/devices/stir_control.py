"""
The file for the StirControl class
"""
import math
import time

from titration.devices.library import board, pwmio

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
        self._motor = pwmio.PWMOut(
            board.D13, duty_cycle=STIR_DUTY_CYCLE, frequency=STIR_FREQUENCY
        )

    def _set_speed(self, target):
        """
        The function to set the motor speed
        """
        direction = math.copysign(1, target - self._motor.duty_cycle)

        if direction == 1 and self._motor.duty_cycle < 1000:
            self._motor.duty_cycle = 1000

        while self._motor.duty_cycle != target:
            next_step = min(abs(target - self._motor.duty_cycle), 100)
            self._motor.duty_cycle = self._motor.duty_cycle + (next_step * direction)

    def set_fast(self):
        """
        The function to set the motor speed to a fast setting
        """
        self._set_speed(STIR_PWM_FAST)

    def set_slow(self):
        """
        The function to set the motor speed to a slow setting
        """
        self._set_speed(STIR_PWM_SLOW)

    def set_stop(self):
        """
        The function to stop the motor
        """
        self._motor.duty_cycle = 0

    def degas(self, degas_time):
        """
        The function to degas the titration solution
        """
        self._set_speed(STIR_PWM_FAST)
        time.sleep(degas_time)
        self._set_speed(STIR_PWM_SLOW)
