"""
The file for the UIState class
"""

# pylint: disable = W0107


class UIState(object):
    """
    The UIState class is the model for all UI states

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def __init__(self, titrator, previous_state=None):
        """
        The constructor for the UIState class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        self.titrator = titrator
        self.previous_state = previous_state
        self.substate = 1

    def handle_key(self, key):
        """
        The function to respond to a keypad input

        Parameters:
            key (char): the keypad input to be processed

        Returns:
            exception: if the handle_key function is not implemented in the derived state
        """
        raise Exception(self.name() + " requires a handle_key function")

    def name(self):
        """
        The function to return the name of the state

        Returns:
            string: the name of the state
        """
        return self.__class__.__name__

    def loop(self):
        """
        The function to loop through the state until a keypad press or external event

        Returns:
            exception: if the loop function is not implemented in the derived state
        """
        raise Exception(self.name() + " requires a loop function")

    def start(self):
        """
        Optional function that is called upon entering a new state
        """
        pass

    def _set_next_state(self, state, update):
        """
        The function to set the next state to go to

        Parameters:
            state (UIState object): the state that will be entered next
            update (bool): update is used to either immediately update or wait
        """
        self.titrator.set_next_state(state, update)
