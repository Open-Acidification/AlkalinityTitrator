import interfaces
import routines
import constants
import analysis
import time
import sys       # exception info
import traceback # exception info


def test():
    """Function for running specific tests for the program"""
    initialize_components()
    while True:
        temp, res = interfaces.read_temperature()
        pH_reading, pH_volts = interfaces.read_pH()
        print('Temperature: {0:0.3f}C'.format(temp))
        print('Resistance: {0:0.3f} Ohms'.format(res))
        interfaces.lcd_out("pH: {}".format(pH_reading))
        interfaces.lcd_out("pH volt: {}".format(pH_volts))
        time.sleep(constants.TITRATION_WAIT_TIME)


def run():
    """Main driver for the program. Initializes components and queries the user for next steps"""
    # initialize components
    initialize_components()
    # output prompt to LCD screen
    routine_selection = '0'
    #options = [str(key) for key in constants.ROUTINE_OPTIONS]
    page = 1
    while routine_selection != '6':
        if (routine_selection is constants.KEY_STAR):
            if (page is 1):
                page = 2
            else:
                page = 1
        if (page is 1):
            interfaces.display_list(constants.ROUTINE_OPTIONS_1)
        else:
            interfaces.display_list(constants.ROUTINE_OPTIONS_2)
            
        # wait for user input to select which routine (polling should be fine here)
        routine_selection = interfaces.read_user_input()
        routines.run_routine(routine_selection)


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
    interfaces.setup_interfaces()


if __name__ == "__main__":
    try:
        run()
    except:
        # Deactivate the SSR if any crash occurs
        interfaces.tempcontroller.deactivate()
        print("\nDeactivated SSR")
        
        print(sys.exc_info()[0])
        traceback.print_exc()
        
