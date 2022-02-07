# import os
import sys

import titration.utils.constants as constants

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    if opts:
        if "-test" in opts:
            print("Starting in Test Mode")
            constants.IS_TEST = True
        elif "-dev" in opts:
            constants.IS_TEST = True
            import titration.utils.driver as driver
            driver.run()
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-test)")
    else:
        constants.IS_TEST = False
    import titration.utils.titration as titration
    titration.run()
