import time

import pandas as pd

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9


class TemperatureControl:
    """
    Mock of Temperature Control class for running the PID control on the Alkalinity
    Titrator using a SSR and Heated Beaker Jacket
    """

    def __init__(self, relay_pin, sensor):
        self.sensor = sensor

    # Flag - print data to console or not
    printData = False

    # Flag - if False, update() does not toggle relay
    controlActive = False

    # PID Parameters
    kp = PID_DEFAULT_KP
    Ti = PID_DEFAULT_TI
    Td = PID_DEFAULT_TD

    # PID Gain
    k = 0
    integral = 0
    integral_prior = 0
    derivative = 0
    error = 0
    error_prior = 0

    # Step Count - How many cycles have we done?
    stepCount = 0

    # Time between steps (seconds) - how long to wait until next step
    timeStep = 1

    # The time the next step nets to be taken
    # not localtime() since we need fractional seconds
    timeNext = time.time()

    # last temperature read
    temperatureLast = 20

    # What state is the relay currently in
    relayOn = False

    # Log of times measurements were taken
    # timeLog = []

    # Data Fame of Measurements
    df = pd.DataFrame(columns=["time (s)", "temperature (C)", "gain"])

    # Target temperature
    setPoint = 30

    """
  Primary function run during the titration. update() will
  check if it is time to change the state of the relay and
  update the PID control and relay status as necessary
  """

    def update(self):
        # If
        if not self.controlActive:
            return

        timeNow = time.time()  # not localtime() since we need fractional seconds

        # TODO: Add logging of timeNow-timeNext results (how late?)
        if timeNow >= self.timeNext:
            if self.relayOn:
                # we'll turn it off
                # turn off
                self.__set_relayState(False)

                # count a step
                self.stepCount += 1

                # update error/integral_priors
                self.__update_priors()

                # set off time based on k
                self.__update_timeNext(time.time() + self.timeStep * (1 - self.k))

                # increase the temperature by k (0-1)
                self.temperatureLast = self.temperatureLast + self.k
                self.sensor.mock_set_temperature(self.temperatureLast)

            else:
                # Get data values
                temperature = self.temperatureLast

                # Check if relay needs to be turned on
                if temperature < self.setPoint - 0.5:
                    self.k = 1
                    self.__set_relayState(True)
                    self.__update_timeNext(time.time() + self.timeStep)

                # temperature above setpoint
                else:
                    self.k = 0
                    self.__set_relayState(False)
                    self.__update_timeNext(time.time() + self.timeStep)
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

        else:
            # pass until next update is called
            return

    def enable_print(self):
        self.printData = True

    def disable_print(self):
        self.printData = False

    def output_csv(self, filename):
        self.df.to_csv(filename, index_label="step", header=True)

    def at_temperature(self):
        if self.sensor.get_temperature() >= 29 and self.sensor.get_temperature() <= 30:
            return True
        else:
            return False

    def get_last_temperature(self):
        return self.temperatureLast

    def activate(self):
        self.controlActive = True
        self.__set_controlparam_default()
        self.timeNext = time.time()

    def deactivate(self):
        self.controlActive = False
        self.__set_relayState(False)

    def __update_timeLast(self, stepTime):
        """
        Update the time of the last step taken with the time of the
        step just taken with time.time()
        """
        self.timeLast = stepTime

    def __update_timeNext(self, stepTime):
        """
        Update the time that the next relay action should be taken
        """
        self.timeNext = stepTime

    def __set_controlparam_antiwindup(self):
        """
        After 250 cycles, the PID control parameters should
        be changed to new values
        """
        self.kp = PID_ANTIWINDUP_KP
        self.Ti = PID_ANTIWINDUP_TI
        self.Td = PID_ANTIWINDUP_TD

    def __set_controlparam_default(self):
        """
        For the first 250 cycles, the PID parameters should
        be set to their default values.
        """
        self.kp = PID_DEFAULT_KP
        self.Ti = PID_DEFAULT_TI
        self.Td = PID_DEFAULT_TD

    def __update_gains(self, temperature):
        self.error = self.setPoint - temperature
        self.integral = self.integral_prior + self.error * self.timeStep
        self.derivative = (self.error - self.error_prior) / self.timeStep
        self.k = self.kp * (
            self.error + self.Ti * self.integral + self.Td * self.derivative
        )

    def __update_priors(self):
        self.error_prior = self.error
        self.integral_prior = self.integral

    def __set_integral_zero(self):
        """
        For the first 250 cycles, the integral value should
        be zeroed to prevent windup
        """
        self.integral = 0

    def __set_relayState(self, boolean):
        self.relayOn = boolean