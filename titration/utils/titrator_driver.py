from titration.utils import titrator

titrator_object = titrator.Titrator()


def run():
    while True:
        titrator_object.loop()
