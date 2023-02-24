"""
The file for the temperature control mock
"""

# pylint: disable = too-many-instance-attributes, unused-argument

import time

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9


class TemperatureControl:
    """
    Mock of Temperature Control class for running the PID control on the Alkalinity
    titrator using a SSR and Heated Beaker Jacket
    """

    def __init__(self, relay_pin, sensor):
        """
        The constructor for the temperature controller
        """
        self.sensor = sensor

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

    # time between steps (seconds) - how long to wait until next step
    time_step = 1

    # The time the next step nets to be taken
    # not localtime() since we need fractional seconds
    time_next = time.time()

    # last temperature read
    temperature_last = 20

    # What state is the relay currently in
    relay_on = False

    # Log of times measurements were taken
    # timeLog = []

    # Data Fame of Measurements
    data_frame = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])

    # Target temperature
    set_point = 30

    """
  Primary function run during the titration. update() will
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

                # increase the temperature by k (0-1)
                self.temperature_last = self.temperature_last + self.k
                self.sensor.mock_set_temperature(self.temperature_last)

            else:
                # Get data values
                temperature = self.temperature_last

                # Check if relay needs to be turned on
                if temperature < self.set_point - 0.5:
                    self.k = 1
                    self.__set_relay_state(True)
                    self.__update_time_next(time.time() + self.time_step)

                # temperature above setpoint
                else:
                    self.k = 0
                    self.__set_relay_state(False)
                    self.__update_time_next(time.time() + self.time_step)
                    self.temperature_last = self.temperature_last - 0.1
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
        The function to print to the console
        """
        self.print_data = True

    def disable_print(self):
        """
        The function to disable the print to console
        """
        self.print_data = False

    def output_csv(self, filename):
        """
        The function to output data to a csv file
        """
        self.data_frame.to_csv(filename, index_label="step", header=True)

    def at_temperature(self):
        """
        The function to tell the current temperature
        """
        return bool(
            self.sensor.get_temperature() >= 29 and self.sensor.get_temperature() <= 30
        )

    def get_last_temperature(self):
        """
        The function to get the last temperature
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

    def __update_time_next(self, step_time):
        """
        Update the time that the next relay action should be taken
        """
        self.time_next = step_time

    def __set_controlparam_default(self):
        """
        For the first 250 cycles, the PID parameters should
        be set to their default values.
        """
        self.k_p = PID_DEFAULT_KP
        self.t_i = PID_DEFAULT_TI
        self.t_d = PID_DEFAULT_TD

    def __update_priors(self):
        """
        The function to update priors
        """
        self.error_prior = self.error
        self.integral_prior = self.integral

    def __set_relay_state(self, boolean):
        """
        The function to set the relay state
        """
        self.relay_on = boolean
