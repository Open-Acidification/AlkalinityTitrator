"""
The file for the Alkalinity Titrator driver
"""
import threading

from titration import constants
from titration.gui import GUI
from titration.titrator import Titrator

titrator = None

gui = GUI()

def run():
    """
    The function that drives sets up threading for the Titrator and GUI
    """
    # This needs to be switch to a gui enable flag
    if constants.GUI_ENABLED:
        thread = threading.Thread(target=run_gui, daemon=True)
        thread.start()

        titrator = Titrator(gui.root)

    else:

        titrator = Titrator()
    
    while True:
        titrator.loop()

def run_gui():
    """
    The function that drives the Alkalinity Titrator's GUI
    """
    # Run the GUI loop
    gui.root.mainloop()
