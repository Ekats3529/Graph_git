from graph import Graph
from queue import Queue


def in_deg(graph, node):
    if node not in graph.nodes_list:
        print(f"No such vertex {node}")
        return -1
    ans = 0
    neib = []
    for item in graph.adj_list.items():
        nodes = [x[0] for x in item[1]]
        if node in nodes:
            neib.append(item[0])
            ans += 1
    return ans, neib


def new_graph(graph):
    gr = graph.copy()
    del_nodes = []
    for node in gr.adj_list.items():
        if len(node[1]) % 2 != 0:
            del_nodes.append(node[0])
    for node in del_nodes:
        gr.delete_node(node)
    return gr


color = []
cycle = False


def dfs(node, gr):
    global color, cycle
    color[gr.nodes_list.index(node)] = 1
    lst = [x[0] for x in gr.adj_list[node]]
    for nd in lst:
        if color[gr.nodes_list.index(nd)] == 0:
            dfs(nd, gr)
        elif color[gr.nodes_list.index(nd)] == 1:
            cycle = True

    color[gr.nodes_list.index(node)] = 2


def acycle(graph):
    if graph.type == "!directed":
        print("Graph is directed")
        return
    global color, cycle
    gr = graph.copy()
    color = [0 for _ in range(len(gr.nodes_list))]
    for node in gr.nodes_list:
        if color[gr.nodes_list.index(node)] == 0:
            dfs(node, gr)
    if cycle:
        return False
    return True


def bfs(s, gr):
    used = [False for _ in range(len(gr.nodes_list))]
    d = [0 for _ in range(len(gr.nodes_list))]
    p = [None for _ in range(len(gr.nodes_list))]
    used[gr.nodes_list.index(s)] = True
    q = Queue()
    q.put(s)
    while not q.empty():
        node = q.get()
        lst = [x[0] for x in gr.adj_list[node]]
        for nd in lst:
            to = gr.nodes_list.index(nd)
            if not used[to]:
                used[to] = True
                q.put(nd)
                d[to] = d[gr.nodes_list.index(node)] + 1
                p[to] = node
    return d, p


def k_path(graph, k):
    gr = graph.copy()
    ans = []
    for node in gr.nodes_list:
        d, p = bfs(node, gr)
        if max(d) <= k:
            ans.append(node)
        # print(node, d, p)
    print(f"The list of vertexes which shortest way to others <= {k}: {' '.join(ans)}")


def search(graph, parent, i):
    if parent[gr.nodes_list.index(i)] == i:
        return i
    return search(graph, parent, parent[gr.nodes_list.index(i)])


def apply_union(graph, parent, rank, x, y):
    xroot = search(graph, parent, x)
    yroot = search(graph, parent, y)
    if rank[gr.nodes_list.index(xroot)] < rank[gr.nodes_list.index(yroot)]:
        parent[gr.nodes_list.index(xroot)] = yroot
    elif rank[gr.nodes_list.index(xroot)] > rank[gr.nodes_list.index(yroot)]:
        parent[gr.nodes_list.index(yroot)] = xroot
    else:
        parent[gr.nodes_list.index(yroot)] = xroot
        rank[gr.nodes_list.index(xroot)] += 1


def kruskal(graph):
    gr = graph.copy()
    n = len(gr.nodes_list)
    result = []
    i, j = 0, 0
    edge_list = gr.create_edge_list(False)
    parent = [gr.nodes_list[i] for i in range(n)]
    rank = [0 for _ in range(n)]
    try:
        edge_list = sorted(edge_list, key=lambda item: int(item[2]))
        while j < n - 1:
            u, v, w = edge_list[i]
            i += 1
            x = search(graph, parent, u)
            y = search(graph, parent, v)
            if x != y:
                j += 1
                result.append([u, v, w])
                apply_union(graph, parent, rank, x, y)
    except ValueError:
        print("ERROR: Incorrect type of weight")
        return
    for u, v, weight in result:
        print(f"({u}, {v}) - {weight}")


gr = Graph()
gr.create_from_file("kr.txt")
kruskal(gr)
