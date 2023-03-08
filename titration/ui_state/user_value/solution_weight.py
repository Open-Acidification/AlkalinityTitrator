"""
The file for the SolutionWeight class
"""
from titration.ui_state.user_value.user_value import UserValue


class SolutionWeight(UserValue):
    """
    This is a class for the SolutionWeight state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's solution weight
        """
        self.titrator.solution_weight = float(value)

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Sol. weight (g):"
