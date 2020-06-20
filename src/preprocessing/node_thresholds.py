import math
import snap


def set_constant(graph, constant):
    """Sets a constant threshold to every node of the graph."""

    # Ensure attributes can be set on the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be added to networks")

    # Add a constant attribute to each node
    for node in graph.Nodes():
        graph.AddIntAttrDatN(node, constant, "threshold")


def set_degree_proportional(graph, fraction=0.5):
    """Sets a threshold proportional to the in-degree to every node of the graph."""

    # Ensure attributes can be set on the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be added to networks")

    # Compute the threshold based on the in-degree and add it to every node
    for node in graph.Nodes():
        degree = node.GetInDeg()
        threshold = math.floor(degree * fraction) + 1

        graph.AddIntAttrDatN(node, threshold, "threshold")

