import pytest
from unittest import mock
from titration.utils.UIState.titration.ManualTitration import ManualTitration
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(ManualTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = ManualTitration(Titrator())

    initialTitration.handleKey(5)
    assert(initialTitration.values['p_direction'] == 5)

    initialTitration.handleKey(1)
    assert(initialTitration.subState == 1)

    initialTitration.handleKey(6)
    assert(initialTitration.values['p_direction'] == 6)

    initialTitration.handleKey(2)
    assert(initialTitration.subState == 3)

    initialTitration.handleKey(5)
    assert(initialTitration.values['user_choice'] == 5)
    assert(initialTitration.subState == 4)

# Test loop
@mock.patch.object(interfaces, "read_user_value")
def test_loop1(mock):
    initialTitration = ManualTitration(Titrator())

    initialTitration.loop()
    mock.assert_called_with('Volume: ')

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop2(mock):
    initialTitration = ManualTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.loop()
    mock.assert_called_with("", line=4)

# Test loop
@mock.patch.object(interfaces, "lcd_clear")
def test_loop3(mock):
    initialTitration = ManualTitration(Titrator())

    initialTitration.subState += 2
    initialTitration.loop()
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value")
def test_loop4(mock):
    initialTitration = ManualTitration(Titrator())

    initialTitration.subState += 3
    initialTitration.values['user_choice'] = 1
    initialTitration.loop()
    mock.assert_called_with("Degas time (s):")
