import interfaces
import routines
import constants
import analysis


def test():
    """Function for running specific tests for the program"""
    initialize_components()
    analysis.write_json('calibration_data.json', constants.calibration_data)
    while True:
        temp, res = interfaces.read_temperature()
        print('Temperature: {0:0.3f}C'.format(temp))
        print('Resistance: {0:0.3f} Ohms'.format(res))
        # time.sleep(constants.TITRATION_WAIT_TIME)


def run():
    """Main driver for the program. Initializes components and queries the user for next steps"""
    # initialize components
    initialize_components()
    # output prompt to LCD screen
    routine_selection = '0'
    while routine_selection != '5':
        interfaces.display_list(constants.ROUTINE_OPTIONS)
        # wait for user input to select which routine (polling should be fine here)
        routine_selection = interfaces.read_user_input(['1', '2', '3', '4', '5'])
        routines.run_routine(routine_selection)


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
    interfaces.setup_interfaces()


if __name__ == "__main__":
    run()
