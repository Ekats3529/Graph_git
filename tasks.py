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
INF = 1e15


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
        print("Graph is not directed")
        return
    global color, cycle
    cycle = False
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
    d = [-1 for _ in range(len(gr.nodes_list))]
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
        if max(d) + 1 <= k and d.count(-1) == 1:
            ans.append(node)
        # print(node, d, p)
    print(f"The list of vertexes which shortest way to others <= {k}: {' '.join(ans)}")


def search(gr, parent, i):
    if parent[gr.nodes_list.index(i)] == i:
        return i
    return search(gr, parent, parent[gr.nodes_list.index(i)])


def apply_union(gr, parent, rank, x, y):
    xroot = search(gr, parent, x)
    yroot = search(gr, parent, y)
    if rank[gr.nodes_list.index(xroot)] < rank[gr.nodes_list.index(yroot)]:
        parent[gr.nodes_list.index(xroot)] = yroot
    elif rank[gr.nodes_list.index(xroot)] > rank[gr.nodes_list.index(yroot)]:
        parent[gr.nodes_list.index(yroot)] = xroot
    else:
        parent[gr.nodes_list.index(yroot)] = xroot
        rank[gr.nodes_list.index(xroot)] += 1


def kruskal(graph):
    if graph.type == "directed":
        print("ERROR: Incorrect type of graph")
        return
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
            if i > len(edge_list) - 1:
                print("EROOR: Can't build the tree")
                return
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
    result_weight = 0
    for u, v, weight in result:
        result_weight += int(weight)
        print(f"({u}, {v}) - {weight}")
    print(f"Weight of all graph: {result_weight}")


# Вывести длины кратчайших путей от u до v1 и v2.
def dijkstra(graph, s):
    gr = graph.copy()
    n = len(gr.nodes_list)
    d = [INF] * n
    pr = [0] * n
    d[gr.nodes_list.index(s)] = 0
    used = [False for _ in range(len(gr.nodes_list))]
    for i in range(n):
        v = -1
        for j in range(n):
            if not used[j] and (v == -1 or d[j] < d[v]):
                v = j
        if d[v] == INF:
            break
        used[v] = True
        lst = gr.adj_list[gr.nodes_list[v]]
        for nd in lst:
            to = gr.nodes_list.index(nd[0])
            ln = int(nd[1])
            if d[v] + ln < d[to]:
                d[to] = d[v] + ln
                pr[to] = v
    return d, pr


def bellman_ford(graph, s):
    gr = graph.copy()
    n = len(gr.nodes_list)
    d = [INF] * n
    d[gr.nodes_list.index(s)] = 0
    edges = gr.create_edge_list(True)
    pr = [0] * n
    # print(edges)
    m = len(edges)
    while True:
        flag = False
        for j in range(m):
            e = edges[j]
            a = gr.nodes_list.index(e[0])
            b = gr.nodes_list.index(e[1])
            cost = int(e[2])
            if d[a] < INF:
                if d[b] > d[a] + cost:
                    d[b] = d[a] + cost
                    pr[b] = a
                    flag = True
        if not flag:
            break
    return d, pr


def create_matrix_adj(gr):
    n = len(gr.adj_list)
    A = [[INF if i != j else 0 for i in range(n)] for j in range(n)]
    for x in gr.adj_list:
        a = gr.nodes_list.index(x)
        for v in gr.adj_list[x]:
            b = gr.nodes_list.index(v[0])
            cost = int(v[-1])
            A[a][b] = cost
            if gr.type == "!directed":
                A[b][a] = cost
    return A


def create_matrix_pr(gr):
    n = len(gr.adj_list)
    pr = [[None for i in range(n)] for j in range(n)]
    for x in gr.adj_list:
        a = gr.nodes_list.index(x)
        for v in gr.adj_list[x]:
            b = gr.nodes_list.index(v[0])
            pr[a][b] = a
            if gr.type == "!directed":
                pr[b][a] = b
    return pr


def print_matrix(A):
    for x in A:
        for y in x:
            if y == INF:
                print(f"{'INF': ^5}", end=" ")
            else:
                print(f"{'None' if y is None else y: ^5}", end=" ")
        print()


def floyd(graph):
    gr = graph.copy()
    n = len(gr.adj_list)
    A = create_matrix_adj(gr)
    cycle = False
    pr = create_matrix_pr(gr)
    for k in range(n):
        for v in range(n):
            for u in range(n):
                if A[v][k] != INF and A[k][u] != INF and A[v][k] + A[k][u] < A[v][u]:
                    A[v][u] = A[v][k] + A[k][u]
                    pr[v][u] = pr[k][u]
                    # print(pr[v][u], pr[v][k], pr[k][u])
            if A[v][v] < 0:
                cycle = True
                # print('Negative-weight cycle found')
                # return
        # print(k)
        # print_matrix(A)
        # print()
        # print_matrix(pr)
        # print()
    # print_matrix(pr)
    return A, pr, cycle


