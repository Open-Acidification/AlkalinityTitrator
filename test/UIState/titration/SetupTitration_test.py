import pytest
from unittest import mock
from titration.utils.UIState.titration.SetupTitration import SetupTitration
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

# Test handleKey
@mock.patch.object(SetupTitration, "_setNextState")
def test_handleKey(mock):
    setupTitration = SetupTitration(Titrator())

    key_input = 1
    setupTitration.handleKey(key_input)
    assert not mock.called
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert not mock.called
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert mock.called
    mock.reset_mock()

# Test loop
@mock.patch.object(interfaces, "read_user_value")
def test_loop(mock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert mock.called
    mock.reset_mock()

    setupTitration.subState += 1
    setupTitration.loop()
    assert mock.called


@mock.patch.object(interfaces, "lcd_clear")
def test_loop(mock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.subState += 2
    setupTitration.loop()
    assert mock.called
