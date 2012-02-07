#!/usr/bin/env python
from Tkinter import *
import tkFileDialog
import data_analyzer

class App:
    def __init__(self, master):
        # initializing variables
        self.filepath_open = None
        frame_1 = Frame(master)
        frame_2 = Frame(master)
        frame_3 = Frame(master)
        frame_4 = Frame(master)
        # creating widgets
        self.label_data_analyzer = Label(frame_1, text="Data Analyzer")
        self.button_open_nexus = Button(frame_2, text="Open Nexus file", command=self.command_button_open_nexus)
        self.button_save_file = Button(frame_3, text="Save file as...", command=self.command_button_save_file)
        self.button_analyze = Button(frame_4, text="Analyze!", command=self.command_button_analyze)
        # configuring widgets
        # packing widgets
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        self.label_data_analyzer.pack(side=TOP)
        self.button_open_nexus.pack(side=LEFT)
        self.button_save_file.pack(side=LEFT)
        self.button_analyze.pack(side=TOP)

    def command_button_open_nexus(self):
        self.filepath_open = tkFileDialog.askopenfilename(filetypes=[("Nexus", "*.nex")], title="Open File...")

    def command_button_save_file(self):
        self.filepath_save = tkFileDialog.asksaveasfilename(filetypes=[("Comma-Separated File", "*.csv")], initialfile="data_analysis.csv", title="Save File As...")

    def command_button_analyze(self):
        data_analyzer.analyze_data(self.filepath_open, self.filepath_save)


root = Tk()
app = App(root)
root.mainloop()
