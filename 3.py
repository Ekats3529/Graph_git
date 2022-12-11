# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from graph import Graph
import networkx as nx



gr = Graph()
gr.create_from_file("a.txt")


# main window
# which inherits QDialog
class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

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
        #self.button_graph.clicked.connect(self.show_graph)

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

    def show_graph(self):
        G = nx.Graph()
        edges = [tuple([x[0], x[1]]) for x in gr.create_edge_list(False)]
        print(1)
        num_nodes = len(gr.nodes_list)

        G.add_nodes_from(gr.nodes_list)
        G.add_edges_from(edges)
        bfs = nx.bfs_tree(G, source="6")
        print(bfs)
        pos = nx.planar_layout(G)

        nx.draw(G, pos)
        # nx.draw(bfs, pos)
        nx.draw_networkx_labels(G, pos)

        self.canvas.draw()



# driver code
if __name__ == "__main__":
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())


