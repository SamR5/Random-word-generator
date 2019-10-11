#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Word generator


import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import random as r

import Words as w
w.initialize() # loads the index

class MyApp():
    def __init__(self, master):
        self.master = master
        self.gui()

    def gui(self):
        # Add first/last letter
        # length of the words
        self.lengthLab = tk.Label(self.master, text="Length (2 to 20)")
        self.userLength = tk.StringVar()
        self.lengthEnt = tk.Entry(self.master, textvariable=self.userLength,
                                  width=7)
        # amount of words to generate
        self.numberLab = tk.Label(self.master, text="Number")
        self.userNumber = tk.StringVar()
        self.numberEnt = tk.Entry(self.master, textvariable=self.userNumber,
                                  width=7)
        #
        self.resultBox = tk.Listbox(self.master, font='monospace')
        # Button to generate words
        self.generateButton = tk.Button(self.master, text="Generate",
                                        command=self.generate)
        self.lengthLab.grid(row=0, column=0, padx=10, pady=15)
        self.lengthEnt.grid(row=0, column=1)
        self.numberLab.grid(row=1, column=0, pady=15)
        self.numberEnt.grid(row=1, column=1)
        self.generateButton.grid(row=2, column=0, columnspan=2)
        self.resultBox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def generate(self):
        try:
            length = int(self.userLength.get())
        except ValueError:
            length = 5
        try:
            number = int(self.userNumber.get())
        except ValueError:
            number = 10
        return self.display(w.filtrated_generator(length, number))

    def display(self, words):
        """"""
        self.resultBox.delete(0, 'end')
        for w in words:
            self.resultBox.insert(0, w)
        


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Words generator')
    A = MyApp(root)
    root.mainloop()
