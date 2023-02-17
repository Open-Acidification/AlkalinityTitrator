"""
The file for the Alkalinity Titrator driver
"""
from titration.titrator import Titrator

titrator = Titrator()


def run():
    """
    The function that drives the Alkalinity Titrator
    """
    while True:
        titrator.loop()
