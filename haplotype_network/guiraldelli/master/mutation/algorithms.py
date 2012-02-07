from data import Mutation
import pygraph.classes.graph

def find_mutations(haplotypes):
    '''Given (a dictionary of) haplotypes, return a list (of Mutation)
    with mutational information about the haplotypes.'''
    mutations = list()
    tested_pairs = list()
    for haplotype in haplotypes.keys():
        for other_haplotype in haplotypes.keys():
            count = 0
            if other_haplotype != haplotype:
                pair = set()
                pair.add(haplotype)
                pair.add(other_haplotype)
                if (pair not in tested_pairs):
                    tested_pairs.append(pair)
                    pair_info = Mutation()
                    pair_info.haplotypes = pair
                    for i in range(0,len(haplotypes[haplotype])):
                        if haplotypes[haplotype][i] != haplotypes[other_haplotype][i]:
                            count = count + 1
                            pair_info.differences.append(i)
                            #print "(%s,%s): difference found on %dth index!" % (haplotype, other_haplotype, i)
                    #print "(%s,%s): %d" % (haplotype, other_haplotype, count)
                    pair_info.count = count
                    mutations.append(pair_info)
                    # HACK: do I need to delete the other data structures?
                    del pair_info
    return mutations

def mutational_network(mutations):
    '''Given (a list of) mutations, returns a haplotype network (graph)
    with mutational distances as edges' weight.'''
    network = pygraph.classes.graph.graph()
    for mutational_pair in mutations:
        # adding the haplotypes of the pair in the network as nodes
        for haplotype in mutational_pair.haplotypes:
            try:
                network.add_node(haplotype)
            except pygraph.classes.exceptions.AdditionError:
                pass
        # adding the edges with mutational distance as edge weight
        try:
            network.add_edge(tuple(mutational_pair.haplotypes), wt=mutational_pair.count)
        except pygraph.classes.exceptions.AdditionError:
            # TODO: must think what to do. May be I should update the edge weight if it is smaller than the existing one
            pass
    return network
