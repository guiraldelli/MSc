import pyparsing
import os.path
import logging

logging.basicConfig()

nodes_count = "Nodes: " + pyparsing.Word(pyparsing.nums)
edges_count = "Edges: " + pyparsing.Word(pyparsing.nums)
weigthed_edge = "(('" + pyparsing.Word(pyparsing.alphanums + "-_. ") + "', '" + pyparsing.Word(pyparsing.alphanums + "-_. ") + "'), " + pyparsing.Word(pyparsing.nums) + ")"

def process_filename(nexus_filename, extension=".txt", suffix_final="_final", suffix_mutational="_mutation", suffix_recombination="_recombination", suffix_data_analyzed="_data_analyzed"):
    filename = None
    if nexus_filename[-4:] == ".nex":
        filename = nexus_filename[0:-4]
        return (filename + suffix_final + extension, filename + suffix_mutational + extension, filename + suffix_recombination + extension, filename + suffix_data_analyzed + ".csv")
    else:
        return None

def process_file(filename):
    logger = logging.getLogger('data_analyzer.process_file')
    logger.setLevel(logging.INFO)
    file = open(filename, 'r')
    number_nodes = int(nodes_count.parseString(file.readline())[1])
    number_edges = int(edges_count.parseString(file.readline())[1])
    nodes = set()
    edges = dict()
    for edge in file.readlines():
        logger.debug(edge)
        parsed = weigthed_edge.parseString(edge)
        nodes.add(parsed[1])
        nodes.add(parsed[3])
        edges[ parsed[1] + "," + parsed[3]  ] = parsed[5]
    if number_nodes != len(nodes):
        message = 'For file %s, number of declared NODES (%d) is DIFFERENT from the number of EXISTING ones (%d).' % (filename, number_edges, len(edges))
        logger.warn(message)
    if number_edges != len(edges.keys()):
        message = 'For file %s, number of declared EDGES (%d) is DIFFERENT from the number of EXISTING ones (%d).' % (filename, number_edges, len(edges))
        logger.warn(message)
    return (nodes, edges)

def process_nodes(final_nodes, mutation_nodes, recombination_nodes):
    logger = logging.getLogger('data_analyzer.process_nodes')
    logger.setLevel(logging.INFO)
    mutation_and_recombination = 0
    mutation_and_final = 0
    recombination_and_final = 0
    mutation_and_recombination_and_final = 0
    nodes = set()
    nodes = nodes.union(final_nodes, mutation_nodes, recombination_nodes)
    for node in nodes:
        if node in mutation_nodes and node in recombination_nodes:
            mutation_and_recombination += 1
            if node in final_nodes:
                mutation_and_recombination_and_final += 1
                mutation_and_final += 1
                recombination_and_final += 1
            else:
                logger.error("Node " + node + " found but not in the final graph!")
        elif node in mutation_nodes and node in final_nodes:
            mutation_and_final += 1
        elif node in recombination_nodes and node in final_nodes:
            recombination_and_final += 1
        else:
            logger.error("Node " + node + " found but not in the final graph!")
    ret = (len(mutation_nodes), len(recombination_nodes), len(final_nodes), mutation_and_recombination, mutation_and_final, recombination_and_final, mutation_and_recombination_and_final)
    return ret
            
def process_edges(final_edges, mutation_edges, recombination_edges):
    logger = logging.getLogger('data_analyzer.process_edges')
    logger.setLevel(logging.INFO)
    mutation_and_recombination = 0
    mutation_and_final = 0
    recombination_and_final = 0
    mutation_and_recombination_and_final = 0
    edges = set()
    edges = edges.union(final_edges.keys(), mutation_edges.keys(), recombination_edges.keys())
    for edge in edges:
        if edge in mutation_edges.keys() and edge in recombination_edges.keys():
            mutation_and_recombination += 1
            if edge in final_edges.keys():
                mutation_and_recombination_and_final += 1
                mutation_and_final += 1
                recombination_and_final += 1
            else:
                logger.error("Edge " + edge + " found but not in the final graph!")
        elif edge in mutation_edges.keys() and edge in final_edges.keys():
            mutation_and_final += 1
        elif edge in recombination_edges.keys() and edge in final_edges.keys():
            recombination_and_final += 1
        else:
            logger.error("Edge " + edge + " found but not in the final graph!")
    ret = (len(mutation_edges.keys()), len(recombination_edges.keys()), len(final_edges.keys()), mutation_and_recombination, mutation_and_final, recombination_and_final, mutation_and_recombination_and_final)
    return ret

# def process_edges(final_edges, mutation_edges, recombination_edges):
#     data = { 'mutation':{'common':0, 'same':0, 'not':0, 'refused':0}, 'recombination':{'common':0, 'same':0, 'not':0, 'refused':0}}
#     # data['mutation']['common'] = 0
#     # data['mutation']['same'] = 0
#     # data['mutation']['not'] = 0
#     # data['mutation']['refused'] = 0
#     # data['recombination']['common'] = 0
#     # data['recombination']['same'] = 0
#     # data['recombination']['not'] = 0
#     # data['recombination']['refused'] = 0
#     for edge in final_edges.keys():
#         if edge in mutation_edges.keys():
#             data['mutation']['common'] += 1
#             if final_edges[edge] == mutation_edges[edge]:
#                 data['mutation']['same'] += 1
#             else:
#                 data['mutation']['refused'] += 1
#         else:
#             data['mutation']['not'] += 1
#         if edge in recombination_edges.keys():
#             data['recombination']['common'] += 1
#             if final_edges[edge] == recombination_edges[edge]:
#                 data['recombination']['same'] += 1
#             else:
#                 data['recombination']['refused'] += 1
#         else:
#             data['recombination']['not'] += 1
#     return data

def process_weights(final_edges, mutation_edges, recombination_edges):
    logger = logging.getLogger('data_analyzer.process_weights')
    logger.setLevel(logging.INFO)
    mutation_and_recombination = 0
    mutation_and_final = 0
    recombination_and_final = 0
    mutation_and_recombination_and_final = 0
    edges = set()
    edges = edges.union(final_edges.keys(), mutation_edges.keys(), recombination_edges.keys())
    for edge in edges:
        if edge in mutation_edges.keys() and edge in recombination_edges.keys() and mutation_edges[edge] == recombination_edges[edge]:
            mutation_and_recombination += 1
            if edge in final_edges.keys() and mutation_edges[edge] == final_edges[edge] and recombination_edges[edge] == final_edges[edge]:
                mutation_and_recombination_and_final += 1
                mutation_and_final += 1
                recombination_and_final += 1
            else:
                logger.error("Edge " + edge + " has a value that is not equal to final, mutation and recombination when it should be!")
        elif edge in mutation_edges.keys() and edge in final_edges.keys() and mutation_edges[edge] == final_edges[edge]:
            mutation_and_final += 1
        elif edge in recombination_edges.keys() and edge in final_edges.keys() and recombination_edges[edge] == final_edges[edge]:
            recombination_and_final += 1
        else:
            logger.error("Edge " + edge + " found but its value not compatible when it should be!")
    ret = (mutation_and_recombination, mutation_and_final, recombination_and_final, mutation_and_recombination_and_final)
    return ret

def write_header(file):
    header_file = '''"Nexus File"'''
    header_nodes = '''"N(M)","N(R)","N(F)","N(M) and N(R)","N(M) and N(F)","N(R) and N(F)","N(M) and N(R) and N(F)"'''
    header_edges = '''"E(M)","E(R)","E(F)","E(M) and E(R)","E(M) and E(F)","E(R) and E(F)","E(M) and E(R) and E(F)"'''
    header_weights = '''"w(M) = w(R)","w(M) = w(F)","w(R) = w(F)","w(M) = w(R) = w(F)"'''
    column_separator = ","
    new_line = "\n"
    file.write(header_file + column_separator + header_nodes + column_separator + header_edges + column_separator + header_weights + new_line)
    file.flush()


def analyze_data(filepath_open, filepath_save):
    logger = logging.getLogger('data_analyzer.analyze_data')
    logger.setLevel(logging.INFO)
    final_filename, mutation_filename, recombination_filename, data_analyzed_filename = process_filename(filepath_open)
    # overwriting data_analyzed_filename
    data_analyzed_filename = filepath_save
    final_nodes, final_edges = process_file(final_filename)
    mutation_nodes, mutation_edges = process_file(mutation_filename)
    recombination_nodes, recombination_edges = process_file(recombination_filename)
    data_analyzed = process_edges(final_edges, mutation_edges, recombination_edges)
    # saving data
    if os.path.exists(data_analyzed_filename):
        file = open(data_analyzed_filename, 'a')
        logger.warn("File '" + data_analyzed_filename + "' exists; appending data in this file.")
    else:
        file = open(data_analyzed_filename, 'w')
        logger.info("Creating file '" + data_analyzed_filename + "'.")
        write_header(file)
    # getting information
    nodes_info = process_nodes(final_nodes, mutation_nodes, recombination_nodes)
    edges_info = process_edges(final_edges, mutation_edges, recombination_edges)
    weights_info = process_weights(final_edges, mutation_edges, recombination_edges)
    # writing to file
    file.write('''"''' + filepath_open + '''",''')
    for info in nodes_info:
        file.write(str(info))
        file.write(",")
    for info in edges_info:
        file.write(str(info))
        file.write(",")
    for info in weights_info:
        file.write(str(info))
        file.write(",")
    file.write("\n")
    # file.write("%d,%d,%d,%d,%d,%d,%d,") % (nodes_info[0], nodes_info[1], nodes_info[2], nodes_info[3], nodes_info[4], nodes_info[5], nodes_info[6])
    # file.write("%d,%d,%d,%d,%d,%d,%d,") % (edges_info[0], edges_info[1], edges_info[2], edges_info[3], edges_info[4], edges_info[5], edges_info[6])
    # file.write("%d,%d,%d,%d\n") % (weights_info[0], weights_info[1], weights_info[2], weights_info[3])
    # # printing to screen
    # print nodes_info
    # print edges_info
    # print weights_info
    # file.write("'Graph','Node','Edges'")
    # file.write("\n")
    # file.write("'%s',%d,%d" % ("Final", len(final_nodes), len(final_edges.keys())))
    # file.write("\n")
    # file.write("'%s',%d,%d" % ("Mutation", len(mutation_nodes), len(mutation_edges.keys())))
    # file.write("\n")
    # file.write("'%s',%d,%d" % ("Recombination", len(recombination_nodes), len(recombination_edges.keys())))
    # file.write("\n")
    # file.write("\n")
    # file.write("'Graph','Common Edges','Same Edges', 'Not Have Edges','Refused Edges'")
    # file.write("\n")
    # for graph_type in data_analyzed.keys():
    #     file.write("'%s'" % (graph_type.capitalize()))
    #     file.write(",%d" % (data_analyzed[graph_type]['common']))
    #     file.write(",%d" % (data_analyzed[graph_type]['same']))
    #     file.write(",%d" % (data_analyzed[graph_type]['not']))
    #     file.write(",%d" % (data_analyzed[graph_type]['refused']))
    #     for property in data_analyzed[graph_type].keys():
    #         logger.debug("data_analyzed[%s][%s] = %d" % (graph_type, property, data_analyzed[graph_type][property]))
    #     file.write("\n")
    file.close()
    logger.info("Data analysis has ended!")
