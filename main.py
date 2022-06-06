# import os
import sys

import titration.utils.constants as constants

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    if opts:
        if "-old" in opts:
            if "-dev" in opts:
                constants.IS_TEST = True
                import titration.utils.titration_old as titration_old
                titration_old.run()
            else:
                constants.IS_TEST = False
                import titration.utils.titration_old as titration_old
                titration_old.run()
        elif "-dev" in opts:
            constants.IS_TEST = True
            import titration.utils.titrator_driver as titrator_driver
            titrator_driver.run()
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} [-test | -dev]")
    else:
        constants.IS_TEST = False
        import titration.utils.titrator_driver as titrator_driver
        titrator_driver.run()
