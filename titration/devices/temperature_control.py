"""
The file for the temperature controller device
"""

# pylint:disable=too-many-instance-attributes, too-many-branches, redefined-outer-name

import time

import pandas as pd
from titration.devices.library import LED


TIMESTEP = 1
SETPOINT = 30

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9

RELAY_PIN = 12


class TemperatureControl:
    """
    The class for the mock Temperature Controller
    running the PID control on the Alkalinity Titrator
    using a SSR and Heated Beaker Jacket
    """

    def __init__(self, sensor):
        """
        The constructor for the TemperatureControl class

        Parameters:
            relay_pin (Pin object): the pin for the relay
            sensor (Pin object): the pin for the temperature sensor
        """
        self.sensor = sensor
        self.relay = LED(RELAY_PIN)

        # Flag - if False, update() does not toggle relay
        self.control_active = False

        # PID Gain
        self.k = 0
        self.integral = 0
        self.integral_prior = 0
        self.derivative = 0
        self.error = 0
        self.error_prior = 0

        # PID Parameters
        self.k_p = PID_DEFAULT_KP
        self.t_i = PID_DEFAULT_TI
        self.t_d = PID_DEFAULT_TD

        self.step_count = 0

        # The time the next step nets to be taken
        # not localtime() since we need fractional seconds
        self.time_next = time.time()

        # last temperature read
        self.temperature_last = 0

        # Data Fame of Measurements
        self.data_frame = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])

    def update(self):
        """
        The function run during the titration. update() will
        check if it is time to change the state of the relay and
        update the PID control and relay status as necessary
        """
        if not self.control_active:
            return

        time_now = time.time()

        if time_now >= self.time_next:
            if self.relay.value == 1:
                self.relay.off()
                self.step_count += 1
                self.__update_priors()
                self.time_next = time.time() + TIMESTEP * (1 - self.k)

            else:
                # Get data values
                temperature = self.sensor.get_temperature()
                self.temperature_last = temperature

                # anti-windup
                if self.step_count < 250:
                    self.integral = 0
                elif self.step_count == 250:
                    self.__set_controlparam_antiwindup()

                # Update PID Gain
                self.__update_gains(temperature)

                # Check if relay needs to be turned on
                if temperature < SETPOINT:
                    if self.k <= 0:
                        self.k = 0
                        self.time_next = time.time() + TIMESTEP
                    elif self.k < 1:
                        self.relay.on()
                        self.time_next = time.time() + TIMESTEP * self.k
                    else:
                        self.k = 1
                        self.relay.on()
                        self.time_next = time.time() + TIMESTEP

                # temperature above setpoint
                else:
                    self.k = 0
                    self.relay.off()
                    self.time_next = time.time() + TIMESTEP
                    self.__update_priors()

                # Add data to self.data_frame
                data_frame_new = pd.DataFrame(
                    [[time.ctime(time_now), temperature, self.k]],
                    columns=["time (s)", "temperature (C)", "gain"],
                )
                self.data_frame = self.data_frame.append(
                    data_frame_new, ignore_index=True
                )

    def output_csv(self, filename):
        """
        The function to output a csv file of the temperature data
        """
        self.data_frame.to_csv(filename, index_label="step", header=True)

    def at_temperature(self):
        """
        The function to see if the sensor is at the specified temperature
        """
        return bool(
            self.sensor.get_temperature() >= 29.5
            and self.sensor.get_temperature() <= 30.5
        )

    def get_last_temperature(self):
        """
        The function to get the last measured temperature
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
        self.relay.off()

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
        self.error = SETPOINT - temperature
        self.integral = self.integral_prior + self.error * TIMESTEP
        self.derivative = (self.error - self.error_prior) / TIMESTEP
        self.k = self.k_p * (
            self.error + self.t_i * self.integral + self.t_d * self.derivative
        )

    def __update_priors(self):
        """
        The function to update the priors
        """
        self.error_prior = self.error
        self.integral_prior = self.integral
