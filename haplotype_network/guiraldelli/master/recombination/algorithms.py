import guiraldelli.master.recombination.data
import pygraph.classes.graph

def recombination_network(haplotypes, recombinations):
    '''Given (a list of) recombinations, returns a haplotype network (graph)
    with distances as edges' weights.'''
    network = pygraph.classes.graph.graph()
    for recombinant_pair in recombinations:
        # adding the haplotypes of the pair in the network as nodes
        for haplotype in recombinant_pair.haplotypes:
            try:
                network.add_node(haplotype)
            except pygraph.classes.exceptions.AdditionError:
                pass
        # adding the edges with mutational distance as edge weight
        try:
            # NOTE: what's the best edge weight to use?
            #  (1) (len(haplotypes[haplotypes.keys()[0]]) - (recombinant_pair.number_recombinations * recombinant_pair.average_size_recombinations))
            #  (2) number_recombinations
            #  
            #  I'm using (2).
            network.add_edge(tuple(recombinant_pair.haplotypes), wt=recombinant_pair.number_recombinations)
        except pygraph.classes.exceptions.AdditionError:
            # TODO: must think what to do. May be I should update the edge weight if it is smaller than the existing one
            pass
    return network


def percentage_equal_substring_in_range(haplotypes, substring, start_index, end_index):
    # TODO: review this function and see if it is doing what is proposed to
    percentage = 0
    for haplotype in haplotypes.keys():
        # NOTE: it will count, by purpose, the haplotypes in analysis
        if haplotypes[haplotype][start_index:(end_index + 1)] == substring:
            percentage = percentage + 1
        else:
            pass
    return float(percentage / len(haplotypes.keys()))

def find_recombinations(haplotypes):
    # TODO: find common substrings
    recombinations = list()
    tested_pairs = list()
    for haplotype in haplotypes.keys():
        for other_haplotype in haplotypes.keys():
            if other_haplotype != haplotype:
                pair = set()
                pair.add(haplotype)
                pair.add(other_haplotype)
                if (pair not in tested_pairs):
                    tested_pairs.append(pair)
                    common_substrings_indexes = common_substrings(haplotypes[haplotype], haplotypes[other_haplotype])
                    # verify the common substrings range in all the other haplotypes. If
                    #   not too common (e.g., < 50%), it is a recombinant sequence
                    number_recombinations = 0
                    average_size_recombinations = 0
                    for index_pair in common_substrings_indexes:
                        substring = haplotypes[haplotype][index_pair[0]:(index_pair[1]+1)]
                        if percentage_equal_substring_in_range(haplotypes, substring, index_pair[0], index_pair[1]) < 0.5:
                            # it's recombinant code!
                            number_recombinations = number_recombinations + 1
                            average_size_recombinations = average_size_recombinations + ((index_pair[1] + 1) - index_pair[0]);
                        else:
                            # no, it isn't!
                            pass
                    # well, it's time to added the recombination information in a data structure
                    if number_recombinations > 0:
                        # mount the data structure
                        average_size_recombinations = float(average_size_recombinations / number_recombinations);
                        pair_info = guiraldelli.master.recombination.data.Recombination()
                        pair_info.haplotypes = pair
                        pair_info.number_recombinations = number_recombinations
                        pair_info.average_size_recombinations = average_size_recombinations
                        # create a list of recombinant haplotypes, with the number of recombinant SNPs
                        recombinations.append(pair_info)
                        del pair_info
                    else:
                        # do not mount the data structure
                        pass
                    # HACK: do I need to delete the other data structures?
                else:
                    # pair already tested
                    pass
            else:
                # why would I test recombination against me?
                pass
    return recombinations

def common_substrings(one_string, other_string):
    '''Returns a list of the common substrings between two haplotypes'''
    common = list()
    substring_minimum_size = int(0.1 * len(one_string))
    substring_maximum_size = int(0.5 * len(one_string))
    start_index = None
    end_index = None
    for index in range(0, len(one_string)):
        if one_string[index] == other_string[index]:
            if start_index == None:
                start_index = index
            end_index = index
        else:
            if start_index == None or end_index == None:
                pass
            # similar string has ended, and do accept strings with size 2
            elif start_index != end_index and end_index == (index - 1) and (end_index - start_index) > substring_minimum_size and  (end_index - start_index) < substring_maximum_size:
                common.append((start_index, end_index))
                start_index = None
            else:
                pass
    return common

def add_to_symbols_table(string, start_index, end_index):
    '''Add entry in the symbols table, watching for conflicts (multiple
    insertion of the same string)'''
    # stating the global variables I will have to use
    global haplotypes
    substring = string[start_index:(end_index + 1)]
    if type(substring) is types.ListType:
        substring = ''.join(substring)
    # mounting the symbols table entry
    symbols_table_entry = dict()
    symbols_table_entry['frequency'] = float(0)
    symbols_table_entry['range'] = [start_index, end_index]
    symbols_table_entry['competing'] = find_all_substrings_in_range(start_index, end_index)
    # updating the frequency
    symbols_table_entry['frequency'] = symbols_table_entry['competing'][substring]
    # removing the self-reference in the competing substrings group
    del symbols_table_entry['competing'][substring]
    if symbols_table.has_key(substring):
        if type(symbols_table[substring]) is types.ListType:
            # verify if the content is not already in the list
            entry_already_exist = False
            for existing_entry in symbols_table[substring]:
                if existing_entry['range'] == [start_index, end_index]:
                    entry_already_exist = True
                else:
                    pass
            if entry_already_exist == False:
                # add the new entry to the list
                symbols_table[substring].append(symbols_table_entry)
        elif symbols_table[substring]['range'] != [start_index, end_index]:
            # conflict happened: we have the same substring elsewhere in the sequence
            entry = symbols_table[substring]
            list_of_entries = list()
            list_of_entries.append(entry)
            list_of_entries.append(symbols_table_entry)
            symbols_table[substring] = list_of_entries
        else:
            # nothing to do since frequency was alread updated
            pass
    else:
        # add the new entry to the symbols table
        symbols_table[substring] = symbols_table_entry

def fetch_from_symbols_table(string, start_index, end_index):
    '''Fetch elements from symbols table'''
    substring = string[start_index:(end_index + 1)]
    if type(substring) is types.ListType:
        substring = ''.join(substring)
    if symbols_table.has_key(substring) == False:
        return None
    else:
        if type(symbols_table[substring]) is types.ListType:
            # if exists more than one entry
            for entry in symbols_table[substring]:
                if entry['range'] == [start_index, end_index]:
                    return entry
                else:
                    pass
            # if the code reaches this point, it did not found an entry
            # so, return None
            return None
        elif symbols_table[substring]['range'] == [start_index, end_index]:
            # if the entry is what we are looking for
            return symbols_table[substring]
        else:
            # nothing was found
            return None

def find_all_substrings_in_range(start_index, end_index):
    '''Finds all the substrings in a given range and determine
    their frequencies'''
    # stating the global variables I will have to use
    global haplotypes
    competing_substrings = dict()
    frequency_step = float(1) / len(haplotypes.keys())
    for each in haplotypes.keys():
        substring = haplotypes[each][start_index:(end_index + 1)]
        # converting from list of characters to string
        substring = ''.join(substring)
        if competing_substrings.has_key(substring):
            competing_substrings[substring] += frequency_step
        else:
            competing_substrings[substring] = frequency_step
    return competing_substrings

