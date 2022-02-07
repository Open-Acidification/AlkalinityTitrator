import pytest
from io import StringIO
from titration.utils.Titrator import Titrator

loop_inputs = StringIO('A\n')

def test_loop(monkeypatch):
    monkeypatch.setattr('sys.stdin', loop_inputs)
    Titrator().loop()
