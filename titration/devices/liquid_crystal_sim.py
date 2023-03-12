"""
The file for mocking the LiquidCrystal class for testing purposes
"""

# pylint: disable = unused-argument

import tkinter as tk

FONT = ("Courier", 15)
WIDTH = 29
FG = "white"
BG = "blue"
ANCHOR = "w"
STICKY = tk.W + tk.E + tk.N + tk.S


class LiquidCrystal:
    """
    The class for the mock of the Sunfire LCD 20x04 Char Display
    """

    def __init__(self, cols, rows, root):
        """
        The function to initialize the GUI LCD
        """

        # Initialize the Labels
        root = tk.Frame(root)
        root.config(bg=BG)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)

        self.line_1 = tk.Label(
            root,
            text="Line 1",
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_1.grid(row=0, column=0, sticky=STICKY)

        self.line_2 = tk.Label(
            root,
            text="Line 2",
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_2.grid(row=1, column=0, sticky=STICKY)

        self.line_3 = tk.Label(
            root,
            text="Line 3",
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_3.grid(row=2, column=0, sticky=STICKY)

        self.line_4 = tk.Label(
            root,
            text="Line 4",
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_4.grid(row=3, column=0, sticky=STICKY)

        root.grid(row=0, column=0, sticky=STICKY)

    def print(self, message, line, style="left"):
        """
        The function to send a string to the GUI LCD
        """
        if line == 1:
            self.line_1.config(text=message)
        elif line == 2:
            self.line_2.config(text=message)
        elif line == 3:
            self.line_3.config(text=message)
        elif line == 4:
            self.line_4.config(text=message)
