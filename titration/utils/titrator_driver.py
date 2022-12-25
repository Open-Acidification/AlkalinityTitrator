from titration.utils import titrator

titrator = titrator.Titrator()


def run():
    while True:
        titrator.loop()
