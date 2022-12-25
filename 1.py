import tasks
# from dash import Dash, html, dcc
# import plotly.express as px
# import plotly.graph_objs as go
# from pyvis.network import Network


# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from graph import Graph
import networkx as nx

gr = Graph()


# main window
# which inherits QDialog
class Window(QDialog):

    # constructor
    def __init__(self):
        super(Window, self).__init__()

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the "figure"it takes the
        # "figure" instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to "plot" method
        self.button_graph = QPushButton("Graph")
        self.button_bfs = QPushButton("BFS")
        self.button_dfs = QPushButton("DFS")
        self.button_kruskal = QPushButton("KRUSKAL")

        self.button_graph.clicked.connect(self.show_graph)
        self.button_bfs.clicked.connect(self.bfs)
        self.button_dfs.clicked.connect(self.dfs)
        self.button_kruskal.clicked.connect(self.kruskal)
        # self.button_graph.clicked.connect(self.show_graph)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        layout.addWidget(self.button_graph)
        layout.addWidget(self.button_bfs)
        layout.addWidget(self.button_dfs)
        layout.addWidget(self.button_kruskal)

        # setting layout to the main window
        self.setLayout(layout)

    # action called by thte push button

    def clear(self):
        for ax in self.figure.axes:
            ax.clear()
        self.canvas.draw()

    def show_graph(self):
        self.clear()
        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])
        pos = nx.planar_layout(G)

        arr = False
        if gr.type == "directed":
            arr = True
        options = {
            'node_color': '#a2add0',
            'node_size': 170,
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 10,
        }

        nx.draw_networkx(G, pos=pos, arrows=arr, **options)
        if gr.weighted:
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)
        self.canvas.draw()

    def bfs(self):
        self.clear()
        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])
        print("Enter sourse of BFS ")
        s = input()
        if s not in gr.nodes_list:
            print("ERROR")
        else:

            bfs = nx.bfs_tree(G, source=s)
            pos = nx.planar_layout(G)
            arr = False
            if gr.type == "directed":
                arr = True
            options = {
                'node_color': '#b5b8b1',
                'node_size': 170,
                'width': 2,
                'arrowstyle': '-|>',
                'arrowsize': 10,
                'edge_color': "#7fb5b5",
            }
            options1 = {
                'node_color': '#a2add0',
                'node_size': 170,
                'width': 2,
                'arrowstyle': '-|>',
                'arrowsize': 10,
            }
            nx.draw_networkx(G, pos=pos, arrows=arr, **options1)
            nx.draw_networkx(bfs, pos=pos, arrows=True, **options)
            if gr.weighted:
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)

        self.canvas.draw()

    def dfs(self):
        self.clear()
        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])
        print("Enter sourse of DFS ")
        p = input()
        if p not in gr.nodes_list:
            print("ERROR")
        else:
            dfs = nx.dfs_tree(G, source=p)
            pos = nx.planar_layout(G)
            arr = False
            if gr.type == "directed":
                arr = True
            options = {
                'node_color': '#b5b8b1',
                'node_size': 170,
                'width': 2,
                'arrowstyle': '-|>',
                'arrowsize': 10,
                'edge_color': "red",
            }
            options1 = {
                'node_color': '#a2add0',
                'node_size': 170,
                'width': 2,
                'arrowstyle': '-|>',
                'arrowsize': 10,
            }
            nx.draw_networkx(G, pos=pos, arrows=arr, **options1)
            nx.draw_networkx(dfs, pos=pos, arrows=True, **options)
            if gr.weighted:
                edge_labels = nx.get_edge_attributes(G, "weight")
                nx.draw_networkx_edge_labels(G, pos, edge_labels)

        self.canvas.draw()

    def kruskal(self):
        self.clear()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        res, wei = tasks.kruskal(gr)

        for i in range(len(res)):
            res[i][-1] = int(res[i][-1])
            res[i] = tuple(res[i])

        G = nx.Graph()
        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])

        pos = nx.planar_layout(G)

        krus = nx.Graph()
        krus.add_nodes_from(gr.nodes_list)
        for edge in res:
            krus.add_edge(edge[0], edge[1], weight=edge[-1])

        options = {
            'node_color': '#a2add0',
            'node_size': 170,
            'width': 2,
            'edge_color': "#e76f51",
        }
        options1 = {
            'node_color': '#a2add0',
            'node_size': 170,
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 10,
        }
        if gr.type == "directed":
            arr = True
        nx.draw_networkx(G, pos=pos, arrows=arr, **options1)
        try:
            nx.draw_networkx(krus, pos=pos, **options)
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)

        except Exception as e:
            print(e)

        self.canvas.draw()


def visualize(graph):
    global gr
    gr = graph.copy()

    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())


# def visualize_web(graph):
#     gr = graph.copy()
#     G = nx.Graph()
#     edges = [tuple([x[0], x[1]]) for x in gr.create_edge_list(False)]
#
#     num_nodes = len(gr.nodes_list)
#     G.add_nodes_from(gr.nodes_list)
#     G.add_edges_from(edges)
#
#     net = Network(notebook=True, cdn_resources='remote')
#     nt = Network('1000px', '1000px', notebook=True, cdn_resources='remote')
#     nt.from_nx(G)
#     nt.show_buttons(filter_=True)
#     nt.show('graph.html')


gr.create_from_file("kr.txt")
visualize(gr)
