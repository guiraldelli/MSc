#!/usr/bin/env python
# Copyright 2011
# Author: Ricardo Henrique Gracini Guiraldelli
# E-mail: rguira at usp dot br

class Mutation:
    '''Class with information about the haplotypes and the mutational
    differences between them'''
    # Set of two haplotypes tested
    haplotypes = set()
    # List with the indexes where the (mutational) differences happen
    differences = list()
    # Number of differences betweeen them
    count = 0
    def __init__(self, one_haplotype=None, other_haplotype=None):
        self.clean_data()
        if one_haplotype != None and other_haplotype != None:
            self.haplotypes.add(one_haplotype)
            self.haplotypes.add(other_haplotype)

    def clean_data(self):
        self.haplotypes = set()
        self.differences = list()
        self.count = 0


