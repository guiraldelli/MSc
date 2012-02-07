#!/usr/bin/env python
# Copyright 2011
# Author: Ricardo Henrique Gracini Guiraldelli
# E-mail: rguira at usp dot br

class Recombination:
    '''Class with information about the common substrings between haplotypes'''
    # Set of two haplotypes tested
    haplotypes = set()
    # Number of recombinations found among the pair
    number_recombinations = 0
    # Average size (of bps) of the recombination codes found among the two haplotypes
    average_size_recombinations = float(0)
    def __init__(self, one_haplotype=None, other_haplotype=None):
        self.clean_data()
        if one_haplotype != None and other_haplotype != None:
            self.haplotypes.add(one_haplotype)
            self.haplotypes.add(other_haplotype)
    
    def clean_data(self):
        self.haplotypes = set()
        self.number_recombinations = 0
        self.average_size_recombinations = float(0)


