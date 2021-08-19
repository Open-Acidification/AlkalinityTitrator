import titration.utils.constants as constants
import titration.utils.interfaces as interfaces
import pwmio
import math

class Stir_Control():
    def __init__(self,pwm_pin, duty_cycle=constants.STIR_DUTY_CYCLE, frequency=constants.STIR_FREQUENCY):
        self.motor = pwmio.PWMOut(pwm_pin, duty_cycle=duty_cycle, frequency=frequency)

    def set_motor_speed(self, target, gradual=False):
        if gradual is True:
            direction = math.copysign(1, target - self.motor.duty_cycle)
            while self.motor.duty_cycle != target:
                next_step = min(abs(target - self.duty_cycle), 100)
                self.duty_cycle = self.duty_cycle + (next_step * direction)
                print("Stirrer set to ", self.duty_cycle)
                interfaces.delay(0.1)
        else:
            self.motor.duty_cycle = target
            print("Stirrer set to ", self.duty_cycle)
    
    def motor_speed_fast(self):
        self.set_motor_speed(constants.STIR_PWM_FAST, gradual=True)
    
    def motor_speed_slow(self):
        self.set_motor_speed(constants.STIR_PWM_SLOW, gradual=True)
    
    def motor_stop(self):
        self.set_motor_speed(0)