"""
The file to test the DemoPump Class
"""

# pylint: disable = redefined-builtin, too-many-statements

from unittest import mock
from unittest.mock import ANY

from titration.devices.library import LiquidCrystal, SyringePump
from titration.titrator import Titrator
from titration.ui_state.demo_mode.demo_mode_menu import DemoModeMenu
from titration.ui_state.demo_mode.demo_pump import DemoPump


@mock.patch.object(SyringePump, "pump_out")
@mock.patch.object(SyringePump, "pump_in")
@mock.patch.object(SyringePump, "empty")
@mock.patch.object(SyringePump, "fill")
@mock.patch.object(DemoPump, "_set_next_state")
def test_handle_key(_set_next_state, fill, empty, pump_in, pump_out):
    """
    The function to test the DemoPump's handle_key function for each keypad input
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.handle_key("1")
    assert demo_pump.substate == 4

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.handle_key("2")
    assert demo_pump.substate == 5

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.handle_key("3")
    assert demo_pump.substate == 6

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.handle_key("4")
    assert demo_pump.substate == 2

    demo_pump.handle_key("1")
    assert demo_pump.substate == 7
    fill.assert_called()

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.handle_key("2")
    assert demo_pump.substate == 8
    empty.assert_called()

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.handle_key("3")
    assert demo_pump.substate == 9
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "PumpVolume"
    pump_in.assert_called_with(0)

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.handle_key("4")
    assert demo_pump.substate == 3

    demo_pump.handle_key("1")
    assert demo_pump.substate == 10
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "PumpVolume"
    pump_out.assert_called_with(0)

    demo_pump.handle_key("1")
    assert demo_pump.substate == 3

    demo_pump.handle_key("4")
    assert demo_pump.substate == 1

    demo_pump.handle_key("D")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "DemoModeMenu"


@mock.patch.object(LiquidCrystal, "print")
def test_loop(print):
    """
    The function to test 's loop function's LiquidCrystal calls
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.substate = 2
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Fill Pump", line=1),
            mock.call("2: Empty Pump", line=2),
            mock.call("3: Pump In", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    demo_pump.substate = 3
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Pump Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.substate = 4
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pump Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_pump_volume()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 5
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Added Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_added_volume()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 6
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Cleared", line=1, style="center"),
            mock.call(
                "Added Volume",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 7
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 8
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Emptying Pump", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 9
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pumping Volume In", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.substate = 10
    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pumping Volume Out", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(SyringePump, "pump_out")
@mock.patch.object(SyringePump, "pump_in")
@mock.patch.object(SyringePump, "empty")
@mock.patch.object(SyringePump, "fill")
@mock.patch.object(DemoPump, "_set_next_state")
@mock.patch.object(LiquidCrystal, "print")
def test_demo_mode(print, _set_next_state, fill, empty, pump_in, pump_out):
    """
    The function to test a use case of the  class:
        User enters "1" to Get Pump Volume
        User enters "1" to return to demo pump menu
        User enters "2" to Get Added Volume
        User enters "1" to return to demo pump menu
        User enters "3" to Clear Added Volume
        User enters "1" to return to demo pump menu
        User enters "4" to go to 2nd page of options
        User enters "1" to Fill Pump
        User enters "1" to return to demo pump menu
        User enters "2" to Empty Pump
        User enters "1" to return to demo pump menu
        User enters "3" to Pump In liquid
        User enters "1" to return to demo pump menu
        User enters "4" to go to 3rd page of options
        User enters "1" to Pump Out liquid
        User enters "1" to return to demo pump menu
        User enters "4" to go to 1st page of options
        User enters "D" to return to Demo Menu
    """
    demo_pump = DemoPump(Titrator(), DemoModeMenu(Titrator()))

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 4

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pump Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_pump_volume()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("2")
    assert demo_pump.substate == 5

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Added Volume:", line=1),
            mock.call(
                f"{demo_pump.titrator.pump.get_added_volume()} ml",
                line=2,
                style="center",
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("3")
    assert demo_pump.substate == 6

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Cleared", line=1, style="center"),
            mock.call(
                "Added Volume",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("4")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Fill Pump", line=1),
            mock.call("2: Empty Pump", line=2),
            mock.call("3: Pump In", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 7
    fill.assert_called()

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Filling Pump", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Fill Pump", line=1),
            mock.call("2: Empty Pump", line=2),
            mock.call("3: Pump In", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    demo_pump.handle_key("2")
    assert demo_pump.substate == 8
    empty.assert_called()

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Emptying Pump", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Fill Pump", line=1),
            mock.call("2: Empty Pump", line=2),
            mock.call("3: Pump In", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    demo_pump.handle_key("3")
    assert demo_pump.substate == 9
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "PumpVolume"
    pump_in.assert_called_with(0)

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pumping Volume In", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 2

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Fill Pump", line=1),
            mock.call("2: Empty Pump", line=2),
            mock.call("3: Pump In", line=3),
            mock.call("4: Page 3", line=4),
        ]
    )

    demo_pump.handle_key("4")
    assert demo_pump.substate == 3

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Pump Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 10
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "PumpVolume"
    pump_out.assert_called_with(0)

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("Pumping Volume Out", line=1),
            mock.call(
                "",
                line=2,
            ),
            mock.call("Press any to cont.", line=3),
            mock.call("", line=4),
        ]
    )

    demo_pump.handle_key("1")
    assert demo_pump.substate == 3

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Pump Out", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("4: Page 1", line=4),
        ]
    )

    demo_pump.handle_key("4")
    assert demo_pump.substate == 1

    demo_pump.loop()
    print.assert_has_calls(
        [
            mock.call("1: Get Volume", line=1),
            mock.call("2: Set Volume", line=2),
            mock.call("3: Zero Added Volume", line=3),
            mock.call("4: Page 2", line=4),
        ]
    )

    demo_pump.handle_key("D")
    _set_next_state.assert_called_with(ANY, True)
    assert _set_next_state.call_args.args[0].name() == "DemoModeMenu"
