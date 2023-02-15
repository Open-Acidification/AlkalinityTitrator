"""
The file for the temperature controller device
"""

# pylint: disable = E0401, R0902, R0912, W0621

import time
import adafruit_max31865
import busio
import digitalio
import pandas as pd
from gpiozero import LED

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9


class TemperatureControl:
    """
    Temperature Control class for running the PID control on the Alkalinity
    t_itrator using a SSR and Heated Beaker Jacket

    """

    def __init__(self, relay_pin, sensor):
        """
        The constructor for the Temperature Controller
        """
        self.sensor = sensor
        self.relay = LED(relay_pin)

    # Flag - print data to console or not
    print_data = False

    # Flag - if False, update() does not toggle relay
    control_active = False

    # PID Parameters
    k_p = PID_DEFAULT_KP
    t_i = PID_DEFAULT_TI
    t_d = PID_DEFAULT_TD

    # PID Gain
    k = 0
    integral = 0
    integral_prior = 0
    derivative = 0
    error = 0
    error_prior = 0

    # Step Count - How many cycles have we done?
    step_count = 0

    # t_ime between steps (seconds) - how long to wait until next step
    time_step = 1

    # The time the next step nets to be taken
    # not localtime() since we need fractional seconds
    time_next = time.time()

    # last temperature read
    temperature_last = 0

    # What state is the relay currently in
    relay_on = False

    # Log of times measurements were taken
    # timeLog = []

    # Data Fame of Measurements
    data_frame = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])

    # Target temperature
    set_point = 30

    """
  Primary function run during the Alkalinityt_itrator.titration. update() will
  check if it is time to change the state of the relay and
  update the PID control and relay status as necessary
  """

    def update(self):
        """
        The function to update the temperature controller
        """
        if not self.control_active:
            return

        time_now = time.time()  # not localtime() since we need fractional seconds

        if time_now >= self.time_next:
            if self.relay_on:
                # we'll turn it off
                # turn off
                self.__set_relay_state(False)

                # count a step
                self.step_count += 1

                # update error/integral_priors
                self.__update_priors()

                # set off time based on k
                self.__update_time_next(time.time() + self.time_step * (1 - self.k))

            else:
                # Get data values
                temperature = self.sensor.get_temperature()
                self.temperature_last = temperature
                # timelog.append(time_now.tm_sec)

                # anti-windup
                if self.step_count < 250:
                    self.__set_integral_zero()
                elif self.step_count == 250:
                    self.__set_controlparam_antiwindup()

                # Update PID Gain
                self.__update_gains(temperature)

                # Check if relay needs to be turned on
                if temperature < self.set_point:
                    if self.k <= 0:
                        self.k = 0
                        self.__update_time_next(time.time() + self.time_step)
                    elif self.k < 1:
                        self.__set_relay_state(True)
                        self.__update_time_next(time.time() + self.time_step * self.k)
                    else:
                        self.k = 1
                        self.__set_relay_state(True)
                        self.__update_time_next(time.time() + self.time_step)

                # temperature above setpoint
                else:
                    self.k = 0
                    self.__set_relay_state(False)
                    self.__update_time_next(time.time() + self.time_step)
                    self.__update_priors()

                # Add data to data_frame
                data_frame_new = pd.DataFrame(
                    [[time.ctime(time_now), temperature, self.k]],
                    columns=["time (s)", "temperature (C)", "gain"],
                )
                self.data_frame = self.data_frame.append(
                    data_frame_new, ignore_index=True
                )
                if self.print_data:
                    print(self.data_frame)

        else:
            # pass until next update is called
            return

    def enable_print(self):
        """
        The function to enable the print
        """
        self.print_data = True

    def disable_print(self):
        """
        The function to disable the print
        """
        self.print_data = False

    def output_csv(self, filename):
        """
        The function to output data to the csv file
        """
        self.data_frame.to_csv(filename, index_label="step", header=True)

    def at_temperature(self):
        """
        The function to tell if the solution is at temperature
        """
        return bool(
            self.sensor.get_temperature() >= 29.5
            and self.sensor.get_temperature() <= 30.5
        )

    def get_last_temperature(self):
        """
        The function to return the last temperature
        """
        return self.temperature_last

    def activate(self):
        """
        The function to activate the temperature controller
        """
        self.control_active = True
        self.__set_controlparam_default()
        self.time_next = time.time()

    def deactivate(self):
        """
        The function to deactivate the temperature controller
        """
        self.control_active = False
        self.__set_relay_state(False)

    def __update_time_next(self, stept_ime):
        """
        Update the time that the next relay action should be taken
        """
        self.time_next = stept_ime

    def __set_controlparam_antiwindup(self):
        """
        After 250 cycles, the PID control parameters should
        be changed to new values
        """
        self.k_p = PID_ANTIWINDUP_KP
        self.t_i = PID_ANTIWINDUP_TI
        self.t_d = PID_ANTIWINDUP_TD

    def __set_controlparam_default(self):
        """
        For the first 250 cycles, the PID parameters should
        be set to their default values.
        """
        self.k_p = PID_DEFAULT_KP
        self.t_i = PID_DEFAULT_TI
        self.t_d = PID_DEFAULT_TD

    def __update_gains(self, temperature):
        """
        The function to update the gains
        """
        self.error = self.set_point - temperature
        self.integral = self.integral_prior + self.error * self.time_step
        self.derivative = (self.error - self.error_prior) / self.time_step
        self.k = self.k_p * (
            self.error + self.t_i * self.integral + self.t_d * self.derivative
        )

    def __update_priors(self):
        """
        The function to update the priors
        """
        self.error_prior = self.error
        self.integral_prior = self.integral

    def __set_integral_zero(self):
        """
        For the first 250 cycles, the integral value should
        be zeroed to prevent windup
        """
        self.integral = 0

    def __set_relay_state(self, boolean):
        """
        The function to set the relay state
        """
        self.relay_on = boolean
        if boolean:
            self.relay.on()
        else:
            self.relay.off()


if __name__ == "__main__":
    import board

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)  # Chip select of the MAX31865 board.
    sensor = adafruit_max31865.MAX31865(
        spi, cs, rtd_nominal=1000, ref_resistor=4300, wires=3
    )

    temperature_control = TemperatureControl(sensor, 12)
    temperature_control.enable_print()

    # 10min time
    timeCurr = time.time()
    timeEnd = timeCurr + 3600
    print("t_ime Start: ", time.ctime(timeCurr), "\nt_ime End: ", time.ctime(timeEnd))
    while timeEnd > time.time():
        temperature_control.update()

    filename = "data/TemperatureCtrl_" + time.ctime() + ".csv"
    filename = filename.replace(":", "-")
    filename = filename.replace(" ", "_")

    temperature_control.output_csv(filename)
