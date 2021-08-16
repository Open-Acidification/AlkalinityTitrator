import traceback  # exception info
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from . import analysis
from . import constants

# Parse opcodes for testing mode
# Must be checked before "import interfaces"
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
if opts:
    if "-test" in opts:
        print("Starting in Test Mode")
        constants.IS_TEST = True
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} (-test)")

from . import interfaces  # noqa: E402
from . import routines  # noqa: E402


def test():
    """Function for running specific tests for the program"""
    initialize_components()
    while True:
        temperature, res = interfaces.read_temperature()
        pH_reading, pH_volts = interfaces.read_pH()
        interfaces.lcd_out(
            "Temperature: {0:0.3f}C".format(temperature),
            1,
            style=constants.LCD_CENT_JUST,
        )
        interfaces.lcd_out(
            "Resistance: {0:0.3f} Ohms".format(res), 2, style=constants.LCD_CENT_JUST
        )
        interfaces.lcd_out(
            "pH: {}".format(pH_reading), 3, style=constants.LCD_CENT_JUST
        )
        interfaces.lcd_out(
            "pH volt: {}".format(pH_volts), 4, style=constants.LCD_CENT_JUST
        )
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
    interfaces.temperature_controller.deactivate()
    interfaces.lcd_clear()
    interfaces.ui_lcd.lcd_backlight(False)


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
    interfaces.setup_interfaces()


if __name__ == "__main__":
    try:
        run()
    except Exception:
        # Deactivate the SSR if any crash occurs
        if interfaces.temperature_controller is not None:
            interfaces.temperature_controller.deactivate()
        print("\nDeactivated SSR")

        print(sys.exc_info()[0])
        traceback.print_exc()
