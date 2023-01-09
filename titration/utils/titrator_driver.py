from titration.utils import Titrator

titrator_object = Titrator.Titrator()


def run():
    while True:
        titrator_object.loop()
