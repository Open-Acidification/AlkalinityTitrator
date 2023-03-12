"""
The file to run the program
"""
import sys

from titration import constants

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    if opts:
        if "-sim" in opts:
            constants.IS_TEST = True
            constants.GUI_ENABLED = True

            from titration.gui import GUI

            gui = GUI()

        elif "-con" in opts:
            constants.IS_TEST = True
            constants.GUI_ENABLED = False

            from titration import titrator_driver

            titrator_driver.run()
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} [-test | -dev]")
    else:
        constants.IS_TEST = False
        constants.GUI_ENABLED = False
        from titration import titrator_driver

        titrator_driver.run()
