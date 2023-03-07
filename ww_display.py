# Was taking ages to create/reset grids (8x8 would take 5s, 20x20 took like 40s or didn't happen at all
# Restarting the vdi fixed this, now 32x32 takes 3.5s
# So unsure if repeatedly running the code is clogging up memory, or just because vdi had been open for 4 days

import copy
import json
import tkinter as tk
from tkinter import ttk

import ww_config
import ww_next

style = ttk.Style()

# activebackground and highlightbackground are meant to do something, but doesn't seem to work at all (on linux only?)
style.configure("Squares0.TButton", font=("Arial", 20), relief="sunken")
style.configure("Squares1.TButton", font=("Arial", 20), background="blue", foreground="grey")
style.configure("Squares2.TButton", font=("Arial", 20), background="red")
style.configure("Squares3.TButton", font=("Arial", 20), background="yellow")
style.configure("NormalButtons.TButton", font=("Helvetica", 9))


# screen_height = win.winfo_screenheight()

class ArrayManager:
    instancelist = []

    def __init__(self):
        ArrayManager.instancelist.append(self)
        self.main_array = [[]]
        self.start_array = [[]]


class GridButton(ttk.Button):
    instancelist = []
    painting = False
    paintlastval = 100  # arbitrary values, which aren't 0/1/2/3
    paintvalue = 200

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        GridButton.instancelist.append(self)
        self.val = arrman.main_array[y][x]
        self.contents = tk.StringVar()
        # self["command"] = lambda: self.changeval()
        self.bind("<Button-1>", self.addval)
        self.bind("<space>", self.addval)
        self.bind("<Button-3>", self.reduceval)

        self["padding"] = -2
        self["width"] = 2
        # self["height"] = 2

        self.contents.set(str(self.val))

        self.styleupdate()
        self["textvariable"] = self.contents

        self.bind("<Button-2>", debuginfo)
        self.bind("<Enter>", self.paintval)

    def updatepadding(self, padval):
        self["padding"] = padval

    def paintval(self, x):
        if GridButton.painting:
            self.val = GridButton.paintvalue
            arrman.main_array[self.y][self.x] = GridButton.paintvalue
            self.contents.set(str(self.val))
            self.styleupdate()

    def addval(self, x):
        if self.val < 3:
            self.val += 1
            arrman.main_array[self.y][self.x] += 1
        else:
            self.val = 0
            arrman.main_array[self.y][self.x] = 0
        self.contents.set(str(self.val))
        self.styleupdate()

    def reduceval(self, x):  # x is unusued, but required or else i get errors
        if self.val > 0:
            self.val -= 1
            arrman.main_array[self.y][self.x] -= 1
        else:
            self.val = 3
            arrman.main_array[self.y][self.x] = 3
        self.contents.set(str(self.val))
        self.styleupdate()

    def styleupdate(self):
        if self.contents.get() == "0":
            self["style"] = "Squares0.TButton"
        if self.contents.get() == "1":
            self["style"] = "Squares1.TButton"
        if self.contents.get() == "2":
            self["style"] = "Squares2.TButton"
        if self.contents.get() == "3":
            self["style"] = "Squares3.TButton"

    def updateit(self, newstate):
        self.val = newstate[self.y][self.x]
        self.contents.set(str(self.val))
        self.styleupdate()


class NextButton(ttk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()

        NextButton.instancelist.append(self)

        self["text"] = "Next Step"
        self.bind("<Button-1>", nextstage)
        self.bind("<space>", nextstage)
        self["style"] = "NormalButtons.TButton"


class StartStopButton(ttk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()

        StartStopButton.instancelist.append(self)

        self.contents = tk.StringVar()
        self.contents.set("Start")
        self["textvariable"] = self.contents

        self.bind("<Button-1>", self.toggle)
        self.bind("<space>", self.toggle)
        self["style"] = "NormalButtons.TButton"
        self.start = 0
        self.running = ""

    def toggle(self, x):
        if self.start == 0:  # if off, turn on
            self.startstop("a")
            self.start = 1
            # print("starting")
            self.contents.set("Stop")
        else:
            self.after_cancel(self.running)
            self.start = 0
            # print("stopping")
            self.contents.set("Start")

    def startstop(self, x):
        for instance in StartStopNumber.instancelist:
            timegap = instance.contents.get()
        # timegap = 1  # in ms
        # print("running")
        nextstage("a")
        self.running = self.after(timegap, self.startstop, "a")


class StartStopNumber(tk.Spinbox):
    instancelist = []

    def __init__(self):
        super().__init__()

        StartStopNumber.instancelist.append(self)

        self["to"] = 10000
        self["from"] = 1
        self["width"] = 5
        self.contents = tk.StringVar()
        self.contents.set(100)
        self["textvariable"] = self.contents

        self.configure(font=("Arial", 13))


class ResetButton(ttk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()

        ResetButton.instancelist.append(self)

        self["text"] = "Reset"
        self.bind("<Button-1>", lambda event: reset())
        self.bind("<space>", lambda event: reset())


class PaintLabel(tk.Label):
    instancelist = []

    def __init__(self):
        super().__init__()

        PaintLabel.instancelist.append(self)

        self.contents = tk.StringVar()
        self.contents.set("Not Painting")
        self["textvariable"] = self.contents
        self.configure(font=("Helvetica", 10,), background="#D9D9D9", foreground="black")

    def updatepaint(self):
        # print("updating")
        if GridButton.painting:
            self.contents.set("Painting " + str(GridButton.paintvalue))
            if GridButton.paintvalue == 0:
                self.configure(background="white", foreground="black", font=("Helvetica", 11))
            if GridButton.paintvalue == 1:
                self.configure(background="blue", foreground="grey", font=("Helvetica", 11))
            if GridButton.paintvalue == 2:
                self.configure(background="red", foreground="black", font=("Helvetica", 11))
            if GridButton.paintvalue == 3:
                self.configure(background="yellow", foreground="black", font=("Helvetica", 11))
        else:
            self.contents.set("Not Painting")
            self.configure(background="#D9D9D9", foreground="black", font=("Helvetica", 10))


class SaveBox(tk.Entry):
    instancelist = []

    def __init__(self):
        super().__init__()

        SaveBox.instancelist.append(self)
        self.contents = tk.StringVar()
        self.contents.set("")
        self["textvariable"] = self.contents

        rowsno = (len(arrman.main_array))  # y coord
        colsno = (len(arrman.main_array[0]))  # x coord

        if colsno <= 9:
            self["width"] = ((colsno - 1) * 2) + 2

        self.bind("<Key-Return>", lambda event: filesaver(self.contents.get()))

        self.configure(font=("Arial", 20))


class SmallLabel(tk.Label):
    instancelist = []

    def __init__(self, text):
        super().__init__()

        SmallLabel.instancelist.append(self)
        self.contents = tk.StringVar()
        self.contents.set(text)
        self["textvariable"] = self.contents
        self.configure(font=("Arial", 12))


class SaveButton(ttk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()
        SaveButton.instancelist.append(self)
        self["text"] = "Save"
        self.bind("<Button-1>", save)
        self.bind("<space>", save)


class TitleLabel(tk.Label):
    instancelist = []

    def __init__(self, text):
        super().__init__()
        TitleLabel.instancelist.append(self)
        self["text"] = text
        self.configure(font=("Arial", 15))


class ErrorLabel(tk.Label):
    instancelist = []

    def __init__(self, text):
        super().__init__()
        ErrorLabel.instancelist.append(self)
        self.contents = tk.StringVar()
        self.contents.set(text)
        self["textvariable"] = self.contents

        self.configure(font=("Arial", 15))


class FileEntryBox(tk.Entry):
    instancelist = []

    def __init__(self):

        FileEntryBox.instancelist.append(self)
        super().__init__()
        self["width"] = 20

        self.contents = tk.StringVar()
        self.contents.set("")
        self["textvariable"] = self.contents

        self.bind("<Key-Return>", self.printfile)

        self.configure(font=("Arial", 16))

    def printfile(self, x):
        filename = self.contents.get()
        if filename != "":
            error = ww_config.main(filename)
            if isinstance(error, str):
                [instance.destroy() for instance in ErrorLabel.instancelist]
                colsno = (len(arrman.main_array[0]))  # x coord
                ErrorLabel(error).grid(column=colsno + 3, row=3, columnspan=3, sticky=tk.W + tk.E)
            else:
                allinst = (
                        SaveButton.instancelist + GridButton.instancelist
                        + NextButton.instancelist + ResetButton.instancelist + SmallLabel.instancelist
                        + MenuButton.instancelist + AddRowButton.instancelist + RemoveRowButton.instancelist
                        + PaintLabel.instancelist + StartStopButton.instancelist + StartStopNumber.instancelist
                )

                if SaveBox.instancelist:
                    allinst += (SaveBox.instancelist)

                if NumEnterBox.instancelist:
                    allinst += (NumEnterBox.instancelist + NumEnterSubmit.instancelist + TitleLabel.instancelist
                                + ErrorLabel.instancelist + FileEntryBox.instancelist)

                [instance.destroy() for instance in allinst]  # deletes the instances

                objectlist = [SaveButton, GridButton, NextButton, ResetButton, SmallLabel, MenuButton, SaveBox,
                              NumEnterBox, NumEnterSubmit, TitleLabel, ErrorLabel, FileEntryBox, AddRowButton,
                              RemoveRowButton, PaintLabel, StartStopButton, StartStopNumber]
                for objecttype in objectlist:
                    objecttype.instancelist.clear()  # then clears them from their respective instance lists

                allinst.clear()
                setup(error)


class NumEnterBox(tk.Spinbox):
    instancelist = []

    def __init__(self, coord):

        NumEnterBox.instancelist.append(self)
        super().__init__()
        self.coord = coord
        self["width"] = 12
        self["to"] = 100
        self["from"] = 7

        self.contents = tk.StringVar()
        if self.coord == "x":
            self.contents.set(len(arrman.main_array[0]))
        else:
            self.contents.set(len(arrman.main_array))
        self["textvariable"] = self.contents
        self.bind("<Key-Return>", numsubmit)

        self.configure(font=("Arial", 14))


class NumEnterSubmit(tk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()

        NumEnterSubmit.instancelist.append(self)

        self["text"] = "Submit"
        self.bind("<Button-1>", numsubmit)
        self.bind("<space>", )

        self.configure(font=("Arial", 16))


class MenuButton(ttk.Button):
    instancelist = []

    def __init__(self):
        super().__init__()
        MenuButton.instancelist.append(self)
        self["text"] = "Menu"
        self.menu_on = False
        self.bind("<Button-1>", self.togglemenu)
        self.bind("<space>", menu)

    def togglemenu(self, a):
        menu(self.menu_on)
        if not self.menu_on:
            self.menu_on = True
        else:
            self.menu_on = False


# used for expanding grid
class AddRowButton(ttk.Button):  # Used for the buttons that allow you to resize the grid
    instancelist = []

    def __init__(self, side):
        super().__init__()

        AddRowButton.instancelist.append(self)

        self["text"] = "+"
        # if side == "top":
        # print(side)
        self["width"] = 2
        self.bind("<Button-1>", self.add_row)
        self.bind("<space>", self.add_row)
        self.side = tk.StringVar()
        self.side.set(side)

    def add_row(self, x):
        side = self.side.get()
        # print("This is an add button from:" + str(side))

        if side == "top":
            arrman.main_array.insert(0, [0, ] * len(arrman.main_array[0]))  # top
        if side == "bottom":
            arrman.main_array.append([0, ] * len(arrman.main_array[0]))  # botttom
        if side == "left":
            for row in arrman.main_array:  # left
                row.insert(0, 0)
        if side == "right":
            for row in arrman.main_array:  # adds to right
                row.append(0)

        gridreset("add", side)


# used for reducing size of grid
class RemoveRowButton(ttk.Button):  # Used for the buttons that allow you to resize the grid
    instancelist = []

    def __init__(self, side):
        super().__init__()

        RemoveRowButton.instancelist.append(self)

        self["text"] = "-"
        # if side == "top":
        #     print(side)
        self["width"] = 2
        self.bind("<Button-1>", self.remove_row)
        self.bind("<space>", self.remove_row)
        self.side = tk.StringVar()
        self.side.set(side)

    def remove_row(self, x):
        side = self.side.get()
        # print("This is an add button from:" + str(side))

        if side == "bottom":
            if (len(arrman.main_array)) > 7:
                del arrman.main_array[-1]  # deletes bottom
                gridreset("remove", side)
        if side == "right":
            if (len(arrman.main_array[0])) > 7:
                for row in arrman.main_array:  # deletes right
                    del row[-1]
                    gridreset("remove", side)


#####################################################################################################################


def debuginfo(a):
    # print("x:", self.x, "y:", self.y, "contents:", self.contents.get(),"style:", self["style"],)
    gridlist = GridButton.instancelist
    print("//////")
    for row in gridlist:
        print(row)


def nextstage(x):
    arrman.main_array = ww_next.main(arrman.main_array)
    [instance.updateit(arrman.main_array) for instance in GridButton.instancelist]


def reset():
    allinst = (
            SaveButton.instancelist + GridButton.instancelist
            + NextButton.instancelist + ResetButton.instancelist + SmallLabel.instancelist
            + MenuButton.instancelist + AddRowButton.instancelist + RemoveRowButton.instancelist
            + PaintLabel.instancelist + StartStopButton.instancelist + StartStopNumber.instancelist
    )

    if SaveBox.instancelist:
        allinst += SaveBox.instancelist

    if NumEnterBox.instancelist:
        allinst += (NumEnterBox.instancelist + NumEnterSubmit.instancelist + TitleLabel.instancelist
                    + ErrorLabel.instancelist + FileEntryBox.instancelist)
    [instance.destroy() for instance in allinst]  # destroys the instances

    objectlist = [SaveButton, GridButton, NextButton, ResetButton, SmallLabel, MenuButton, SaveBox, NumEnterBox,
                  NumEnterSubmit, TitleLabel, ErrorLabel, FileEntryBox, AddRowButton, RemoveRowButton, PaintLabel,
                  StartStopButton, StartStopNumber]
    for objecttype in objectlist:
        objecttype.instancelist.clear()  # then clears them from their respective instance lists

    allinst.clear()

    setup(arrman.start_array)


def filesaver(name):
    with open(name + ".json", "w") as s:
        json.dump(arrman.main_array, s)
    [instance.destroy() for instance in SaveBox.instancelist]
    [instance.destroy() for instance in SmallLabel.instancelist]


def save(a):
    rowsno = (len(arrman.main_array))  # y coord
    colsno = (len(arrman.main_array[0]))  # x coord

    if colsno > 9:
        SaveBox().grid(column=0, row=rowsno + 2, columnspan=colsno)
        SmallLabel(".json").grid(column=int(colsno / 2) + 4, row=rowsno + 2)
    else:
        SaveBox().grid(column=0, row=rowsno + 2, columnspan=colsno)
        SmallLabel(".json").grid(column=colsno, row=rowsno + 2)


def numsubmit(x):
    for instance in NumEnterBox.instancelist:
        if instance.coord == "x":
            gridx = instance.contents.get()
        if instance.coord == "y":
            gridy = instance.contents.get()

    if int(gridx) < 7:
        gridx = 7
    if int(gridy) < 7:
        gridy = 7
    allinst = (
            SaveButton.instancelist + GridButton.instancelist
            + NextButton.instancelist + ResetButton.instancelist + SmallLabel.instancelist
            + MenuButton.instancelist + AddRowButton.instancelist + RemoveRowButton.instancelist
            + PaintLabel.instancelist + StartStopButton.instancelist + StartStopNumber.instancelist
    )

    if SaveBox.instancelist:
        allinst += (SaveBox.instancelist)

    if NumEnterBox.instancelist:
        allinst += (NumEnterBox.instancelist + NumEnterSubmit.instancelist + TitleLabel.instancelist
                    + ErrorLabel.instancelist + FileEntryBox.instancelist)
    [instance.destroy() for instance in allinst]  # destroys the instances

    objectlist = [SaveButton, GridButton, NextButton, ResetButton, SmallLabel, MenuButton, SaveBox, NumEnterBox,
                  NumEnterSubmit, TitleLabel, ErrorLabel, FileEntryBox, AddRowButton, RemoveRowButton, PaintLabel,
                  StartStopButton, StartStopNumber]

    for objecttype in objectlist:
        objecttype.instancelist.clear()  # then clears them from their respective instance lists

    array = [[0 for col in range(int(gridx))] for row in range(int(gridy))]  # creates array of 0s of specified size
    setup(array)


def menu(on):
    colsno = (len(arrman.main_array[0]))  # x coord
    if not on:
        TitleLabel("Please enter the config file name").grid(column=colsno + 3, row=1, columnspan=3, sticky=tk.W + tk.E)
        FileEntryBox().grid(column=colsno + 3, row=2, columnspan=3, sticky=tk.W + tk.E)
        ErrorLabel("").grid(column=colsno + 3, row=3, columnspan=3, sticky=tk.W + tk.E)
        TitleLabel("Alternatively, enter the dimensions for an empty grid").grid(column=colsno + 3, row=4,
                                                                                 columnspan=3, sticky=tk.W + tk.E)
        NumEnterBox("x").grid(column=colsno + 3, row=5)
        NumEnterBox("y").grid(column=colsno + 4, row=5)
        NumEnterSubmit().grid(column=colsno + 5, row=5)
    else:
        menuinstances = (TitleLabel.instancelist + FileEntryBox.instancelist + ErrorLabel.instancelist
                         + NumEnterBox.instancelist + NumEnterSubmit.instancelist)
        [instance.destroy() for instance in menuinstances]  # destroys instances

        objectlist = [NumEnterBox, NumEnterSubmit, TitleLabel, ErrorLabel, FileEntryBox]

        for objecttype in objectlist:
            objecttype.instancelist.clear()  # then clears them from their respective instance lists


def gridreset(type, side):  # used for expanding grid

    rowsno = (len(arrman.main_array))  # y coord
    colsno = (len(arrman.main_array[0]))  # x coord

    if type == "add":
        if side == "right":
            for button_y in (range(rowsno)):
                GridButton(colsno - 1, button_y).grid(row=button_y + 1, column=colsno)  # creates col of gridbuttons
                buttonsetup(colsno, rowsno, 1)
        if side == "bottom":
            for button_x in (range(colsno)):
                GridButton(button_x, rowsno - 1).grid(row=rowsno, column=button_x + 1)  # creates col of gridbuttons
                buttonsetup(colsno, rowsno, 1)

    if type == "remove":
        if side == "right":

            # deletes instances with x value that matches deleted column, and removes list

            dellist = list(filter(lambda instance: instance.x == colsno, GridButton.instancelist))
            while dellist:
                for instance in dellist:
                    if instance in GridButton.instancelist:
                        instance.destroy()
                        dellist.remove(instance)

            GridButton.instancelist = list(filter(lambda instance: instance.x != colsno, GridButton.instancelist))

            buttonsetup(colsno, rowsno, 1)
        if side == "bottom":
            # deletes instances with y value that matches deleted row, and removes from list

            dellist = list(filter(lambda instance: instance.y == rowsno, GridButton.instancelist))
            while dellist:
                for instance in dellist:
                    if instance in GridButton.instancelist:
                        instance.destroy()
                        dellist.remove(instance)

            GridButton.instancelist = list(filter(lambda instance: instance.y != rowsno, GridButton.instancelist))

            buttonsetup(colsno, rowsno, 1)


def buttonsetup(colsno, rowsno, resetting):
    if resetting == 1:
        allinst = (
                SaveButton.instancelist + NextButton.instancelist + ResetButton.instancelist + SmallLabel.instancelist
                + MenuButton.instancelist + AddRowButton.instancelist + RemoveRowButton.instancelist
                + PaintLabel.instancelist + StartStopButton.instancelist + StartStopNumber.instancelist
                # NO GRIDBUTTON HERE
        )

        if SaveBox.instancelist:
            allinst += SaveBox.instancelist

        if NumEnterBox.instancelist:
            allinst += (NumEnterBox.instancelist + NumEnterSubmit.instancelist + TitleLabel.instancelist
                        + ErrorLabel.instancelist + FileEntryBox.instancelist)
        [instance.destroy() for instance in allinst]

        objectlist = [SaveButton, NextButton, ResetButton, SmallLabel, MenuButton, SaveBox, NumEnterBox,
                      NumEnterSubmit, TitleLabel, ErrorLabel, FileEntryBox, AddRowButton, RemoveRowButton, PaintLabel,
                      StartStopButton, StartStopNumber]
        # NO GRIDBUTTON HERE

        for objecttype in objectlist:
            objecttype.instancelist.clear()  # then clears them from their respective instance lists

    ResetButton().grid(column=int(colsno) + 2, row=1)
    MenuButton().grid(column=int(colsno) + 2, row=2)
    NextButton().grid(column=int(colsno) + 2, row=int((rowsno / 2) + 0.5))  # creates the "next" button
    StartStopButton().grid(column=int(colsno) + 2, row=int((rowsno / 2) + 1.5))  # creates the "start" button
    StartStopNumber().grid(column=int(colsno) + 2, row=int((rowsno / 2) + 2.5))  # creates the "start" button
    PaintLabel().grid(column=int(colsno) + 2, row=int((rowsno * 0.8) + 1.5))  # creates the "Painting" label

    GridButton.painting = False
    GridButton.paintvalue = 200
    GridButton.paintlastval = 150
    [instance.updatepaint() for instance in PaintLabel.instancelist]

    SaveButton().grid(column=int(colsno) + 2, row=rowsno + 1)

    # Makes it so the +/- are either the middle 2 squares if even, or 1 above/below the middle if odd
    AddRowButton("right").grid(column=colsno + 1, row=(((rowsno + 1) // 2) + 1), padx=2, pady=2)
    RemoveRowButton("right").grid(column=colsno + 1, row=(rowsno // 2))

    AddRowButton("bottom").grid(column=((colsno + 1) // 2) + 1, row=rowsno + 1, padx=2, pady=2)
    RemoveRowButton("bottom").grid(column=(colsno // 2), row=rowsno + 1)
    stylescaling()


def paint(value):
    if GridButton.instancelist:  # only does anything when off initial screen

        if value != "esc":
            GridButton.paintlastval = GridButton.paintvalue
            GridButton.paintvalue = value

            if GridButton.painting:
                if GridButton.paintvalue == GridButton.paintlastval:
                    nextpaint = False
                    # print("painting off")
                else:
                    nextpaint = True

            else:
                nextpaint = True
                # print("painting on")

        else:
            nextpaint = False
            # print("painting off")

        GridButton.painting = nextpaint
        [instance.updatepaint() for instance in PaintLabel.instancelist]
        # print(PaintLabel.instancelist)


def stylescaling():
    maxwidth = 40
    maxheight = 16
    colsno = (len(arrman.main_array[0]))  # x coord
    rowsno = (len(arrman.main_array))  # y coord

    if (rowsno > maxheight) or (colsno > maxwidth):

        if (rowsno - maxheight) > (colsno - maxwidth):
            fontmult = (1 - ((rowsno - maxheight) / 50)) - 0.01
            if (fontmult * 20) < 1:
                fontmult = 1 / 20

        else:
            fontmult = (1 - ((colsno - maxwidth) / 50)) - 0.01
            if (fontmult * 20) < 1:
                fontmult = 1 / 20

    else:
        fontmult = 1

    style.configure("Squares0.TButton", font=("Arial", int(fontmult * 20)), relief="sunken")
    style.configure("Squares1.TButton", font=("Arial", int(fontmult * 20)), background="blue", foreground="grey")
    style.configure("Squares2.TButton", font=("Arial", int(fontmult * 20)), background="red")
    style.configure("Squares3.TButton", font=("Arial", int(fontmult * 20)), background="yellow")
    style.configure("NormalButtons.TButton", font=("Helvetica", 9))

    for instance in GridButton.instancelist:
        instance.updatepadding((4 * fontmult) - 1.75)
    # instance["width"] = fontmult*2
    # instance["height"] = fontmult * 2

    # print(fontmult)
    # print(int(fontmult * 20))

    if int(fontmult * 20) <= 15:
        for instance in ResetButton.instancelist:
            instance.grid(column=int(colsno) + 2, row=1, rowspan=2)
        for instance in MenuButton.instancelist:
            instance.grid(column=int(colsno) + 2, row=3, rowspan=2)
        for instance in NextButton.instancelist:
            instance.grid(column=int(colsno) + 2, row=int((rowsno / 2) + 0.5), rowspan=2)  # creates the "next" button
        for instance in StartStopButton.instancelist:
            instance.grid(column=int(colsno) + 2, row=int((rowsno / 2) + 2.5), rowspan=2)  # normally +1.5
        for instance in StartStopNumber.instancelist:
            instance.grid(column=int(colsno) + 2, row=int((rowsno / 2) + 4.5), rowspan=2)  # normally +2.5

        [instance.destroy() for instance in AddRowButton.instancelist]
        [instance.destroy() for instance in RemoveRowButton.instancelist]
        AddRowButton.instancelist.clear()
        RemoveRowButton.instancelist.clear()

        # +/-1, so it is same distance when size doubled
        AddRowButton("right").grid(column=colsno + 1, row=(((rowsno + 1) // 2) + 1) + 1, padx=2, pady=2, rowspan=2)
        RemoveRowButton("right").grid(column=colsno + 1, row=(rowsno // 2) - 1, rowspan=2)
        AddRowButton("bottom").grid(column=((colsno + 1) // 2) + 1 + 1, row=rowsno + 1, padx=2, pady=2, columnspan=2)
        RemoveRowButton("bottom").grid(column=(colsno // 2) - 1, row=rowsno + 1, columnspan=2)

        for instance in MenuButton.instancelist:
            instance.grid(column=int(colsno) + 2, row=3, rowspan=2)

        for instance in PaintLabel.instancelist:
            instance.grid(column=int(colsno) + 2, row=int((rowsno * 0.8) + 1.5), rowspan=2)  # painting


def setup(arr):
    # if arr != 0:
    arrman.main_array = arr

    arrman.start_array = copy.deepcopy(arrman.main_array)

    rowsno = (len(arrman.main_array))  # y coord
    colsno = (len(arrman.main_array[0]))  # x coord

    for button_y in (range(rowsno)):
        for button_x in (range(colsno)):
            GridButton(button_x, button_y).grid(row=button_y + 1, column=button_x + 1)  # creates all grid buttons

    buttonsetup(colsno, rowsno, 0)


arrman = ArrayManager()
