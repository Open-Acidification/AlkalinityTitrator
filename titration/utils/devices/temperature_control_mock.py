"""
The file for the TemperatureControl class
"""
import time
import pandas as pd

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

        # Flag - if False, update() does not toggle relay
        self.control_active = False

        # PID Gain
        self.k = 0

        # The time the next step nets to be taken
        # not localtime() since we need fractional seconds
        self.time_next = time.time()

        # last temperature read
        self.temperature_last = 20

        # What state is the relay currently in
        self.relay_on = False

        # Data Fame of Measurements
        self.df = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])


    def update(self):
        """
        The function run during the titration. update() will
        check if it is time to change the state of the relay and
        update the PID control and relay status as necessary
        """
        if self.control_active:

            timeNow = time.time()  # not localtime() since we need fractional seconds

            if timeNow >= self.time_next:
                if self.relay_on:

                    # turn off
                    self.__set_relay_state(False)

                    # set off time based on k
                    self.__update_time_next(time.time() + TIMESTEP * (1 - self.k))

                    # increase the temperature by k (0-1)
                    self.temperature_last = self.temperature_last + self.k
                    self.sensor.mock_set_temperature(self.temperature_last)

                else:
                    # Get data values
                    temperature = self.temperature_last

                    # Check if relay needs to be turned on
                    if temperature < SETPOINT - 0.5:
                        self.k = 1
                        self.__set_relay_state(True)
                        self.__update_time_next(time.time() + TIMESTEP)

                    # temperature above setpoint
                    else:
                        self.k = 0
                        self.__set_relay_state(False)
                        self.__update_time_next(time.time() + TIMESTEP)
                        self.temperature_last = self.temperature_last - 0.1
                        self.__update_priors()

                    # Add data to df
                    data_frame_new = pd.DataFrame(
                        [[time.ctime(timeNow), temperature, self.k]],
                        columns=["time (s)", "temperature (C)", "gain"],
                    )
                    self.df = self.df.append(data_frame_new, ignore_index=True)

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

    def __update_time_next(self, stepTime):
        """
        The function to Update the time that the next relay action should be taken
        """
        self.time_next = stepTime

    def __set_relay_state(self, boolean):
        """
        The function to set the relay state on or off
        """
        self.relay_on = boolean
