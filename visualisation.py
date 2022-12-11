import tasks
from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from pyvis.network import Network


def visualize(graph):
    gr = graph.copy()
    net = Network(notebook=True, cdn_resources='remote')
    G = nx.Graph()
    edges = [tuple([x[0], x[1]]) for x in gr.create_edge_list(False)]
    num_nodes = len(gr.nodes_list)
    G.add_nodes_from(gr.nodes_list)
    G.add_edges_from(edges)
    bfs = nx.bfs_tree(G, source="6")
    print(bfs)
    pos = nx.planar_layout(G)

    nt = Network('1000px', '1000px', notebook=True, cdn_resources='remote')
    nt.from_nx(bfs)
    #nt.from_nx(G)
    nt.show('graph.html')


gr = Graph()
gr.create_from_file("a.txt")
visualize(gr)


# G = nx.dodecahedral_graph()
# edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
# nx.draw(G)
# plt.show()
