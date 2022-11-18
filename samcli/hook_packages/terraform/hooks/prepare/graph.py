import networkx

from samcli.hook_packages.terraform.hooks.prepare.resource_linking import LAMBDA_LAYER_RESOURCE_ADDRESS_PREFIX


__GRAPH__ = None

def _clean(address: str):
    # index of 8 to skip "[root]"
    # remove "(expand)" text

    # this is an assumption of the format of the node values
    return address.strip()[8:-1].replace(" (expand)", "")

def _first_pass(lines: "list[str]"):
    """
    First pass to parse initial dot file contents
    """
    DELIM = " -> "

    nodes = {}
    
    for line in lines:
        if DELIM in line:
            a, b = line.split(DELIM, 2)

            a = _clean(a)
            b = _clean(b)

            children = nodes.get(a, [])
            if b not in children and a != b:
                children.append(b)

            nodes[a] = children

    return nodes
            
def _second_pass(nodes: dict):
    """
    Second pass to resolve "(close)" nodes
    """
    import copy

    new_nodes: dict = copy.deepcopy(nodes)

    for node, child_nodes in nodes.items():
        for child_node in child_nodes:
            if " (close)" in child_node:
                new_nodes.get(node).remove(child_node)
                new_nodes.get(node).append(nodes.get(child_node)[0])

    for node in nodes:
        if " (close)" in node:
            del new_nodes[node]

    return new_nodes

def _generate_graph(nodes: dict):
    graph = networkx.DiGraph()
    for node, children in nodes.items():
        for child in children:
            graph.add_edge(node, child)

    return graph

def parse_output(lines: "list[str]"):
    global __GRAPH__
    __GRAPH__ = _generate_graph(_second_pass(_first_pass(lines)))

def find(start: str):
    global __GRAPH__
    for _, b in networkx.bfs_edges(__GRAPH__, start):
        if LAMBDA_LAYER_RESOURCE_ADDRESS_PREFIX in b:
            return b

    return None