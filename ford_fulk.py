from dataclasses import dataclass
from graph import Graph


visited = []
pred = []

network = []
flow_edges = []


@dataclass
class Edge:
    source: str
    target: str
    capacity: int
    flow: int


def find_path(graph, v):
    visited[graph.nodes_list.index(v)] = True
    for e in network[graph.nodes_list.index(v)]:
        u = flow_edges[e].target
        if not visited[graph.nodes_list.index(u)] and flow_edges[e].capacity - flow_edges[e].flow > 0:
            pred[graph.nodes_list.index(u)] = e
            find_path(graph, u)


def build_network(graph):
    for v in graph.nodes_list:
        for u, cu in graph.adj_list[v]:
            network[graph.nodes_list.index(v)].append(len(flow_edges))
            flow_edges.append(Edge(source=v, target=u, capacity=int(cu), flow=0))
            network[graph.nodes_list.index(u)].append(len(flow_edges))
            flow_edges.append(Edge(source=u, target=v, capacity=0, flow=0))


def ford_fulkerson(graph, s, t):
    global n, visited, pred, network, flow_edges
    n = len(graph.nodes_list)

    visited = [False for _ in range(n)]
    pred = [None for _ in range(n)]

    network = [[] for v in range(n)]
    flow_edges = []

    if s == t:
        return None

    build_network(graph)
    # print(network, flow_edges)

    result_flow = 0

    while True:
        for v in graph.nodes_list:
            visited[graph.nodes_list.index(v)] = False
            pred[graph.nodes_list.index(v)] = None

        find_path(graph, s)
        if not visited[graph.nodes_list.index(t)]:
            break

        path = []
        while pred[graph.nodes_list.index(v)] is not None:
            e = pred[graph.nodes_list.index(v)]
            path.append(e)
            v = flow_edges[e].source

        flow = flow_edges[path[0]].capacity - flow_edges[path[0]].flow
        for e in path:
            flow = min(flow, flow_edges[e].capacity - flow_edges[e].flow)

        for e in path:
            edge = flow_edges[e]
            edge.flow += flow

            edge = flow_edges[e ^ 1]
            edge.flow -= flow

        result_flow += flow

    return result_flow



