from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState import MainMenu


class ManualTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('ManualTitration', titrator)
        self.titrator = titrator
        self.values = {
            'p_volume' : 0, 'p_direction' : 0, 
            'degas_time' : 0, 'current_pH' : 5
        }
        self.subState = 1

    def name(self):
        return 'ManualTitration'

    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            self.values['p_direction'] = key
            self.subState += 1

        # Substate 2 key handle
        elif self.subState == 2:
            if key == 1 or key == constants.KEY_1:
                self.subState -= 1
            else:
                self.subState += 1
        
        # Substate 3 key handle
        elif self.subState == 3:
            if key == 0 or key == constants.KEY_0:
                self.subState += 2
            elif key == 1 or key == constants.KEY_1:
                self.subState += 1

        # Substate 4 key handle
        elif self.subState == 4:
            self.subState += 1

        # Substate 5 key handle
        elif self.subState == 5:
            if key == 0 or key == constants.KEY_0:
                self._setNextState(MainMenu.MainMenu(self.titrator), True)
                pass
            elif key == 1 or key == constants.KEY_1:
                quit()

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            self.values['p_volume'] = interfaces.read_user_value("Volume: ")
            interfaces.lcd_clear()
            interfaces.lcd_out("Direction (0/1): ", line=1)
        
        # Substate 2 output
        elif self.subState == 2:
            interfaces.lcd_out("Current pH: {0:>4.5f}".format(self.values['current_pH']), line=1)   # TODO: change current pH value from 5
            interfaces.lcd_out("Add more HCl?", line=2)
            interfaces.lcd_out("(0 - No, 1 - Yes)", line=3)
            interfaces.lcd_out("", line=4)
        
        # Substate 3 output
        elif self.subState == 3:
            interfaces.lcd_clear()
            interfaces.lcd_out("Current pH: {0:>4.5f}".format(self.values['current_pH']), line=1)   # TODO: change current pH value from 5
            interfaces.lcd_out("Degas?", 1)
            interfaces.lcd_out("(0 - No, 1 - Yes)", line=2)
        
        # Substate 4 output
        elif self.subState == 4:
            self.values['degas_time'] = interfaces.read_user_value("Degas time (s):")

        # Substate 5 output
        elif self.subState == 5:
            interfaces.lcd_clear()
            interfaces.lcd_out("Return to", line=1)
            interfaces.lcd_out("main menu: 0", line=2)
            interfaces.lcd_out("Exit: 1", line=3)

    def start(self):
        interfaces.lcd_out("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)

