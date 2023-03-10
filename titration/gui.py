
import tkinter as tk

from titration.titrator import Titrator

class GUI():

    def __init__(self):
        """
        The GUI for the Alkalinity Titrator 
        """
        self.root = tk.Tk()
        self.root.geometry("300x220")
        self.root.title("Alkalinity Titrator")
        self.root.configure(background='black')

        self.titrator = Titrator(self.root)

        self.titrator.loop()

        buttonframe = tk.Frame(self.root)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)
        buttonframe.columnconfigure(3, weight=1)

        btn1 = tk.Button(buttonframe, text="1", bg='silver',
                        command=lambda: self.titrator.handle_ui("1"), relief="raised")
        btn1.grid(row = 4, column = 0, sticky=tk.W+tk.E)

        btn2 = tk.Button(buttonframe, text="2", bg='silver',
                        command=lambda: self.titrator.handle_ui("2"), relief="raised")
        btn2.grid(row = 4, column = 1, sticky=tk.W+tk.E)

        btn3 = tk.Button(buttonframe, text="3", bg='silver',
                        command=lambda: self.titrator.handle_ui("3"), relief="raised")
        btn3.grid(row = 4, column = 2, sticky=tk.W+tk.E)

        btnA = tk.Button(buttonframe, text="A", bg='silver',
                        command=lambda: self.titrator.handle_ui("A"), relief="raised")
        btnA.grid(row = 4, column = 3, sticky=tk.W+tk.E)

        btn4 = tk.Button(buttonframe, text="4", bg='silver',
                        command=lambda: self.titrator.handle_ui("4"), relief="raised")
        btn4.grid(row = 5, column = 0, sticky=tk.W+tk.E)

        btn5 = tk.Button(buttonframe, text="5", bg='silver',
                        command=lambda: self.titrator.handle_ui("5"), relief="raised")
        btn5.grid(row = 5, column = 1, sticky=tk.W+tk.E)

        btn6 = tk.Button(buttonframe, text="6", bg='silver',
                        command=lambda: self.titrator.handle_ui("6"), relief="raised")
        btn6.grid(row = 5, column = 2, sticky=tk.W+tk.E)

        btnB = tk.Button(buttonframe, text="B", bg='silver',
                        command=lambda: self.titrator.handle_ui("B"), relief="raised")
        btnB.grid(row = 5, column = 3, sticky=tk.W+tk.E)

        btn7 = tk.Button(buttonframe, text="7", bg='silver',
                        command=lambda: self.titrator.handle_ui("7"), relief="raised")
        btn7.grid(row = 6, column = 0, sticky=tk.W+tk.E)

        btn8 = tk.Button(buttonframe, text="8", bg='silver',
                        command=lambda: self.titrator.handle_ui("8"), relief="raised")
        btn8.grid(row = 6, column = 1, sticky=tk.W+tk.E)

        btn9 = tk.Button(buttonframe, text="9", bg='silver',
                        command=lambda: self.titrator.handle_ui("9"), relief="raised")
        btn9.grid(row = 6, column = 2, sticky=tk.W+tk.E)

        btnC = tk.Button(buttonframe, text="C", bg='silver',
                        command=lambda: self.titrator.handle_ui("C"), relief="raised")
        btnC.grid(row = 6, column = 3, sticky=tk.W+tk.E)

        btnStar = tk.Button(buttonframe, text="*", bg='silver',
                        command=lambda: self.titrator.handle_ui("*"), relief="raised")
        btnStar.grid(row = 7, column = 0, sticky=tk.W+tk.E)

        btn0 = tk.Button(buttonframe, text="0", bg='silver',
                        command=lambda: self.titrator.handle_ui("0"), relief="raised")
        btn0.grid(row = 7, column = 1, sticky=tk.W+tk.E)

        btnHash = tk.Button(buttonframe, text="#", bg='silver',
                        command=lambda: self.titrator.handle_ui("#"), relief="raised")
        btnHash.grid(row = 7, column = 2, sticky=tk.W+tk.E)

        btnD = tk.Button(buttonframe, text="D", bg='silver',
                        command=lambda: self.titrator.handle_ui("D"), relief="raised")
        btnD.grid(row = 7, column = 3, sticky=tk.W+tk.E)

        buttonframe.pack(fill='x')

        self.root.mainloop()