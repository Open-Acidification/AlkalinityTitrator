import sys
import traceback

from titration.utils import analysis, constants, interfaces, routines


def run():
    """Main driver for the program. Initializes components and queries the user for next steps"""

    try:
        # initialize components
        initialize_components()
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
    except Exception:
        # Deactivate the SSR if any crash occurs
        if interfaces.temperature_controller is not None:
            interfaces.temperature_controller.deactivate()
        print("\n************************\nDeactivated SSR\n************************")

        #print(sys.exc_info()[0])
        #traceback.print_exc()


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
    interfaces.setup_interfaces()
