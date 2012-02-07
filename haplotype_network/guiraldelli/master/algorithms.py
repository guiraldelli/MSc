import pygraph.classes.graph
import pygraph.algorithms.minmax

def extract_minimum_spanning_tree(weighted_graph):
    '''Extracts the minimum spanning tree using the function provided by pygraph.algorithms.minmax module.
    For this reason, a dictionary, not a graph, is returned.'''
    return pygraph.algorithms.minmax.minimal_spanning_tree(weighted_graph)

def minimal_spanning_tree(weighted_graph):
    # TODO: implement this!
    mst_dictionary = extract_minimum_spanning_tree(weighted_graph)
    minimum_spanning_tree = pygraph.classes.graph.graph()
    minimum_spanning_tree.add_nodes(mst_dictionary.keys())
    for one_vertex in mst_dictionary.keys():
        if mst_dictionary[one_vertex] == None:
            continue
        other_vertex = mst_dictionary[one_vertex]
        edge = (one_vertex, other_vertex)
        minimum_spanning_tree.add_edge(edge, wt=weighted_graph.edge_weight(edge))
    return minimum_spanning_tree
