"""
The file to run the program
"""
import sys

from AlkalinityTitrator.titration.utils import constants

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    if opts:
        if "-dev" in opts:
            constants.IS_TEST = True
            from AlkalinityTitrator.titration.utils import titrator_driver

            titrator_driver.run()
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} [-test | -dev]")
    else:
        constants.IS_TEST = False
        from AlkalinityTitrator.titration.utils import titrator_driver

        titrator_driver.run()
