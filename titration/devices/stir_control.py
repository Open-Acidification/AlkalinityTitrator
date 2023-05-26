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

        # Timer variables
        self.start_time = 0
        self.current_time = 0

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
        # Timer values
        self.start_time = degas_time
        self.current_time = time.time()

        self._set_speed(STIR_PWM_FAST)
        self._set_speed(STIR_PWM_SLOW)

    def get_timer(self):
        """
        The function to return the time left on the degas function
        """
        if time.time() < (self.current_time + self.start_time):
            seconds = float(self.start_time - (time.time() - self.current_time))
            minutes = math.floor(seconds / 60)
            seconds = int(seconds % 60)
            if seconds >= 10:
                return f"{minutes:>0.0f}:{seconds:>0.0f}"
            return f"{minutes:>0.0f}:0{seconds:>0.0f}"
        return "0:00"
