"""
The file to test the Titrator class
"""
from unittest import mock
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.titration.setup_titration import SetupTitration
from titration.utils.titrator import Titrator
from titration.utils.devices.keypad_mock import Keypad


@mock.patch.object(Titrator, "_handle_ui")
def test_loop(handle_ui_mock):
    """
    The function to test function calls of the loop function
    """
    titrator = Titrator()

    titrator.loop()
    handle_ui_mock.assert_called()


@mock.patch.object(Titrator, "_update_state")
def test_set_next_state_true(update_state_mock):
    """
    The function to test the set_next_state function with update parameter set to True
    """
    titrator = Titrator()

    temp = MainMenu(titrator)
    assert titrator.next_state is None
    titrator.set_next_state(temp, True)
    assert titrator.next_state == temp
    update_state_mock.assert_called()


@mock.patch.object(Titrator, "_update_state")
def test_set_next_state_false(update_state_mock):
    """
    The function to test the set_next_state function with update parameter set to False
    """
    titrator = Titrator()

    temp = MainMenu(titrator)
    assert titrator.next_state is None
    titrator.set_next_state(temp, False)
    assert titrator.next_state == temp
    update_state_mock.assert_not_called()


@mock.patch.object(SetupTitration, "start")
def test_update_state_without_next_state(start_mock):
    """
    The function to test the start function when the titrator does not have a next_state
    """
    titrator = Titrator()

    assert titrator.next_state is None
    titrator._update_state()
    start_mock.assert_not_called()


@mock.patch.object(SetupTitration, "start")
def test_update_state_with_next_state(start_mock):
    """
    The function to test the start function when the titrator has a next_state
    """
    titrator = Titrator()

    temp = SetupTitration(titrator)
    titrator.next_state = temp
    assert titrator.state != titrator.next_state
    titrator._update_state()
    assert titrator.state == temp
    assert titrator.next_state is None
    start_mock.assert_called()


@mock.patch.object(Keypad, "keypad_poll")
@mock.patch.object(Titrator, "_update_state")
@mock.patch.object(MainMenu, "handle_key")
@mock.patch.object(MainMenu, "loop")
def test_handle_ui(keypad_poll_mock, update_state_mock, handle_key_mock, loop_mock):
    """
    The function to test function calls of the handle_ui function
    """
    titrator = Titrator()

    titrator._handle_ui()
    keypad_poll_mock.assert_called()
    handle_key_mock.assert_called()
    update_state_mock.assert_called()
    loop_mock.assert_called()
