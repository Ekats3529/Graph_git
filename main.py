import tasks
import visualisation
from graph import Graph
import ford_fulk

commands_num = {"1": "CREATE EMPTY", "2": "CREATE FILE", "3": "COPY", "4": "CHOOSE GRAPH",
                "5": "ADD VERTEX", "6": "ADD EDGE", "7": "DELETE VERTEX", "8": "DELETE EDGE",
                "9": "PRINT LIST EDGES FILE", "10": "PRINT LIST EDGES CONSOLE", "11": "PRINT ADJACENCY LIST CONSOLE",
                "13": "HELP", "14": "PRINT LIST COMMANDS", "15": "PRINT LIST GRAPHS", "0": "EXIT",
                "100": "IN DEGREE", "101": "TASK Ib 18", "102": "ACYCLE", "103": "K_PATH", "104": "KRUSKAL",
                "201": "DIJKSTRA", "202": "BELLMAN_FORD", "203": "FLOYD", "301": "FLOYD",
                "401": "FORD_FULKERSON", "501": "VISUALIZE"}

commands = {"CREATE EMPTY": "Create a new empty graph",
            "CREATE FILE": "Create a new graph from the file",
            "COPY": "Create the copy of existing graph",
            "CHOOSE GRAPH": "Choose the name if graph to work with",
            "ADD VERTEX": "Add a vertex to the graph",
            "ADD EDGE": "Add an edge to the graph",
            "DELETE VERTEX": "Remove a vertex from the graph",
            "DELETE EDGE": "Remove an edge from the graph",
            "PRINT LIST EDGES FILE": "Print list of edges to the file",
            "PRINT LIST EDGES CONSOLE": "Print list of edges to the console(there)",
            "PRINT ADJACENCY LIST CONSOLE": "Print adjacency list to the console(there)",
            "HELP": "Print the hint for the command",
            "EXIT": "Exit the execution",
            "PRINT LIST COMMANDS": "Print list of commands to the console(there)",
            "PRINT LIST GRAPHS": "Print list of graphs to the console(there)",
            "IN DEGREE": "-",
            "TASK Ib 18": "-",
            "ACYCLE": "Find out whether the graph is acycle",
            "K_PATH": "-",
            "KRUSKAL": "Find the minimum spanning tree",
            "DIJKSTRA": "Find the minimum distance from node to other nodes",
            "BELLMAN_FORD": "Find the minimum distance from node to other nodes, weights can be negative",
            "FLOYD": "Find the minimum distance from node to other nodes, weights can be negative",
            "FORD_FULKERSON": "Find the maximum flow",
            "VISUALIZE": "Creative task"}

graphs = {}
chosen_graph = None


def print_menu():
    print("Enter the command from the list")
    for items in commands_num.items():
        print(items[0], items[1])


def create(*filename):
    fl = True
    if len(filename) == 1:
        gr = Graph()
        fl = gr.create_from_file(filename[0])
    else:
        print("Enter the type of graph: directed or !directed")
        type = input()
        if type != "directed" and type != "!directed":
            print("ERROR: Unexpected type")
            return
        print("Enter the type of graph: weighted or !weighted")
        weight = input()
        if weight != "weighted" and weight != "!weighted":
            print("ERROR: Unexpected type")
            return
        gr = Graph(type, weight)

    if fl:
        print("Enter the name for the new graph")
        name = input()
        while name in graphs.keys():
            print("This name already exists. Enter another")
            name = input()
        else:
            graphs[name] = gr


def get_graph_by_name(name):
    global chosen_graph
    if name is None:
        print("Enter the name of graph or enter STOP to stop entering")
        in_name = input()
        if in_name in graphs.keys():
            chosen_graph = in_name
            return graphs[chosen_graph]
        else:
            while in_name not in graphs.keys():
                print("ERROR. Try to enter another name or STOP to stop entering")
                in_name = input()
                if in_name == "STOP":
                    chosen_graph = None
                    return None
            else:
                chosen_graph = in_name

                return graphs[chosen_graph]
    chosen_graph = name
    return graphs[name]


if __name__ == '__main__':
    print_menu()
    print("\nENTER THE COMMAND: ", end="")
    command = input()
    cur_graph = None
    while command != "EXIT" and command != "0":
        if command not in commands.keys() and command not in commands_num.keys():
            print("ERROR: UNKNOWN COMMAND")

        else:
            if command == "EXIT" or command == "0":
                exit(0)

            elif command == "HELP" or command == "13":
                fl = False
                print("To exit HELP enter STOP")
                print("Enter the name of command")
                name = input()
                while name != "STOP":
                    while name not in commands.keys():
                        if name == "STOP":
                            fl = True
                            break
                        print("Wrong value. Enter name of command again")
                        name = input()
                    else:
                        print(f"{name} : {commands[name]}")
                        print("To exit HELP enter STOP")
                    if fl:
                        break
                    print("Enter the name of command")
                    name = input()

            elif command == "CREATE EMPTY" or command == "1":
                create()

            elif command == "CHOOSE GRAPH" or command == "4":
                cur_graph = get_graph_by_name(None)

            elif command == "CREATE FILE" or command == "2":
                print("Enter the name of file")
                create(input())

            elif command == "COPY" or command == "3":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the name of the copy-graph: ", end="")
                    name = input()
                    if name not in graphs.keys():
                        graphs[name] = cur_graph.copy()
                    else:
                        while name in graphs.keys():
                            print("ERROR. Try to enter another name or STOP to stop entering")
                            name = input()
                            if name == "STOP":
                                break
                        else:
                            graphs[name] = cur_graph.copy()

            elif command == "ADD VERTEX" or command == "5":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the vertex to add: ", end="")
                    node = input()
                    cur_graph.add_node(node)

            elif command == "ADD EDGE" or command == "6":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the edge to add: ", end="")
                    edge = input().split()
                    cur_graph.add_edge(edge)

            elif command == "DELETE VERTEX" or command == "7":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the vertex to delete: ", end="")
                    node = input()
                    cur_graph.delete_node(node)

            elif command == "DELETE EDGE" or command == "8":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print('Enter the edge to delete":', end="")
                    edge = input().split()
                    cur_graph.delete_edge(edge)

            elif command == "PRINT LIST EDGES FILE" or command == "9":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the name of file")
                    filename = input()
                    cur_graph.print_to_file(filename)

            elif command == "PRINT LIST EDGES CONSOLE" or command == "10":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    lst = cur_graph.create_edge_list(False)
                    for e in lst:
                        if cur_graph.weighted:
                            print(*e)
                        else:
                            print(f"{e[0]} {e[1]}")

            elif command == "PRINT ADJACENCY LIST CONSOLE" or command == "11":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    cur_graph.print_to_console()

            elif command == "PRINT LIST COMMANDS" or command == "14":
                print_menu()

            elif command == "PRINT LIST GRAPHS" or command == "15":
                for gr in graphs.items():
                    print(f"Name: {gr[0]}\tAdjacency list: ", end="")
                    gr[1].print_to_console()
                    print()

            elif command == "IN DEGREE" or command == "100":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the node")
                    node = input()
                    ans = tasks.in_deg(cur_graph, node)
                    if ans != -1:
                        if cur_graph.type == "!directed":
                            print("This graph is not directed")
                            print(f"degree {ans[0]}\nneighbours {' '.join(ans[1])}")
                        else:
                            print(f"income degree {ans[0]}\nincome neighbours {' '.join(ans[1])}")

            elif command == "TASK Ib 18" or command == "101":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    if cur_graph.type == "directed":
                        print(f"Unable to create the new graph from {chosen_graph}")
                    else:
                        new_gr = tasks.new_graph(cur_graph)
                        new_gr.print_to_console()
                        print("Would you like to add new graph to list of graphs? Y/N")
                        ans = input()
                        if ans == "Y":
                            print("Enter the name of the new-graph: ", end="")
                            name = input()
                            if name not in graphs.keys():
                                graphs[name] = new_gr
                            else:
                                while name in graphs.keys():
                                    print("ERROR. Try to enter another name or STOP to stop entering")
                                    name = input()
                                    if name == "STOP":
                                        break
                                else:
                                    graphs[name] = new_gr
                        elif ans != "N":
                            print("Cannot recognise the answer")

            elif command == "ACYCLE" or command == "102":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    res = tasks.acycle(cur_graph)
                    if res:
                        print("Acycle")
                    elif not res:
                        print("Got a cycle")

            elif command == "K_PATH" or command == "103":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print("Enter the value of k: ", end="")
                    try:
                        k = int(input())
                        tasks.k_path(cur_graph, k)
                    except ValueError:
                        print("ERROR Value of k is not integer")

            elif command == "KRUSKAL" or command == "104":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    res, weih = tasks.kruskal(cur_graph)
                    for u, v, weight in res:
                        print(f"({u}, {v}) - {weight}")
                    print(f"Weight of all graph: {weih}")

            elif command == "DIJKSTRA" or command == "201":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print(f"Enter the node u: ", end="")
                    u = input()
                    print(f"Enter the node v1: ", end="")
                    v1 = input()
                    print(f"Enter the node v2: ", end="")
                    v2 = input()
                    if u not in cur_graph.nodes_list or v1 not in cur_graph.nodes_list or v2 not in cur_graph.nodes_list:
                        print("ERROR No such node")
                    else:
                        d, pr = tasks.dijkstra(cur_graph, u)
                        #print(d, pr)

                        if d[cur_graph.nodes_list.index(v1)] != tasks.INF:
                            print(f"min distance between {u} & {v1}: {d[cur_graph.nodes_list.index(v1)]}")
                            path = []
                            v = cur_graph.nodes_list.index(v1)
                            s = cur_graph.nodes_list.index(u)
                            while v != s:
                                path.append(cur_graph.nodes_list[v])
                                v = pr[v]
                            print(f"Path: {u}-{'-'.join(path[::-1])}")
                        else:
                            print(f"No path between {u} & {v1}")

                        if d[cur_graph.nodes_list.index(v2)] != tasks.INF:
                            print(f"min distance between {u} & {v2}: {d[cur_graph.nodes_list.index(v2)]}")
                            path = []
                            v = cur_graph.nodes_list.index(v2)
                            s = cur_graph.nodes_list.index(u)
                            while v != s:
                                path.append(cur_graph.nodes_list[v])
                                v = pr[v]
                            print(f"Path: {u}-{'-'.join(path[::-1])}")
                        else:
                            print(f"No path between {u} & {v2}")

            elif command == "BELLMAN_FORD" or command == "202":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print(f"Enter the node u: ", end="")
                    u = input()
                    if u not in cur_graph.nodes_list:
                        print("ERROR No such node")
                    else:
                        n = len(cur_graph.nodes_list)
                        for v in range(n):
                            if cur_graph.nodes_list[v] != u:
                                d, pr = tasks.bellman_ford(cur_graph, cur_graph.nodes_list[v])
                                #print(d, pr)
                                if d[cur_graph.nodes_list.index(u)] != tasks.INF:
                                    print(f"min distance between {cur_graph.nodes_list[v]} & {u}: {d[cur_graph.nodes_list.index(u)]}")
                                    path = []
                                    v1 = cur_graph.nodes_list.index(u)
                                    s = v
                                    while v1 != s:
                                        path.append(cur_graph.nodes_list[v1])
                                        v1 = pr[v1]
                                    print(f"Path: {cur_graph.nodes_list[v]}-{'-'.join(path[::-1])}")
                                else:
                                    print(f"No path between {cur_graph.nodes_list[v]} & {u}")

            elif command == "FLOYD" or command == "203":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print(f"Enter the node u: ", end="")
                    u = input()
                    print(f"Enter the node v1: ", end="")
                    v1 = input()
                    print(f"Enter the node v2: ", end="")
                    v2 = input()
                    if u not in cur_graph.nodes_list or v1 not in cur_graph.nodes_list or v2 not in cur_graph.nodes_list:
                        print("ERROR No such node")
                    else:
                        A, pr, cycle = tasks.floyd(cur_graph)
                        # print(d, pr)
                        if cycle:
                            print('Negative-weight cycle found')
                            if A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v1)] != tasks.INF:
                                print(f"min distance between {u} & {v1}: {A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v1)]}")
                            else:
                                print(f"No path between {u} & {v1}")

                            if A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v2)] != tasks.INF:
                                print(f"min distance between {u} & {v2}: {A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v2)]}")
                            else:
                                print(f"No path between {u} & {v2}")

                        else:
                            if A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v1)] != tasks.INF:
                                print(f"min distance between {u} & {v1}: {A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v1)]}")
                                path = []
                                v = cur_graph.nodes_list.index(v1)
                                s = cur_graph.nodes_list.index(u)

                                while v != s:
                                    #print(v, pr[s][v])
                                    path.append(cur_graph.nodes_list[v])
                                    v = pr[s][v]
                                print(f"Path: {u}-{'-'.join(path[::-1])}")
                            else:
                                print(f"No path between {u} & {v1}")

                            if A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v2)] != tasks.INF:
                                print(f"min distance between {u} & {v2}: {A[cur_graph.nodes_list.index(u)][cur_graph.nodes_list.index(v2)]}")
                                path = []
                                v = cur_graph.nodes_list.index(v2)
                                s = cur_graph.nodes_list.index(u)
                                while v != s:
                                    #print(v)
                                    path.append(cur_graph.nodes_list[v])
                                    v = pr[s][v]
                                print(f"Path: {u}-{'-'.join(path[::-1])}")
                            else:
                                print(f"No path between {u} & {v2}")

            elif command == "FORD_FULKERSON" or command == "401":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    print(f"Enter the node s: ", end="")
                    s = input()
                    print(f"Enter the node t: ", end="")
                    t = input()
                    if s not in cur_graph.nodes_list or t not in cur_graph.nodes_list:
                        print("ERROR No such node")
                    else:
                        print(ford_fulk.ford_fulkerson(cur_graph, s, t))

            elif command == "VISUALIZE" or command == "501":
                if cur_graph is None:
                    cur_graph = get_graph_by_name(None)
                if cur_graph is not None:
                    print(f"Current graph is: {chosen_graph}")
                    visualisation.visualize(cur_graph)

        print("\nENTER THE COMMAND: ", end="")
        command = input()
