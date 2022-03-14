from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState import MainMenu

class AutomaticTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('AutomaticTitration', titrator)
        self.titrator = titrator
        self.values = {'pH_target' : 5, 'current_pH' : 5}
        self.subState = 1
    
    def name(self):
        return 'AutomaticTitration'

    def handleKey(self, key):
        # Substate 4 key handle
        if self.subState == 4:
            if key == 0 or key == constants.KEY_0:
                self._setNextState(MainMenu.MainMenu(self.titrator), True)
                pass
            elif key == 1 or key == constants.KEY_1:
                quit()


    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            interfaces.lcd_out(
                "Titrating to {} pH".format(str(self.values['pH_target'])),   # TODO: Change pH_target
                style=constants.LCD_CENT_JUST,
                line=4
            )
            self.subState += 1
        
        # Substate 2 output
        elif self.subState == 2:
            interfaces.lcd_out("Mixing...", style=constants.LCD_CENT_JUST, line=4)
            self.subState += 1
        
        # Substate 3 output
        elif self.subState == 3:
            interfaces.lcd_out("pH value {} reached".format(self.values['current_pH']), line=4) # TODO: Change current_pH
            self.subState += 1
        
        # Substate 4 output
        elif self.subState == 4:
            interfaces.lcd_clear()
            interfaces.lcd_out("Return to", line=1)
            interfaces.lcd_out("main menu: 0", line=2)
            interfaces.lcd_out("Exit: 1", line=3)


    def start(self):
        interfaces.lcd_out("AUTO SELECTED", style=constants.LCD_CENT_JUST, line=4)

