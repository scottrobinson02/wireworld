import tkinter as tk
from tkinter import *

import ww_config

root = Tk()

import ww_display  # this has to be below the "root =Tk()" line, or else it causes a 2nd window to open

root.title("Wireworld")


class TitleLabel(tk.Label):
    instancelist = []

    def __init__(self, text):
        super().__init__()
        TitleLabel.instancelist.append(self)
        self["text"] = text
        self.configure(font=("Arial", 20))


class ErrorLabel(tk.Label):
    instancelist = []

    def __init__(self, text):
        super().__init__()
        ErrorLabel.instancelist.append(self)
        self.contents = tk.StringVar()
        self.contents.set(text)
        self["textvariable"] = self.contents

        self.configure(font=("Arial", 20))


class FileEntryBox(tk.Entry):
    instancelist = []

    def __init__(self):

        FileEntryBox.instancelist.append(self)
        super().__init__()
        self["width"] = 30

        self.contents = tk.StringVar()
        self.contents.set("")
        self["textvariable"] = self.contents

        self.bind("<Key-Return>", self.printfile)

        self.configure(font=("Arial", 20))

    def printfile(self, x):
        filename = self.contents.get()
        if filename != "":
            error = ww_config.main(filename)
            if isinstance(error, str):
                [instance.destroy() for instance in ErrorLabel.instancelist]
                ErrorLabel(error).grid(column=0, row=2, padx=10, pady=10, columnspan=3, sticky=tk.W + tk.E)
            else:
                destroyall()
                ww_display.setup(error)


class NumEnterBox(tk.Spinbox):
    instancelist = []

    def __init__(self, coord):
        NumEnterBox.instancelist.append(self)
        super().__init__()
        self.coord = coord
        self["width"] = 12
        self["to"] = 100
        self["from"] = 5

        self.contents = tk.StringVar()
        self.contents.set(8)
        self["textvariable"] = self.contents
        self.bind("<Key-Return>", numsubmit)

        self.configure(font=("Arial", 18))

    def returnval(self, requested):
        if self.coord == "x":
            if requested == "x":
                return self.contents.get()
        if self.coord == "y":
            if requested == "y":
                return self.contents.get()


class NumEnterSubmit(tk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()

        NumEnterSubmit.instancelist.append(self)

        self["text"] = "Submit"
        self.bind("<Button-1>", numsubmit)
        self.bind("<space>", )

        self.configure(font=("Arial", 18))


def numsubmit(x):
    gridx = [instance.returnval("x") for instance in NumEnterBox.instancelist]
    gridy = [instance.returnval("y") for instance in NumEnterBox.instancelist]
    gridx = gridx[0]
    gridy = gridy[1]
    if int(gridx) < 5:
        gridx = 5
    if int(gridy) < 5:
        gridy = 5
    destroyall()
    array = [[0 for col in range(int(gridx))] for row in range(int(gridy))]  # creates array of 0s of specified size
    ww_display.setup(array)


def destroyall():
    allinst = (ErrorLabel.instancelist + FileEntryBox.instancelist + TitleLabel.instancelist
               + NumEnterBox.instancelist + NumEnterSubmit.instancelist)
    [instance.destroy() for instance in allinst]


def close():
    # root.destroy()
    quit()


def main():
    TitleLabel("Please enter the config file name").grid(column=0, row=0, padx=10, pady=10,
                                                         columnspan=3, sticky=tk.W + tk.E)
    FileEntryBox().grid(column=0, row=1, padx=10, pady=10, columnspan=3, sticky=tk.W + tk.E)
    ErrorLabel("").grid(column=0, row=2, padx=10, pady=10, columnspan=3, sticky=tk.W + tk.E)
    TitleLabel("Alternatively, enter the dimensions for an empty grid").grid(column=0, row=3, padx=10, pady=10,
                                                                             columnspan=3, sticky=tk.W + tk.E)
    NumEnterBox("x").grid(column=0, row=4, padx=10, pady=10)
    NumEnterBox("y").grid(column=1, row=4, padx=10, pady=10)
    NumEnterSubmit().grid(column=2, row=4, padx=10, pady=10)
    root.protocol("WM_DELETE_WINDOW", close)
    root.bind(")", lambda event: ww_display.paint(0))
    root.bind("!", lambda event: ww_display.paint(1))
    root.bind('"', lambda event: ww_display.paint(2))
    root.bind("<sterling>", lambda event: ww_display.paint(3))
    root.bind("<Escape>", lambda event: ww_display.paint("esc"))
    root.mainloop()


while 0 != 1:
    main()
