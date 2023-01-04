from titration.utils import Titrator

titrator = Titrator.Titrator()


def run():
    while True:
        titrator.loop()
