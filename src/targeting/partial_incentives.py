import snap

from src.preprocessing import graph_manager


def tpi(graph):
    # Ensure attributes can be read from the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be read from networks")

    # Make a temporary copy of the graph to make direct changes
    temp_graph = graph_manager.copy(graph)

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = dict()

    # Keep track of nodes not examined yet
    unexplored = set([node.GetId() for node in temp_graph.Nodes()])

    # Initialize values on nodes of temporary graph
    for node in temp_graph.Nodes():
        temp_graph.AddIntAttrDatN(node, 0, "incentive")

    # Perform operations until all nodes have been examined
    while len(unexplored) > 0:
        # Track whether a node with a threshold greater than its in-degree exists or not
        threshold_increased = False
        
        for node_id in unexplored:
            # Get the node iterator from its identifier
            node = temp_graph.GetNI(node_id)

            # Get current threshold and in-degree to see if condition holds
            threshold = temp_graph.GetIntAttrDatN(node, "threshold")
            in_degree = node.GetInDeg()

            if threshold > in_degree:
                # Get the current incentive for the node
                incentive = temp_graph.GetIntAttrDatN(node, "incentive")

                # Update both incentive and threshold for the node
                temp_graph.AddIntAttrDatN(node, incentive + threshold - in_degree, "incentive")
                temp_graph.AddIntAttrDatN(node, in_degree, "threshold")

                # Record a node with a threshold greater than its in-degree has been found
                threshold_increased = True

                # Remove the node if it has no more in-edges
                if in_degree == 0:
                    unexplored.remove(node_id)
                    break

        if threshold_increased:
            # Jump to the next while iteration if a node has been found having a threshold greater than its in-degree
            continue
        else:
            # Choose a vertex to remove from the graph
            candidate = dict()

            for node_id in unexplored:
                # Get the node iterator from its identifier
                node = temp_graph.GetNI(node_id)

                # Get current threshold and in-degree
                threshold = temp_graph.GetIntAttrDatN(node, "threshold")
                in_degree = node.GetInDeg()

                # Compute the index for the node and set it as candidate if condition holds
                index = (threshold * (threshold + 1)) / (in_degree * (in_degree + 1))

                if "node" not in candidate or index > candidate["index"]:
                    candidate["node"] = node
                    candidate["index"] = index

            destinations = set()

            for node_id in candidate["node"].GetOutEdges():
                # Mark the edges going out from the candidate to be removed
                destinations.add(node_id)

            for node_id in destinations:
                temp_graph.DelEdge(candidate["node"].GetId(), node_id)

            # Remove the candidate node from the set of those to be examined
            unexplored.remove(candidate["node"].GetId())

    # Compute the incentives dictionary to be returned
    incentives = dict((node.GetId(), temp_graph.GetIntAttrDatN(node, "incentive")) for node in temp_graph.Nodes())

    return incentives

