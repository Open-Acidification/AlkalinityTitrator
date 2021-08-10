import time
from array import *

import pandas as pd

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9

# tempcontrol
class TempControl:
    """
    Temp Control class for running the PID control on the Alkalinity
    Titrator using a SSR and Heated Beaker Jacket

    """

    def __init__(self, sensor, relay_pin):
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
    tempLast = 20

    # What state is the relay currently in
    relayOn = False

    # Log of times measurements were taken
    # timeLog = []

    # Data Fame of Measurements
    df = pd.DataFrame(columns=["time (s)", "temp (C)", "gain"])

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
                self.tempLast = self.tempLast + self.k

            else:
                # Get data values
                temp = self.tempLast

                # Check if relay needs to be turned on
                if temp < self.setPoint - 0.5:
                    self.k = 1
                    self.__set_relayState(True)
                    self.__update_timeNext(time.time() + self.timeStep)

                # temp above setpoint
                else:
                    self.k = 0
                    self.__set_relayState(False)
                    self.__update_timeNext(time.time() + self.timeStep)
                    self.tempLast = self.tempLast - 0.1
                    self.__update_priors()

                # Add data to df
                data_frame_new = pd.DataFrame(
                    [[time.ctime(timeNow), temp, self.k]],
                    columns=["time (s)", "temp (C)", "gain"],
                )
                self.df = self.df.append(data_frame_new, ignore_index=True)
                if self.printData == True:
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

    def at_temp(self):
        if self.tempLast >= 29 and self.tempLast <= 30:
            return True
        else:
            return False

    def get_last_temp(self):
        return self.tempLast

    def activate(self):
        self.controlActive = True
        self.__set_controlparam_default()
        timeNext = time.time()

    def deactivate(self):
        self.controlActive = False
        self.__set_relayState(False)

    """
  Update the time of the last step taken with the time of the 
  step just taken with time.time()
  """

    def __update_timeLast(self, stepTime):
        self.timeLast = stepTime

    """
  Update the time that the next relay action should be taken
  """

    def __update_timeNext(self, stepTime):
        self.timeNext = stepTime

    """
  After 250 cycles, the PID control parameters should
  be changed to new values
  """

    def __set_controlparam_antiwindup(self):
        self.kp = PID_ANTIWINDUP_KP
        self.Ti = PID_ANTIWINDUP_TI
        self.Td = PID_ANTIWINDUP_TD

    """
  For the first 250 cycles, the PID parameters should
  be set to their default values. 
  """

    def __set_controlparam_default(self):
        self.kp = PID_DEFAULT_KP
        self.Ti = PID_DEFAULT_TI
        self.Td = PID_DEFAULT_TD

    def __update_gains(self, temp):
        self.error = self.setPoint - temp
        self.integral = self.integral_prior + self.error * self.timeStep
        self.derivative = (self.error - self.error_prior) / self.timeStep
        self.k = self.kp * (
            self.error + self.Ti * self.integral + self.Td * self.derivative
        )

    def __update_priors(self):
        self.error_prior = self.error
        self.integral_prior = self.integral

    """
  For the first 250 cycles, the integral value should
  be zeroed to prevent windup 
  """

    def __set_integral_zero(self):
        self.integral = 0

    def __set_relayState(self, boolean):
        self.relayOn = boolean


if __name__ == "__main__":
    tempControl = TempControl()
    tempControl.enable_print()
    tempControl.activate()

    # 10min time
    timeCurr = time.time()
    timeEnd = timeCurr + 60
    print("Time Start: ", time.ctime(timeCurr), "\nTime End: ", time.ctime(timeEnd))
    while timeEnd > time.time():
        tempControl.update()

    filename = "data/TempCtrl_" + time.ctime() + ".csv"
    filename = filename.replace(":", "-")
    filename = filename.replace(" ", "_")

    tempControl.output_csv(filename)

    tempControl.deactivate()
