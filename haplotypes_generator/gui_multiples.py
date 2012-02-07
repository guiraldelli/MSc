#!/usr/bin/env python
from Tkinter import *
import tkFileDialog
import tkMessageBox
import generator
import control

class App:
    def __init__(self, master):
        frame_1 = Frame(master)
        frame_2 = Frame(master)
        frame_3 = Frame(master)
        frame_4 = Frame(master)
        frame_5 = Frame(master)
        frame_6 = Frame(master)
        frame_7 = Frame(master)
        frame_8 = Frame(master)
        frame_9 = Frame(master)
        # creating widgets
        self.label_number_simulations = Label(frame_1, text="How many simulations?")
        self.entry_number_simulations = Entry(frame_1, width=5)
        self.label_number_haplotypes = Label(frame_2, text="Number of haplotypes per simulation:")
        self.label_number_haplotypes_minimum = Label(frame_3, text="Minimum:")
        self.entry_number_haplotypes_minimum = Entry(frame_3, width=5)
        self.label_number_haplotypes_maximum = Label(frame_3, text="Maximum:")
        self.entry_number_haplotypes_maximum = Entry(frame_3, width=5)
        self.label_haplotype_length = Label(frame_4, text="What's the range of the haplotype length?")
        self.label_haplotype_length_minimum = Label(frame_5, text="Minimum:")
        self.entry_haplotype_length_minimum = Entry(frame_5, width=5)
        self.label_haplotype_length_maximum = Label(frame_5, text="Maximum:")
        self.entry_haplotype_length_maximum = Entry(frame_5, width=5)
        self.label_percentage_rate = Label(frame_6, text="Rate in % of Mutation and/or Recombination:")
        self.label_percentage_rate_minimum = Label(frame_7, text="Minimum:")
        self.entry_percentage_rate_minimum = Entry(frame_7, width=5)
        self.label_percentage_rate_maximum = Label(frame_7, text="Maximum:")
        self.entry_percentage_rate_maximum = Entry(frame_7, width=5)
        self.button_select_directory = Button(frame_8, text="Select Directory to Save Simulations...", command=self.command_button_select_directory)
        self.button_generate_sequence = Button(frame_9, text="Generate!", command=self.command_button_generate_sequence)
        # configuring widgets
        self.entry_number_simulations.insert(0,100)
        self.entry_number_haplotypes_minimum.insert(0,20)
        self.entry_number_haplotypes_maximum.insert(0,100)
        self.entry_haplotype_length_minimum.insert(0,50)
        self.entry_haplotype_length_maximum.insert(0,5000)
        self.entry_percentage_rate_minimum.insert(0,10)
        self.entry_percentage_rate_maximum.insert(0,90)
        # packing widgets
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        frame_5.pack()
        frame_6.pack()
        frame_7.pack()
        frame_8.pack()
        frame_9.pack()
        self.label_number_simulations.pack(side=LEFT)
        self.entry_number_simulations.pack(side=LEFT)
        self.label_number_haplotypes.pack(side=TOP)
        self.label_number_haplotypes_minimum.pack(side=LEFT)
        self.entry_number_haplotypes_minimum.pack(side=LEFT)
        self.label_number_haplotypes_maximum.pack(side=LEFT)
        self.entry_number_haplotypes_maximum.pack(side=LEFT)
        self.label_haplotype_length.pack(side=TOP)
        self.label_haplotype_length_minimum.pack(side=LEFT)
        self.entry_haplotype_length_minimum.pack(side=LEFT)
        self.label_haplotype_length_maximum.pack(side=LEFT)
        self.entry_haplotype_length_maximum.pack(side=LEFT)
        self.label_percentage_rate.pack(side=TOP)
        self.label_percentage_rate_minimum.pack(side=LEFT)
        self.entry_percentage_rate_minimum.pack(side=LEFT)
        self.label_percentage_rate_maximum.pack(side=LEFT)
        self.entry_percentage_rate_maximum.pack(side=LEFT)
        self.button_select_directory.pack(side=TOP)
        self.button_generate_sequence.pack(side=TOP)

    def command_button_select_directory(self):
        self.directory_to_save_simulations = tkFileDialog.askdirectory(title="Directory To Save Simulations...", initialdir=".", mustexist=True)

    def command_button_generate_sequence(self):
        number_simulations = int(self.entry_number_simulations.get())
        number_haplotypes_minimum = int(self.entry_number_haplotypes_minimum.get())
        number_haplotypes_maximum = int(self.entry_number_haplotypes_maximum.get())
        haplotype_length_maximum = int(self.entry_haplotype_length_maximum.get()) 
        haplotype_length_minimum = int(self.entry_haplotype_length_minimum.get())
        percentage_rate_minimum = int(self.entry_percentage_rate_minimum.get())
        percentage_rate_maximum = int(self.entry_percentage_rate_maximum.get())
        control.generate_multiple_sequences(number_simulations, number_haplotypes_minimum, number_haplotypes_maximum, haplotype_length_minimum, haplotype_length_maximum, percentage_rate_minimum, percentage_rate_maximum, self.directory_to_save_simulations)
        tkMessageBox.showinfo(title="Process Finished", message="All simulations have been done!")


root = Tk()
app = App(root)
root.mainloop()
