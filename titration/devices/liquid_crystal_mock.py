"""
The file for mocking the LiquidCrystal class for testing purposes
"""
import tkinter as tk


class LiquidCrystal:
    """
    The class for the mock of the Sunfire LCD 20x04 Char Display
    """

    def __init__(self, root):
        self.root = root
        self.Line1 = tk.Label(root, text="Line 1", fg = "white", bg ="blue", font = ('Arial', 15), width=20, anchor="w")
        self.Line1.pack(fill = "x")

        self.Line2 = tk.Label(root, text="Line 2", fg = "white", bg ="blue", font = ('Arial', 15), width=20, anchor="w")
        self.Line2.pack(fill ="x")

        self.Line3 = tk.Label(root, text="Line 3", fg = "white", bg ="blue", font = ('Arial', 15), width = 20, anchor="w")
        self.Line3.pack(fill ="x")

        self.Line4 = tk.Label(root, text="Line 4", fg = "white", bg ="blue", font = ('Arial', 15), width = 20, anchor="w")
        self.Line4.pack(fill = "x")

    def print(self, message, line, style="left"):
        """
        The function to send a string to the GUI LCD
        """
        
        if style == "left":
            anchor = "W"
        elif style == "right":
            anchor = "E"
        elif style == "center":
            anchor = "CENTER"
        

        if line == 1:
            print("REACHED")
            self.Line1.config(text="ONE")
        elif line == 2:
            self.Line2.config(text="TWO")
        elif line == 3:
            self.Line3.config(text="THREE")
        elif line == 4:
            self.Line4.config(text="FOUR")
