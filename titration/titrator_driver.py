"""
The file for the Alkalinity Titrator driver
"""
import threading

from titration import constants
from titration.gui import GUI
from titration.titrator import Titrator


def run():
    """
    The function that drives sets up threading for the Titrator and GUI
    """
    titrator = Titrator()

    if constants.IS_TEST:
        thread = threading.Thread(target=run_gui, args=[titrator], daemon=True)
        thread.start()

    while True:
        titrator.loop()


def run_gui(titrator):
    """
    The function that drives the Alkalinity Titrator's GUI
    """
    GUI(titrator)
