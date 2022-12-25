import time

import tasks
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
from pyvis.network import Network


# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtCore import QTimer
from graph import Graph
import networkx as nx
from PyQt5 import uic

gr = Graph()


# main window
# which inherits QDialog
class Window(QDialog):

    # constructor
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('new_interface.ui', self)
        self.setWindowTitle('Graph Visualizer')
        self.fig = plt.figure(1)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

        self.pushButton_graph.clicked.connect(self.show_graph)
        self.pushButton_bfs.clicked.connect(self.bfs)
        self.pushButton_dfs.clicked.connect(self.dfs)
        self.pushButton_kruskal.clicked.connect(self.kruskal)

        self.pushButton.clicked.connect(self.ok)

        self.cur = None
        self.opt = None

        self.fig_dial = plt.figure(2)
        self.canvas_dial = FigureCanvas(self.fig_dial)

    def clear(self):
        for ax in self.fig.axes:
            ax.clear()
        self.label_put.setText("")
        self.label_weight.setText("")
        self.label_tree.setText("")
        self.canvas.draw()

    def ok(self):
        p = str(self.lineEdit.text())

        if p not in gr.nodes_list:
            self.label_put.setText("ERROR")

        else:
            if self.opt == "bfs":
                new_gr = nx.bfs_tree(self.cur, source=p)
                options = {
                    'node_color': '#b5b8b1',
                    'node_size': 170,
                    'width': 2,
                    'arrowstyle': '-|>',
                    'arrowsize': 10,
                    'edge_color': "red",
                }
            else:
                new_gr = nx.dfs_tree(self.cur, source=p)
                options = {
                    'node_color': '#b5b8b1',
                    'node_size': 170,
                    'width': 2,
                    'arrowstyle': '-|>',
                    'arrowsize': 10,
                    'edge_color': "#7fb5b5",
                }
            pos = nx.planar_layout(self.cur)
            arr = False
            if gr.type == "directed":
                arr = True

            options1 = {
                'node_color': '#a2add0',
                'node_size': 170,
                'width': 2,
                'arrowstyle': '-|>',
                'arrowsize': 10,
            }
            nx.draw_networkx(self.cur, pos=pos, arrows=arr, **options1)
            nx.draw_networkx(new_gr, pos=pos, arrows=True, **options)
            if gr.weighted:
                edge_labels = nx.get_edge_attributes(self.cur, "weight")

                nx.draw_networkx_edge_labels(self.cur, pos, edge_labels)

            self.canvas.draw()

            DialTree = DialogTree(self, self.fig_dial, self.canvas_dial, self.opt, [new_gr, pos, options])
            DialTree.show()
            DialTree.exec()

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
        # plt.show()
        self.canvas.draw()

    def bfs(self):
        self.clear()

        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])

        self.label_put.setText("Enter sourse of BFS ")

        self.opt = "bfs"
        self.cur = G

    def dfs(self):
        self.clear()

        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])

        self.label_put.setText("Enter sourse of DFS ")

        self.opt = "dfs"
        self.cur = G

    def kruskal(self):
        self.clear()

        G = nx.Graph()
        edges = [tuple([x[0], x[1], int(x[2])]) for x in gr.create_edge_list(False)]
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[-1])

        res, weig = tasks.kruskal(gr)

        for i in range(len(res)):
            res[i][-1] = int(res[i][-1])
            res[i] = tuple(res[i])

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
        try:
            nx.draw_networkx(G, pos=pos, **options1)
            nx.draw_networkx(krus, pos=pos, **options)
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels)
            self.label_weight.setText(f"Weight of all graph: {weig}")
            s = ""
            for u, v, weight in res:
                s += f"({u}, {v}) - {weight}\n"
            self.label_tree.setText(s)

            self.canvas.draw()

            DialTree = DialogTree(self, self.fig_dial, self.canvas_dial, "krus", [krus, pos, options])
            DialTree.show()
            DialTree.exec()

        except Exception as e:
            print(e)


class DialogTree(QDialog):
    def __init__(self, mainwindow, fig_dial, canvas_dial, type, opt):
        super().__init__()
        uic.loadUi('tree.ui', self)

        self.mainwindow = mainwindow

        self.setWindowTitle('Separate Tree')
        self.fig = fig_dial
        self.canvas = canvas_dial

        self.horizontalLayout.addWidget(self.canvas)

        if type == "krus":
            self.kruskal(opt)
        else:
            self.dfs_bfs(opt)

    def clear(self):
        for ax in self.fig.axes:
            ax.clear()
        self.canvas.draw()

    def kruskal(self, opt):
        self.clear()
        Gr, pos, options = opt[0], opt[1], opt[-1]
        nx.draw_networkx(Gr, pos=pos, **options)
        edge_labels = nx.get_edge_attributes(Gr, "weight")
        nx.draw_networkx_edge_labels(Gr, pos, edge_labels)
        self.canvas.draw()

    def dfs_bfs(self, opt):
        self.clear()

        Gr, pos, options = opt[0], opt[1], opt[2]
        nx.draw_networkx(Gr, pos=pos, arrows=True, **options)

        self.canvas.draw()


def visualize(graph):
    global gr
    gr = graph.copy()
    app = QApplication(sys.argv)
    main = Window()
    main.show()
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
