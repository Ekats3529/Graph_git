from copy import deepcopy


class Graph:
    adj_list = {}   # список смежности
    type = "!directed"      # тип графа: ориентированный или нет
    weighted = False    # тип графа: взвешенный или нет
    nodes_list = []     # список вершин

    # инициализация графа
    def __init__(self, *attributes):
        self.adj_list = {}
        if len(attributes) > 0:
            self.type = attributes[0]
            self.weighted = True if attributes[1] == "weighted" else False

    # метод для создания списка ребер
    def create_edge_list(self, dublicate):
        edge_list = []

        if not dublicate:
            edges = []
            for node in self.adj_list.keys():
                for adj in self.adj_list[node]:
                    if [node, adj[0]] not in edges:
                        edges.append([adj[0], node])
                        edge_list.append([node, adj[0], adj[1]])
        else:
            for node in self.adj_list.keys():
                for adj in self.adj_list[node]:
                    edge_list.append([node, adj[0], adj[1]])

        return edge_list

    # метод для создания графа из файла
    def create_from_file(self, filename):
        adj_list = {}
        try:
            fin = open(filename, encoding="utf8")
        except FileNotFoundError:
            print("ERROR: No such file or directory")
            return False

        self.type = fin.readline().split()[0]
        self.weighted = True if fin.readline().split()[0] == "weighted" else False
        n, m = map(int, fin.readline().split())
        self.nodes_list = fin.readline().split()

        for node in self.nodes_list:
                adj_list[node] = []

        edges = fin.readlines()
        for edge in edges:
            v, u, c = edge.split()
            try:
                if v == u and self.type == "!directed":
                    print(f"ERROR: No loop in not directed graph")
                    return False
                if u in self.nodes_list:
                    if u not in adj_list[v]:
                        adj_list[v].append([u, c])
                    else:
                        print(f"ERROR: No multiple edges")
                        return False
                else:
                    print(f"ERROR: No such vertex {u}")
                    return False
            except KeyError:
                print(f"ERROR: No such vertex {v}")
                return False

            if self.type == "!directed":
                try:
                    if v in self.nodes_list:
                        if u not in adj_list[v]:
                            adj_list[u].append([v, c])
                        else:
                            print(f"ERROR: No multiple edges")
                            return False
                    else:
                        print(f"ERROR: No such vertex {v}")
                        return False
                except KeyError:
                    print(f"ERROR: No such vertex {u}")
                    return False

        self.adj_list = adj_list
        return True

    # метод для создания копии графа
    def copy(self):
        cp_graph = Graph(self.type, "weighted" if self.weighted else "!weighted")
        cp_graph.adj_list = deepcopy(self.adj_list)
        cp_graph.nodes_list = self.nodes_list.copy()
        return cp_graph

    # метод для добавления вершины
    def add_node(self, node):
        if node in self.nodes_list:
            print(f"ERROR: Unable to add vertex {node}. The same vertex already exist")
            return False
        self.adj_list[node] = []
        self.nodes_list.append(node)
        return True

    # метод для добавления ребра (дуги)
    def add_edge(self, edge):
        if len(edge) < 2:
            print(f"Unable to add the edge")
            return False
        v, u = edge[0], edge[1]
        c = '1'
        fl = False
        if self.weighted:
            try:
                c = edge[2]
            except (KeyError, IndexError):
                print(f"Unable to add the edge. No weight entered")
                return False
        else:
            if len(edge) == 3:
                print("This graph is not weighted, so the weight of this edge not counted")
        try:
            if self.weighted:
                if v == u and self.type == "!directed":
                    print(f"Unable to add the edge. No loop in not directed graph")
                    return False
                nodes = [x[0] for x in self.adj_list[v]]
                if u in nodes:
                    print(f"Do you want to change the weight of edge {v} {u} "
                          f"from {self.adj_list[v][nodes.index(u)][1]} to {c} "
                          f"Y/N")
                    ans = input()
                    if ans == "Y":
                        fl = True
                        self.adj_list[v][nodes.index(u)][1] = c
                else:
                    if u in self.nodes_list and v in self.nodes_list:
                        self.adj_list[v].append([u, c])
                    else:
                        print(f"Unable to add the edge. No such vertex")
                        return False
            else:
                if v == u and self.type == "!directed":
                    print(f"Unable to add the edge. No loop in not directed graph")
                    return False
                if [u, c] not in self.adj_list[v]:
                    if u in self.nodes_list and v in self.nodes_list:
                        self.adj_list[v].append([u, c])
                    else:
                        print(f"Unable to add the edge. No such vertex")
                        return False
                else:
                    print(f"Unable to add the edge. Same edge already exists")
                    return False

        except KeyError:
            print(f"Unable to add the edge. No such vertex {v}")
            return False

        if self.type != "directed":
            try:
                if self.weighted:

                    nodes = [x[0] for x in self.adj_list[u]]
                    if v in nodes:
                        if fl:
                            self.adj_list[u][nodes.index(v)][1] = c
                    else:
                        if u in self.nodes_list and v in self.nodes_list:
                            self.adj_list[u].append([v, c])
                        else:
                            print(f"Unable to add the edge. No such vertex")
                            return False
                else:
                    if [v, c] not in self.adj_list[u]:
                        if u in self.nodes_list and v in self.nodes_list:
                            self.adj_list[u].append([v, c])
                        else:
                            print(f"Unable to add the edge. No such vertex")
                            return False
                    else:
                        print(f"Unable to add the edge. Same edge already exists")
                        return False
            except KeyError:
                print(f"Unable to add the edge. No such vertex {u}")
                return False
        return True

    # метод для удаления вершины
    def delete_node(self, node):
        try:
            for item in self.adj_list.items():
                nodes = [x[0] for x in item[1]]
                if node in nodes:
                    del self.adj_list[item[0]][nodes.index(node)]
            del self.adj_list[node]
            del self.nodes_list[self.nodes_list.index(node)]
        except KeyError:
            print(f"ERROR: No such vertex {node}")
            return False
        return True

    # метод для удаления ребра (дуги)
    def delete_edge(self, edge):
        v, u = edge[0], edge[1]

        try:
            nodes = [x[0] for x in self.adj_list[v]]
            del self.adj_list[v][nodes.index(u)]
        except (KeyError, ValueError):
            print(f"ERROR: No such edge ({v}, {u})")
            return False

        if self.type != "directed":
            try:
                nodes = [x[0] for x in self.adj_list[u]]
                del self.adj_list[u][nodes.index(v)]
            except (KeyError, ValueError):
                print(f"ERROR: No such edge ({u}, {v})")
                return False
        return True

    # метод для вывода графа в файл
    def print_to_file(self, filename):
        try:
            fout = open(filename, 'w', encoding="utf8")
        except FileNotFoundError:
            print("ERROR: No such file or directory")
            return False
        lst = self.create_edge_list(False)
        print(self.type, file=fout)
        print("weighted" if self.weighted else "!weighted", file=fout)
        print(len(self.nodes_list), len(lst), file=fout)
        print(" ".join(self.nodes_list), file=fout)
        for edge in lst:
            print(f"{edge[0]} {edge[1]}", file=fout)
        return True

    # метод для вывода списка смежности в консоль
    def print_to_console(self):
        print()
        if self.weighted:
            for item in self.adj_list.items():
                nodes = ["(" + ",".join([x[0], x[1]]) + ")" for x in item[1]]
                line = " ".join(nodes)
                print(f"{item[0]}: {line}")
        else:
            for item in self.adj_list.items():
                nodes = [x[0] for x in item[1]]
                line = " ".join(nodes)
                print(f"{item[0]}: {line}")
