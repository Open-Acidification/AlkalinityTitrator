"""
The file to run the program
"""
import sys

from titration import mock_config

if __name__ == "__main__":
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    if opts:
        if "-gui" in opts:
            mock_config.MOCK_ENABLED = True
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} [-gui]")

    from titration import titrator_driver

    titrator_driver.run()
