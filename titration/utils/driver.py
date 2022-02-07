from titration.utils import Titrator

def run():
    titrator = Titrator.Titrator()
    while True:
        titrator.loop()