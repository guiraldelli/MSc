import pygraph.classes.graph
import pygraph.classes.exceptions
import sys
import logging
import md5

logging.basicConfig()
logger = logging.getLogger('guiraldelli.master.unification.algorithms')
logger.setLevel(logging.INFO)

def graphs_unification(graphs_universe):
    '''Compose a final graph by the 'selected edges' of the graphs
    beloning to the universe of graphs.'''
    logger = logging.getLogger('guiraldelli.master.unification.algorithms.graphs_unification')
    logger.setLevel(logging.INFO)
    final_graph = pygraph.classes.graph.graph()
    final_graph.add_nodes(vertices(graphs_universe))
    for one_vertix in final_graph.nodes():
        for other_vertix in final_graph.nodes():
            if one_vertix != other_vertix:
                minimum_weight = minimum_weighted_edge(one_vertix, other_vertix, graphs_universe)
                logger.debug('For edge (%s, %s) minimum weight is %s.', one_vertix, other_vertix, minimum_weight)
                if minimum_weight != None:
                    try:
                        final_graph.add_edge((one_vertix, other_vertix), wt=minimum_weight)
                    except pygraph.classes.exceptions.AdditionError:
                        pass
                else:
                    pass
    return final_graph

def vertices(graphs_universe):
    '''Compose a list of vertices that should be added in the final graph
    by all the vertices existing in the graphs of the universe of graphs.'''
    vertices = list()
    for graph in graphs_universe:
        for vertix in graph.nodes():
            if vertix not in vertices:
                vertices.append(vertix)
            else:
                pass
    return vertices

def minimum_weighted_edge(one_vertix, other_vertix, graphs_universe):
    '''Find the minimum weigthed edge and returns the minimum weight to
    compose a new edge in the final graph.'''
    logger = logging.getLogger('guiraldelli.master.unification.algorithms.minimum_weighted_edge')
    logger.setLevel(logging.WARN)
    inspection_edge = (one_vertix, other_vertix)
    minimum_weight = None
    for graph in graphs_universe:
        if graph.has_edge(inspection_edge):
            if minimum_weight == None or graph.edge_weight(inspection_edge) < minimum_weight:
                minimum_weight = graph.edge_weight(inspection_edge)
                logger.info("Selected edge from the graph %s.", md5.new(str(graph)).hexdigest())
                # NOTE: there is no need to receive the edge
            else:
                pass
        else:
            pass
    logger.debug('For edge (%s, %s) minimum weight is %s.', one_vertix, other_vertix, minimum_weight)
    return minimum_weight
