import tasks
from graph import Graph

commands_num = {"1": "CREATE EMPTY", "2": "CREATE FILE", "3": "COPY", "4": "CHOOSE GRAPH",
                "5": "ADD VERTEX", "6": "ADD EDGE", "7": "DELETE VERTEX", "8": "DELETE EDGE",
                "9": "PRINT LIST EDGES FILE", "10": "PRINT LIST EDGES CONSOLE", "11": "PRINT ADJACENCY LIST CONSOLE",
                "13": "HELP", "14": "PRINT LIST COMMANDS", "15": "PRINT LIST GRAPHS", "0": "EXIT",
                "100": "IN DEGREE", "101": "TASK Ib 18", "102": "ACYCLE", "103": "K_PATH"}

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
            "ACYCLE": "-",
            "K_PATH": "-"
            }

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
                    print(cur_graph.create_edge_list())

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
                        print(tasks.k_path(cur_graph, k))
                    except ValueError:
                        print("ERROR Value of k is not integer")

        print("\nENTER THE COMMAND: ", end="")
        command = input()