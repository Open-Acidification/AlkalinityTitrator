
import tkinter as tk

class Keypad():
    """
    The class for the GUI's Keypad
    """

    def __init__(self, root):
        """
        The function to initialize the keypad simulation
        """

        self.key_pressed = None

        buttonframe = tk.Frame(root)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)
        buttonframe.columnconfigure(3, weight=1)

        btn1 = tk.Button(buttonframe, text="1", bg='silver',
                        command=lambda: self.set_key_pressed("1"), relief="raised")
        btn1.grid(row = 4, column = 0, sticky=tk.W+tk.E)

        btn2 = tk.Button(buttonframe, text="2", bg='silver',
                        command=lambda: self.set_key_pressed("2"), relief="raised")
        btn2.grid(row = 4, column = 1, sticky=tk.W+tk.E)

        btn3 = tk.Button(buttonframe, text="3", bg='silver',
                        command=lambda: self.set_key_pressed("3"), relief="raised")
        btn3.grid(row = 4, column = 2, sticky=tk.W+tk.E)

        btnA = tk.Button(buttonframe, text="A", bg='silver',
                        command=lambda: self.set_key_pressed("A"), relief="raised")
        btnA.grid(row = 4, column = 3, sticky=tk.W+tk.E)

        btn4 = tk.Button(buttonframe, text="4", bg='silver',
                        command=lambda: self.set_key_pressed("4"), relief="raised")
        btn4.grid(row = 5, column = 0, sticky=tk.W+tk.E)

        btn5 = tk.Button(buttonframe, text="5", bg='silver',
                        command=lambda: self.set_key_pressed("5"), relief="raised")
        btn5.grid(row = 5, column = 1, sticky=tk.W+tk.E)

        btn6 = tk.Button(buttonframe, text="6", bg='silver',
                        command=lambda: self.set_key_pressed("6"), relief="raised")
        btn6.grid(row = 5, column = 2, sticky=tk.W+tk.E)

        btnB = tk.Button(buttonframe, text="B", bg='silver',
                        command=lambda: self.set_key_pressed("B"), relief="raised")
        btnB.grid(row = 5, column = 3, sticky=tk.W+tk.E)

        btn7 = tk.Button(buttonframe, text="7", bg='silver',
                        command=lambda: self.set_key_pressed("7"), relief="raised")
        btn7.grid(row = 6, column = 0, sticky=tk.W+tk.E)

        btn8 = tk.Button(buttonframe, text="8", bg='silver',
                        command=lambda: self.set_key_pressed("8"), relief="raised")
        btn8.grid(row = 6, column = 1, sticky=tk.W+tk.E)

        btn9 = tk.Button(buttonframe, text="9", bg='silver',
                        command=lambda: self.set_key_pressed("9"), relief="raised")
        btn9.grid(row = 6, column = 2, sticky=tk.W+tk.E)

        btnC = tk.Button(buttonframe, text="C", bg='silver',
                        command=lambda: self.set_key_pressed("C"), relief="raised")
        btnC.grid(row = 6, column = 3, sticky=tk.W+tk.E)

        btnStar = tk.Button(buttonframe, text="*", bg='silver',
                        command=lambda: self.set_key_pressed("*"), relief="raised")
        btnStar.grid(row = 7, column = 0, sticky=tk.W+tk.E)

        btn0 = tk.Button(buttonframe, text="0", bg='silver',
                        command=lambda: self.set_key_pressed("0"), relief="raised")
        btn0.grid(row = 7, column = 1, sticky=tk.W+tk.E)

        btnHash = tk.Button(buttonframe, text="#", bg='silver',
                        command=lambda: self.set_key_pressed("#"), relief="raised")
        btnHash.grid(row = 7, column = 2, sticky=tk.W+tk.E)

        btnD = tk.Button(buttonframe, text="D", bg='silver',
                        command=lambda: self.set_key_pressed("D"), relief="raised")
        btnD.grid(row = 7, column = 3, sticky=tk.W+tk.E)

        buttonframe.pack(fill='x')

    def set_key_pressed(self, key):
        """
        The function to update the key that was pressed
        """
        self.key_pressed = key

    def get_key(self):
        """
        The function to get the pressed key
        """
        temp = self.key_pressed
        self.key_pressed = None
        return temp
