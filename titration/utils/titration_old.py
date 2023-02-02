import sys
import traceback

from titration.utils import analysis, constants, interfaces, routines

# The old driver function for the alkalinity titrator. Does implement the UI state machine that has since been created.


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
                interfaces.lcd.display_list(constants.ROUTINE_OPTIONS_1)
            else:
                interfaces.lcd.display_list(constants.ROUTINE_OPTIONS_2)

            # wait for user input to select which routine (polling should be fine here)
            routine_selection = interfaces.read_user_input()
            routines.run_routine(routine_selection)

        analysis.save_calibration_data()
        interfaces.temperature_controller.deactivate()
        interfaces.lcd.clear()
        interfaces.lcd.lcd_backlight(False)
    except (BaseException, Exception):
        # Deactivate the SSR if any crash occurs
        if interfaces.temperature_controller is not None:
            interfaces.temperature_controller.deactivate()
        print("\n************************\nDeactivated SSR\n************************\n")

        try:
            interfaces.lcd.clear()
        except BaseException:
            pass
        try:
            interfaces.lcd.print("Deactivated SSR", 1)
        except BaseException:
            pass

        # Attempt to save calibration data, this will save syringe position
        # and any recent calibrations
        try:
            analysis.save_calibration_data()
            print(
                "\n************************\nCalibration Saved\n************************\n"
            )
            try:
                interfaces.lcd.print("Calibration Saved", 2)
            except Exception:
                pass
        except Exception:
            print(
                "\n!!!!!!!!!!!!!!!!!!!!!!!!\nUnable to save calibration data\n!!!!!!!!!!!!!!!!!!!!!!!!\n"
            )
            try:
                interfaces.lcd.print("Calibration UNSAVED", 2)
            except Exception:
                pass
        print(sys.exc_info()[0])
        traceback.print_exc()


def initialize_components():
    """Initializes external interfaces and saved calibration data"""
    analysis.setup_calibration()
