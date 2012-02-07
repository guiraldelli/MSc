#!/usr/bin/env python
from Tkinter import *
import tkFileDialog
import generator
import control

class App:
    def __init__(self, master):
        frame_1 = Frame(master)
        frame_2 = Frame(master)
        frame_3 = Frame(master)
        frame_4 = Frame(master)
        # creating widgets
        self.label_number_haplotypes = Label(frame_1, text="How many haplotypes?")
        self.entry_number_haplotypes = Entry(frame_1, width=5)
        self.label_haplotype_length = Label(frame_2, text="How long will be each sequence?")
        self.entry_haplotype_length = Entry(frame_2, width=5)
        self.label_rate = Label(frame_3, text="Rate in %:")
        self.slider_mutation_rate = Scale(frame_3, from_=0, to=100, orient=HORIZONTAL, label="Mutation", command=self.command_slider_mutation_rate)
        self.slider_recombination_rate = Scale(frame_3, from_=0, to=100, orient=HORIZONTAL, label="Recombination", command=self.command_slider_recombination_rate)
        self.button_generate_sequence = Button(frame_4, text="Generate!", command=self.command_button_generate_sequence)
        # configuring widgets
        self.entry_number_haplotypes.insert(0,20)
        self.entry_haplotype_length.insert(0,100)
        self.slider_mutation_rate.set(50)
        self.slider_recombination_rate.set(50)
        # packing widgets
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        self.label_number_haplotypes.pack(side=LEFT)
        self.entry_number_haplotypes.pack(side=LEFT)
        self.label_haplotype_length.pack(side=LEFT)
        self.entry_haplotype_length.pack(side=LEFT)
        self.label_rate.pack(side=TOP)
        self.slider_mutation_rate.pack(side=LEFT)
        self.slider_recombination_rate.pack(side=LEFT)
        self.button_generate_sequence.pack(side=TOP)

    def command_slider_mutation_rate(self, value):
        self.slider_recombination_rate.set(100-int(value))

    def command_slider_recombination_rate(self, value):
        self.slider_mutation_rate.set(100-int(value))

    def command_button_generate_sequence(self):
        haplotype_length = int(self.entry_haplotype_length.get())
        total_number = int(self.entry_number_haplotypes.get())
        mutation_rate = int(self.slider_mutation_rate.get())
        recombination_rate = int(self.slider_recombination_rate.get())
        control.generate_sequence(haplotype_length, total_number, mutation_rate, recombination_rate)
        file_path = tkFileDialog.asksaveasfilename(filetypes=[("Nexus", "*.nex")], title="Save File As...")
        # TODO: if file_path does not end with '.nex', add it
        control.save_file(file_path)


root = Tk()
app = App(root)
root.mainloop()
