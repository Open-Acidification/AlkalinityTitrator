
import tkinter as tk

class GUI():

    def __init__(self):
        """
        The GUI for the Alkalinity Titrator 
        """

        self.root = tk.Tk()
        self.root.geometry("300x220")
        self.root.title("Alkalinity Titrator")
        self.root.configure(background='black')

        self.lcd = LCD(self.root)

        self.keypad = Keypad(self.root)


        self.root.mainloop()

class LCD():

    def __init__(self, root):
        self.Line1 = tk.Label(root, text="Line 1", fg = "white", bg ="blue", font = ('Arial', 15), width=20, anchor="w")
        self.Line1.pack(fill = "x")

        Line2 = tk.Label(root, text="Line 2", fg = "white", bg ="blue", font = ('Arial', 15), width=20, anchor="w")
        Line2.pack(fill ="x")

        Line3 = tk.Label(root, text="Line 3", fg = "white", bg ="blue", font = ('Arial', 15), width = 20, anchor="w")
        Line3.pack(fill ="x")

        Line4 = tk.Label(root, text="Line 4", fg = "white", bg ="blue", font = ('Arial', 15), width = 20, anchor="w")
        Line4.pack(fill = "x")




gui = GUI()