import math

import pwmio

import titration.utils.constants as constants


class Stir_Control:
    def __init__(
        self,
        pwm_pin,
        duty_cycle=constants.STIR_DUTY_CYCLE,
        frequency=constants.STIR_FREQUENCY,
        debug=False,
    ):
        self.motor = pwmio.PWMOut(pwm_pin, duty_cycle=duty_cycle, frequency=frequency)
        self.debug = False

    def set_motor_speed(self, target, gradual=False):
        if gradual is True:
            direction = math.copysign(1, target - self.motor.duty_cycle)

            # It won't move under 1000, so this speeds up the process
            if direction == 1 and self.motor.duty_cycle < 1000:
                self.motor.duty_cycle = 1000
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.motor.duty_cycle))

            while self.motor.duty_cycle != target:
                next_step = min(abs(target - self.motor.duty_cycle), 100)
                self.motor.duty_cycle = self.motor.duty_cycle + (next_step * direction)
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.motor.duty_cycle))
        else:
            self.motor.duty_cycle = target
            if self.debug:
                print("Stirrer set to {0:.0f}".format(self.motor.duty_cycle))

    def motor_speed_fast(self):
        self.set_motor_speed(constants.STIR_PWM_FAST, gradual=True)

    def motor_speed_slow(self):
        self.set_motor_speed(constants.STIR_PWM_SLOW, gradual=True)

    def motor_stop(self):
        self.set_motor_speed(0)
