class UIState:
    def __init__(self, titrator):
        self.titrator = titrator

    def handleKey(self, key):
        raise Exception("A handleKey function is missing")

    def name(self):
        raise Exception("A name function is missing")

    def loop(self):
        raise Exception("A loop function is missing")

    def start(self):
        pass

    def _setNextState(self, state, update):
        self.titrator.setNextState(state, update)
