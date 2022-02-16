from titration.utils.UIState import UIState
from titration.utils import interfaces, constants


class ManualTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('ManualTitration', titrator)
        self.titrator = titrator
        self.values = {
            'p_volume' : 0, 'p_direction' : 0, 
            'user_choice' : 0, 'degas_time' : 0,
            'current_pH' : 5
        }
        self.subState = 1

    def name(self):
        return 'ManualTitration'

    def handleKey(self, key):
        if self.subState == 1:
            self.values['p_direction'] = key
            self.subState += 1

        elif self.subState == 2:
            if key == '1' or key == constants.KEY_1:
                self.subState -= 1
            else:
                self.subState += 1
        
        elif self.subState == 3:
            self.values['user_choice'] = key
            self.subState += 1

    def loop(self):
        if self.subState == 1:
            self.values['p_volume'] = interfaces.read_user_value("Volume: ")
            interfaces.lcd_clear()
            interfaces.lcd_out("Direction (0/1): ", line=1)
        
        elif self.subState == 2:
            interfaces.lcd_out("Current pH: {0:>4.5f}".format(self.values['current_pH']), line=1) # TODO: change current pH value from 5
            interfaces.lcd_out("Add more HCl?", line=2)
            interfaces.lcd_out("(0 - No, 1 - Yes)", line=3)
            interfaces.lcd_out("", line=4)
        
        elif self.subState == 3:
            interfaces.lcd_clear()
            interfaces.lcd_out("Current pH: {0:>4.5f}".format(self.values['current_pH']), line=1) # TODO: change current pH value from 5
            interfaces.lcd_out("Degas?", 1)
            interfaces.lcd_out("(0 - No, 1 - Yes)", line=2)
        
        elif self.subState == 4:
            if self.values['user_choice'] == constants.KEY_1:
                self.values['degas_time'] = interfaces.read_user_value("Degas time (s):")
            # TODO: next state


    def start(self):
        interfaces.lcd_out("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)

