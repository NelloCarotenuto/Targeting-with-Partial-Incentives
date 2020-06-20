import random
import snap


BASE_SEED = 1


def set_random(graph, seed):
    """Sets a random activation threshold for every edge of the graph."""

    # Ensure attributes can be set on the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be added to networks")

    # Set the random seed to be able to reproduce results
    random.seed(BASE_SEED + seed)

    # Generate a random threshold for each edge in the graph and add it
    for destination in graph.Nodes():
        for source in destination.GetInEdges():
            edge = graph.GetEI(source, destination.GetId())
            threshold = random.uniform(0, 1)

            graph.AddFltAttrDatE(edge, threshold, "threshold")


def set_degree_proportional(graph):
    """Sets a threshold proportional to the degree of the node."""

    # Ensure attributes can be set on the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be added to networks")

    # Compute the threshold based on the in-degree of each node and add it to its edges
    for destination in graph.Nodes():
        degree = destination.GetInDeg()
        threshold = 1 / degree

        for source in destination.GetInEdges():
            edge = graph.GetEI(source, destination.GetId())
            graph.AddFltAttrDatE(edge, threshold, "threshold")

