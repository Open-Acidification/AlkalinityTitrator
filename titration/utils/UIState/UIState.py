class UIState:
    def __init__(self, titrator):
        self.titrator = titrator

    def handleKey(self, key):
        pass

    def name(self):
        pass

    def loop(self):
        pass

    def start(self):
        pass

    def _setNextState(self, state, update):
        self.titrator.setNextState(state, update)
