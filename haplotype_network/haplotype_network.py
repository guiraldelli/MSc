#!/usr/bin/env python
# Copyright 2011
# Author: Ricardo Henrique Gracini Guiraldelli
# E-mail: rguira at usp dot br

import nexus
import os
import string
import types
import pygraph.classes.graph
import pygraph.readwrite.dot
import pygraph.algorithms.minmax
import guiraldelli.master.mutation.algorithms
import guiraldelli.master.recombination.algorithms
import guiraldelli.master.unification.algorithms
import guiraldelli.master.algorithms

# global variables
symbols_table = dict()
competing_table = dict()
haplotypes = dict()


### FILE SYSTEM CODE ###
def select_file(path=os.curdir):
    '''Shows the files in the current directory and asks the user to
    pick one'''
    directory_list = os.listdir(path)
    files = [file for file in directory_list if os.path.isfile(file) == True]
    for i, file in enumerate(files):
        print "(%d) %s" % (i, file)
    i = None
    while (i < 0) or (i > len(files)):
        i = int(raw_input("Choose the file (number): "))
    return files[i]

def read_file(filename):
    '''Read the Nexus file'''
    return nexus.NexusReader(filename)

def save_graph_dot(filename, graph, weighted=True):
    file = open(filename, 'w')
    dot = pygraph.readwrite.dot.write(graph, weighted)
    file.write(dot)
    file.close()

def save_graph_text(filename, graph):
    file = open(filename, 'w')
    file.write("Nodes: " + str(len(graph.nodes())))
    file.write("\n")
    file.write("Edges: " + str(len(graph.edges())/2))
    file.write("\n")
    edges_saved = list()
    for edge in sorted(graph.edges()):
        pair = set()
        pair.add(edge[0])
        pair.add(edge[1])
        if pair not in edges_saved:
            edges_saved.append(pair)
            edge_to_save = "(%s, %d)" % (edge, graph.edge_weight(edge))
            file.write(edge_to_save)
            file.write("\n")
        else:
            pass

def save_graph_tex(filename, graph):
    # TODO: implement this!
    pass

### ABSTRACTION CODE ###
def group_sequences(nexus):
    '''Given the nucleotide sequences, group them in sets if their are equal'''
    groups = list()
    visited_keys = set()
    for key in nexus.data.matrix.keys():
        same_haplotype = list()
        for key_compare in nexus.data.matrix.keys():
            if nexus.data.matrix[key] == nexus.data.matrix[key_compare] and key_compare not in visited_keys:
                same_haplotype.append(key_compare)
                visited_keys.add(key_compare)
        # if same_haplotype is not empty, add to the groups list
        if same_haplotype != list():
            groups.append(same_haplotype)
    return groups

def groups_to_haplotypes(groups, nexus):
    '''Create a dictionary of haplotypes, naming them by numbers'''
    haplotypes = dict()
    for i, group in enumerate(groups):
        #haplotypes[i+1] = nexus.data.matrix[group[0]]
        haplotypes[group[0]] = nexus.data.matrix[group[0]]
    return haplotypes

def analyze_data(filename_open, filename_save, save_dot=False, save_text=True, save_tex=False, save_mst=False):
    nexus = read_file(filename_open)
    haplotypes = groups_to_haplotypes(group_sequences(nexus), nexus)
    # mutation verification
    mutations = guiraldelli.master.mutation.algorithms.find_mutations(haplotypes)
    # generate the mutation network
    mutational_network = guiraldelli.master.mutation.algorithms.mutational_network(mutations)
    # recombination verification
    recombinations = guiraldelli.master.recombination.algorithms.find_recombinations(haplotypes)
    # generate the recombination network
    recombination_network = guiraldelli.master.recombination.algorithms.recombination_network(haplotypes, recombinations)
    # unifying the networks
    final_graph = guiraldelli.master.unification.algorithms.graphs_unification([mutational_network, recombination_network])
    # save the graphs in files
    if save_dot:
        save_graph_dot(filename_save + "_final.dot", final_graph)
        save_graph_dot(filename_save + "_mutation.dot", mutational_network)
        save_graph_dot(filename_save + "_recombination.dot", recombination_network)
    if save_text:
        save_graph_text(filename_save + "_final.txt", final_graph)
        save_graph_text(filename_save + "_mutation.txt", mutational_network)
        save_graph_text(filename_save + "_recombination.txt", recombination_network)
    if save_tex:
        save_graph_tex(filename_save + "_final.tex", final_graph)
        save_graph_tex(filename_save + "_mutation.tex", mutational_network)
        save_graph_tex(filename_save + "_recombination.tex", recombination_network)
    if save_mst:
        save_graph_dot(filename_save + "_minimumSpanningTree_final.dot", guiraldelli.master.algorithms.minimal_spanning_tree(final_graph))
        save_graph_dot(filename_save + "_minimumSpanningTree_mutation.dot", guiraldelli.master.algorithms.minimal_spanning_tree(mutational_network))
        save_graph_dot(filename_save + "_minimumSpanningTree_recombination.dot", guiraldelli.master.algorithms.minimal_spanning_tree(recombination_network))
    # the end
