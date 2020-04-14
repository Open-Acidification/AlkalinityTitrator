# Main driver function for everything
# initializations, calling other functions
import interfaces
import routines
import constants
import events
import RPI.GPIO as GPIO


def start():
    # Default program
    # initialize components
    initialize_components()
    # While loop to continuously prompt user?
    # output prompt to LCD screen
    interfaces.display_list(constants.ROUTINE_OPTIONS)
    # wait for user input to select which routine (polling should be fine here)
    routine_selection = interfaces.read_user_input()
    routines.select_routine(routine_selection)


def initialize_components():
    """Function to initialize components"""
    # Should this go under interfaces?
    GPIO.add_event_detect(constants.KEY_0, GPIO.RISING, events.handle)
