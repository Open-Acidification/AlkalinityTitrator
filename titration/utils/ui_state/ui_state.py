class UIState:
    def __init__(self, titrator):
        self.titrator = titrator

    def handleKey(self, key):
        raise Exception(self.titrator.state.name() + " requires a handleKey function")

    def name(self):
        raise Exception(self.titrator.state.name() + " requires a name function")

    def loop(self):
        raise Exception(self.titrator.state.name() + " requires a loop function")

    def start(self):
        pass

    def _setNextState(self, state, update):
        self.titrator.setNextState(state, update)
