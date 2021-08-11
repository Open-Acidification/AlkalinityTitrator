import sys  # exception info
import traceback  # exception info

import analysis
import constants

# Parse opcodes for testing mode
# Must be checked before "import interfaces"
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
if opts:
    if "-test" in opts:
        print("Starting in Test Mode")
        constants.IS_TEST = True
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} (-test)")

import interfaces
import routines


def test():
    """Function for running specific tests for the program"""
    initialize_components()
    while True:
        temp, res = interfaces.read_temperature()
        pH_reading, pH_volts = interfaces.read_pH()
        print("Temperature: {0:0.3f}C".format(temp))
        print("Resistance: {0:0.3f} Ohms".format(res))
        interfaces.lcd_out("pH: {}".format(pH_reading))
        interfaces.lcd_out("pH volt: {}".format(pH_volts))
        interfaces.delay(constants.TITRATION_WAIT_TIME)


def run():
    """Main driver for the program. Initializes components and queries the user for next steps"""
    # initialize components
    initialize_components()
    # routines.auto_home()
    # output prompt to LCD screen
    routine_selection = "0"

    page = 1
    while routine_selection != "6" or routine_selection != constants.KEY_6:
        if routine_selection is constants.KEY_STAR:
            if page == 1:
                page = 2
            else:
                page = 1
        if page == 1:
            interfaces.display_list(constants.ROUTINE_OPTIONS_1)
        else:
            interfaces.display_list(constants.ROUTINE_OPTIONS_2)

        # wait for user input to select which routine (polling should be fine here)
        routine_selection = interfaces.read_user_input()
        routines.run_routine(routine_selection)

    analysis.save_calibration_data()
    interfaces.tempcontroller.deactivate()
    interfaces.lcd_clear()
    interfaces.ui_lcd.lcd_backlight(False)


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
    interfaces.setup_interfaces()


if __name__ == "__main__":
    try:
        run()
    except:
        # Deactivate the SSR if any crash occurs
        if interfaces.tempcontroller is not None:
            interfaces.tempcontroller.deactivate()
        print("\nDeactivated SSR")

        print(sys.exc_info()[0])
        traceback.print_exc()
