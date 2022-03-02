from mimetypes import init
import pytest
from unittest import mock
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(AutomaticTitration, "_setNextState")
def test_handleKey(mock):
    pass

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop1(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    assert mock.called
    mock.reset_mock()

    initialTitration.loop()
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_clear")
def test_loop2(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    initialTitration.loop()
    initialTitration.loop()
    assert mock.called

# Test start
@mock.patch.object(interfaces, "lcd_out")
def test_start(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.start()
    assert mock.called
