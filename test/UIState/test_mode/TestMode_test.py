from unittest import mock
from titration.utils.titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.test_mode.TestMode import TestMode

# Test handleKey
@mock.patch.object(TestMode, "_setNextState")
def test_handleKey(mock):
    testMode = TestMode(Titrator(), Titrator())

    testMode.handleKey(1)
    assert mock.called
    mock.reset_called()

    testMode.handleKey(2)
    assert mock.called
    mock.reset_called()

    testMode.handleKey(3)
    assert mock.called
    mock.reset_called()

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.handleKey(4)
    assert mock.called
    mock.reset_called()

    testMode.handleKey(5)
    assert mock.called
    mock.reset_called()

    testMode.handleKey(6)
    assert mock.called
    mock.reset_called()

    testMode.handleKey('*')
    assert(testMode.subState == 1)

# Test loop
@mock.patch.object(LCD, "display_list")
def test_loop(mock):
    testMode = TestMode(Titrator(), Titrator())

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.subState += 1

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_2)

# Test TestMode
@mock.patch.object(LCD, "display_list")
def test_TestMode(mock):
    testMode = TestMode(Titrator(), Titrator())

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey(1)
    assert mock.called
    mock.reset_called()

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey(2)
    assert mock.called
    mock.reset_called()
    
    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey(3)
    assert mock.called
    mock.reset_called()

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_2)

    testMode.handleKey(4)
    assert mock.called
    mock.reset_called()

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_2)

    testMode.handleKey(5)
    assert mock.called
    mock.reset_called()
    
    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_2)
