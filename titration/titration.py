# Main driver function for everything
# initializations, calling other functions
import interfaces
import routines
import constants
import analysis
import events
import RPI.GPIO as GPIO
import time


def test():
    initialize_components()
    analysis.write_json(analysis.DATA_PATH+'calibration_data.json', 
                        constants.calibrated_pH)
    while True:
        print(interfaces.read_temperature())
        time.sleep(constants.SLEEP_TIME)


def start():
    # Default program
    # initialize components
    initialize_components()
    # While loop to continuously prompt user?
    # output prompt to LCD screen
    interfaces.display_list(constants.ROUTINE_OPTIONS)
    # wait for user input to select which routine (polling should be fine here)
    routine_selection = interfaces.read_user_input(['1','2','3'])
    routines.run_routine(routine_selection)


def initialize_components():
    """Function to initialize components"""
    # Should this go under interfaces?
    # GPIO.add_event_detect(constants.KEY_0, GPIO.RISING, events.handle)

    interfaces.setup_interfaces()
    # TODO load saved constants, such as calibration values


if __name__ == "__main__":
    test()
