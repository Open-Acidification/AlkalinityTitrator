"""
The file for the SolutionSalinity class
"""
from titration.ui_state.user_value.user_value import UserValue


class SolutionSalinity(UserValue):
    """
    This is a class for the SolutionSalinity state of the titrator
    """

    def save_value(self):
        """
        The function to save the titrator's solution salinity
        """
        self.titrator.solution_salinity = self.value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Sol. salinity (ppt):"
