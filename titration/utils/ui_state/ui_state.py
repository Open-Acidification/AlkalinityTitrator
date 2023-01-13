class UIState:
    def __init__(self, titrator, previousState=None):
        self.titrator = titrator
        self.previousState = previousState
        self.subState = 1

    def handleKey(self, key):
        raise Exception(self.__class__.__name__ + " requires a handleKey function")

    def name(self):
        return self.__class__.__name__

    def loop(self):
        raise Exception(self.__class__.__name__ + " requires a loop function")

    def start(self):
        pass

    def _setNextState(self, state, update):
        self.titrator.setNextState(state, update)
