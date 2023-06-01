"""
The file to hold the Alkalinity Titrator's GUI class
"""

# pylint: disable = too-many-locals, too-many-statements

import threading
import time
import tkinter as tk

STICKY = tk.E + tk.W + tk.S + tk.N
FONT = ("Courier", 15)
TEXTBOX_WIDTH = 15
LABEL_WIDTH = 20
BUTTON_WIDTH = 8
WIDTH = 22
FG = "white"
BG = "blue"
ANCHOR = "w"


class GUI:
    """
    The class for the Alkalinity Titrator's GUI
    """

    def __init__(self, titrator):
        """
        The GUI for the Alkalinity Titrator
        """

        # Keep an Instance of the Titrator
        self.titrator = titrator

        # Initialize the GUI Frame
        self.root = tk.Tk()
        self.root.geometry("280x200")
        self.root.title("Alkalinity Titrator")
        self.root.configure(background="black")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Initialize the Labels
        label_frame = tk.Frame(self.root)
        label_frame.config(bg=BG)
        label_frame.rowconfigure(0, weight=1)
        label_frame.rowconfigure(1, weight=1)
        label_frame.rowconfigure(2, weight=1)
        label_frame.rowconfigure(3, weight=1)

        self.line_1 = tk.Label(
            label_frame,
            text=self.titrator.lcd.get_line(1),
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_1.grid(row=0, column=0, sticky=STICKY)

        self.line_2 = tk.Label(
            label_frame,
            text=self.titrator.lcd.get_line(2),
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_2.grid(row=1, column=0, sticky=STICKY)

        self.line_3 = tk.Label(
            label_frame,
            text=self.titrator.lcd.get_line(3),
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_3.grid(row=2, column=0, sticky=STICKY)

        self.line_4 = tk.Label(
            label_frame,
            text=self.titrator.lcd.get_line(4),
            fg=FG,
            bg=BG,
            font=FONT,
            width=WIDTH,
            anchor=ANCHOR,
        )
        self.line_4.grid(row=3, column=0, sticky=STICKY)

        label_frame.grid(row=0, column=0, sticky=STICKY)

        # Initialize the Buttons
        buttonframe = tk.Frame(self.root)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)
        buttonframe.columnconfigure(3, weight=1)

        tk.Button(
            buttonframe,
            text="1",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("1"),
        ).grid(row=4, column=0, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="2",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("2"),
        ).grid(row=4, column=1, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="3",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("3"),
        ).grid(row=4, column=2, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="A",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("A"),
        ).grid(row=4, column=3, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="4",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("4"),
        ).grid(row=5, column=0, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="5",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("5"),
        ).grid(row=5, column=1, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="6",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("6"),
        ).grid(row=5, column=2, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="B",
            width=8,
            command=lambda: self.button_press("B"),
        ).grid(row=5, column=3, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="7",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("7"),
        ).grid(row=6, column=0, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="8",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("8"),
        ).grid(row=6, column=1, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="9",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("9"),
        ).grid(row=6, column=2, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="C",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("C"),
        ).grid(row=6, column=3, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="*",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("*"),
        ).grid(row=7, column=0, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="0",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("0"),
        ).grid(row=7, column=1, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="#",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("#"),
        ).grid(row=7, column=2, sticky=STICKY)

        tk.Button(
            buttonframe,
            text="D",
            width=BUTTON_WIDTH,
            command=lambda: self.button_press("D"),
        ).grid(row=7, column=3, sticky=STICKY)

        buttonframe.grid(row=1, column=0, sticky=STICKY)

        self.thread = threading.Thread(target=self.update_lcd, daemon=True)
        self.thread.start()

        self.root.mainloop()

    def button_press(self, key):
        """
        The function to facilitate button presses
        """
        self.titrator.keypad.set_key(key)

    def update_lcd(self):
        """
        The function to update the GUI LCD
        """
        while True:
            time.sleep(0.001)
            self.line_1.config(
                text=self.titrator.lcd.get_line(1),
                anchor=self.titrator.lcd.get_style(1),
            )
            self.line_2.config(
                text=self.titrator.lcd.get_line(2),
                anchor=self.titrator.lcd.get_style(2),
            )
            self.line_3.config(
                text=self.titrator.lcd.get_line(3),
                anchor=self.titrator.lcd.get_style(3),
            )
            self.line_4.config(
                text=self.titrator.lcd.get_line(4),
                anchor=self.titrator.lcd.get_style(4),
            )
