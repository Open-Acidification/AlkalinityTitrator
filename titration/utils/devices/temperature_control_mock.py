"""
The file for the TemperatureControl class
"""
import time
import pandas as pd

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9

TIMESTEP = 1
SETPOINT = 30

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
        self.relay = RELAY_PIN

        # Flag - print data to console or not
        self.printData = False

        # Flag - if False, update() does not toggle relay
        self.controlActive = False

        # PID Parameters
        self.kp = PID_DEFAULT_KP
        self.Ti = PID_DEFAULT_TI
        self.Td = PID_DEFAULT_TD

        # PID Gain
        self.k = 0
        self.integral = 0
        self.integral_prior = 0
        self.derivative = 0
        self.error = 0
        self.error_prior = 0

        # The time the next step nets to be taken
        # not localtime() since we need fractional seconds
        self.timeNext = time.time()

        # last temperature read
        self.temperatureLast = 20

        # What state is the relay currently in
        self.relayOn = False

        # Data Fame of Measurements
        self.df = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])


    def update(self):
        """
        The function run during the titration. update() will
        check if it is time to change the state of the relay and
        update the PID control and relay status as necessary
        """
        if self.controlActive:

            timeNow = time.time()  # not localtime() since we need fractional seconds

            # TODO: Add logging of timeNow-timeNext results (how late?)
            if timeNow >= self.timeNext:
                if self.relayOn:
                    # we'll turn it off
                    # turn off
                    self.__set_relayState(False)

                    # update error/integral_priors
                    self.__update_priors()

                    # set off time based on k
                    self.__update_timeNext(time.time() + TIMESTEP * (1 - self.k))

                    # increase the temperature by k (0-1)
                    self.temperatureLast = self.temperatureLast + self.k
                    self.sensor.mock_set_temperature(self.temperatureLast)

                else:
                    # Get data values
                    temperature = self.temperatureLast

                    # Check if relay needs to be turned on
                    if temperature < SETPOINT - 0.5:
                        self.k = 1
                        self.__set_relayState(True)
                        self.__update_timeNext(time.time() + TIMESTEP)

                    # temperature above setpoint
                    else:
                        self.k = 0
                        self.__set_relayState(False)
                        self.__update_timeNext(time.time() + TIMESTEP)
                        self.temperatureLast = self.temperatureLast - 0.1
                        self.__update_priors()

                    # Add data to df
                    data_frame_new = pd.DataFrame(
                        [[time.ctime(timeNow), temperature, self.k]],
                        columns=["time (s)", "temperature (C)", "gain"],
                    )
                    self.df = self.df.append(data_frame_new, ignore_index=True)
                    if self.printData:
                        print(self.df)

    def enable_print(self):
        """
        The function to enable printing of the temperature data
        """
        self.printData = True

    def disable_print(self):
        """
        The function to disable printing of the temperature data
        """
        self.printData = False

    def output_csv(self, filename):
        """
        The function to output the temperature data into a csv file
        """
        self.df.to_csv(filename, index_label="step", header=True)

    def at_temperature(self):
        """
        The function to determine if the temperature of the titration is at the set point
        """
        if self.sensor.get_temperature() >= 29 and self.sensor.get_temperature() <= 30:
            return True
        else:
            return False

    def get_last_temperature(self):
        """
        The function to return the last measured temperature
        """
        return self.temperatureLast

    def activate(self):
        """
        The function to activate the temperature controller
        """
        self.controlActive = True
        self.__set_controlparam_default()
        self.timeNext = time.time()

    def deactivate(self):
        """
        The function to deactivate the temperature controller
        """
        self.controlActive = False
        self.__set_relayState(False)

    def __update_timeLast(self, stepTime):
        """
        The function to update the time of the last step taken with the time of the
        step just taken with time.time()
        """
        self.timeLast = stepTime

    def __update_timeNext(self, stepTime):
        """
        The function to Update the time that the next relay action should be taken
        """
        self.timeNext = stepTime

    def __set_controlparam_antiwindup(self):
        """
        The function to set the control parameters to antiwindup mode
        After 250 cycles, the PID control parameters should
        be changed to new values
        """
        self.kp = PID_ANTIWINDUP_KP
        self.Ti = PID_ANTIWINDUP_TI
        self.Td = PID_ANTIWINDUP_TD

    def __set_controlparam_default(self):
        """
        The function to set the control parameters to default mode
        For the first 250 cycles, the PID parameters should
        be set to their default values.
        """
        self.kp = PID_DEFAULT_KP
        self.Ti = PID_DEFAULT_TI
        self.Td = PID_DEFAULT_TD

    def __update_gains(self, temperature):
        """
        The function to update the gain
        """
        self.error = SETPOINT - temperature
        self.integral = self.integral_prior + self.error * TIMESTEP
        self.derivative = (self.error - self.error_prior) / TIMESTEP
        self.k = self.kp * (
            self.error + self.Ti * self.integral + self.Td * self.derivative
        )

    def __update_priors(self):
        """
        The function to update the prior measurements
        """
        self.error_prior = self.error
        self.integral_prior = self.integral

    def __set_integral_zero(self):
        """
        The function to set the integral to zero
        For the first 250 cycles, the integral value should
        be zeroed to prevent windup
        """
        self.integral = 0

    def __set_relayState(self, boolean):
        """
        The function to set the relay state on or off
        """
        self.relayOn = boolean
