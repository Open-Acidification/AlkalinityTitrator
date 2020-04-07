# Main driver function for everything
# initializations, calling other functions
import interfaces
import constants


def start():
    # PROGRAM FLOW
    # output prompt to LCD screen
    interfaces.lcd_out(constants.SELECT_PROGRAM)
    # wait for user input to select which routine (polling should be fine here)
    


def initialize_components():
    """Function to initialize components"""
    # Should this go under interfaces?