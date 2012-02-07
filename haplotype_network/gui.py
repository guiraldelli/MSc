#!/usr/bin/env python
from Tkinter import *
import tkFileDialog
import haplotype_network

class App:
    def __init__(self, master):
        # initializing variables
        self.filepath_open = None
        self.filepath_save = None
        self.save_dot = BooleanVar()
        self.save_text = BooleanVar()
        self.save_tex = BooleanVar()
        self.save_minimum_spanning_tree = BooleanVar()
        frame_1 = Frame(master)
        frame_2 = Frame(master)
        frame_3 = Frame(master)
        frame_4 = Frame(master)
        frame_5 = Frame(master)
        # creating widgets
        self.label_haplotype_network_analysis = Label(frame_1, text="Haplotype Network Analysis")
        self.button_open_nexus = Button(frame_2, text="Open Nexus file", command=self.command_button_open_nexus)
        self.button_save_output = Button(frame_3, text="Save output as...", command=self.command_button_save_output)
        self.checkbutton_dot = Checkbutton(frame_3, text="Dot", variable=self.save_dot)
        self.checkbutton_text = Checkbutton(frame_3, text="Text", variable=self.save_text)
        self.checkbutton_tex = Checkbutton(frame_3, text="TeX", variable=self.save_tex)
        self.checkbutton_minimum_spanning_tree = Checkbutton(frame_4, text="Minimum Spanning Trees", variable=self.save_minimum_spanning_tree)
        self.button_analyze = Button(frame_5, text="Analyze!", command=self.command_button_analyze)
        # configuring widgets
        self.checkbutton_text.select()
        # packing widgets
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        frame_5.pack()
        self.label_haplotype_network_analysis.pack(side=TOP)
        self.button_open_nexus.pack(side=LEFT)
        self.button_save_output.pack(side=LEFT)
        self.checkbutton_dot.pack(side=LEFT)
        self.checkbutton_text.pack(side=LEFT)
        self.checkbutton_tex.pack(side=LEFT)
        self.checkbutton_minimum_spanning_tree.pack(side=LEFT)
        self.button_analyze.pack(side=TOP)

    def command_button_open_nexus(self):
        self.filepath_open = tkFileDialog.askopenfilename(filetypes=[("Nexus", "*.nex")], title="Open File...")

    def command_button_save_output(self):
        self.filepath_save = tkFileDialog.asksaveasfilename(title="Save File As...")

    def command_button_analyze(self):
        haplotype_network.analyze_data(self.filepath_open, self.filepath_save, self.save_dot.get(), self.save_text.get(), self.save_tex.get(), self.save_minimum_spanning_tree.get())


root = Tk()
app = App(root)
root.mainloop()
