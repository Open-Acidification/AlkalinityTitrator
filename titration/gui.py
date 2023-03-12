"""
The file to hold the Alkalinity Titrator's GUI class
"""

# pylint: disable = too-many-locals, too-many-statements

import tkinter as tk

from titration.titrator import Titrator

STICKY = tk.E + tk.W + tk.S + tk.N
FONT = ("Courier", 15)

TEXTBOX_WIDTH = 15
LABEL_WIDTH = 20
BUTTON_WIDTH = 8


class GUI:
    """
    The class for the Alkalinity Titrator's GUI
    """

    def __init__(self):
        """
        The GUI for the Alkalinity Titrator
        """

        # Initialize the GUI Frame
        self.root = tk.Tk()
        self.root.geometry("475x210")
        self.root.title("Alkalinity Titrator")
        self.root.configure(background="black")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Create a Titrator Instance
        self.titrator = Titrator(self.root)

        # Initial loop to get the Main Menu
        self.titrator.loop()

        # Initialize the Textboxes
        textboxframe = tk.Frame(self.root)
        textboxframe.rowconfigure(0, weight=1)
        textboxframe.rowconfigure(1, weight=1)
        textboxframe.rowconfigure(2, weight=1)
        textboxframe.rowconfigure(3, weight=1)
        textboxframe.rowconfigure(4, weight=1)
        textboxframe.rowconfigure(5, weight=1)
        textboxframe.rowconfigure(6, weight=1)
        textboxframe.rowconfigure(7, weight=1)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=0, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=1, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=2, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=3, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=4, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=5, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=6, column=0, sticky=STICKY)

        tk.Text(
            textboxframe,
            font=FONT,
            width=TEXTBOX_WIDTH,
        ).grid(row=7, column=0, sticky=STICKY)

        textboxframe.grid(row=0, column=2, rowspan=2, sticky=STICKY)

        # Initialize the Labels for Variables
        labelframev = tk.Frame(self.root)
        labelframev.rowconfigure(0, weight=1)
        labelframev.rowconfigure(1, weight=1)
        labelframev.rowconfigure(2, weight=1)
        labelframev.rowconfigure(3, weight=1)
        labelframev.rowconfigure(4, weight=1)
        labelframev.rowconfigure(5, weight=1)
        labelframev.rowconfigure(6, weight=1)
        labelframev.rowconfigure(7, weight=1)

        tk.Label(
            labelframev,
            text="pH",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=0, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="Salinity",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=1, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="Temperature",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=2, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="Volume",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=3, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=4, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=5, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=6, column=0, sticky=STICKY)

        tk.Label(
            labelframev,
            text="",
            fg="white",
            bg="black",
            font=FONT,
            width=LABEL_WIDTH,
            anchor="w",
        ).grid(row=7, column=0, sticky=STICKY)

        labelframev.grid(row=0, column=1, rowspan=2, sticky=STICKY)

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

        # Run the GUI loop
        self.root.mainloop()

    def button_press(self, key):
        """
        The function to facilitate button presses
        """
        self.titrator.handle_ui(key)
