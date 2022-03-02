import pytest
from unittest import mock
from titration.utils.UIState.titration.InitialTitration import InitialTitration
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

# Test handleKey
@mock.patch.object(InitialTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = InitialTitration(Titrator())

    key_input = 'a'
    initialTitration.handleKey(key_input)
    assert(initialTitration.value == 'a')

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop1(mock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    assert mock.called

# Test loop
@mock.patch.object(InitialTitration, "_setNextState")
def test_loop2(mock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey(1)
    initialTitration.loop()
    assert mock.called
