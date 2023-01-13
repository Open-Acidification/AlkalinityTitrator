from titration.utils.titrator import Titrator

titrator = Titrator()


def run():
    while True:
        titrator.loop()
