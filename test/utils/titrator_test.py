from unittest import mock
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.titration.setup_titration import SetupTitration
from titration.utils.titrator import Titrator
from titration.utils.devices.keypad_mock import Keypad


# Test loop
@mock.patch.object(Titrator, "_handleUI")
def test_loop(handleUIMock):
    titrator = Titrator()

    titrator.loop()
    handleUIMock.assert_called()
    handleUIMock.reset_mock()


# Test setNextState
@mock.patch.object(Titrator, "_updateState")
def test_setNextState(updateStateMock):
    titrator1 = Titrator()

    temp = MainMenu(titrator1)
    assert titrator1.nextState is None
    titrator1.setNextState(temp, True)
    assert titrator1.nextState == temp
    updateStateMock.assert_called()
    updateStateMock.reset_mock()

    titrator2 = Titrator()

    temp = MainMenu(titrator2)
    assert titrator2.nextState is None
    titrator2.setNextState(temp, False)
    assert titrator2.nextState == temp
    updateStateMock.assert_not_called()
    updateStateMock.reset_mock()


# Test _updateState
@mock.patch.object(SetupTitration, "start")
def test_updateState(startMock):
    titrator = Titrator()

    assert titrator.nextState is None
    titrator._updateState()
    startMock.assert_not_called()
    startMock.reset_mock()

    temp = SetupTitration(titrator)
    titrator.nextState = temp
    assert titrator.state != titrator.nextState
    titrator._updateState()
    assert titrator.state == temp
    assert titrator.nextState is None
    startMock.assert_called()


# Test _handleUI
@mock.patch.object(Keypad, "get_key")
@mock.patch.object(Titrator, "_updateState")
@mock.patch.object(MainMenu, "handleKey")
@mock.patch.object(MainMenu, "loop")
def test_handleUI(getKeyMock, updateStateMock, handleKeyMock, loopMock):
    titrator = Titrator()

    titrator._handleUI()
    getKeyMock.assert_called()
    getKeyMock.reset_mock()

    handleKeyMock.assert_called()
    handleKeyMock.reset_mock()

    updateStateMock.assert_called()
    updateStateMock.reset_mock()

    loopMock.assert_called()
    loopMock.reset_mock()
