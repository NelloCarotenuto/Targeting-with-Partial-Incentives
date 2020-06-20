import random
import snap

from src.preprocessing import graph_manager


BASE_SEED = -1


def prune_randomly(graph, seed):
    """Removes edges from the graph by generating random numbers and comparing them to their activation thresholds."""

    # Ensure attributes can be read from the graph
    if not isinstance(graph, snap.PNEANet):
        raise Exception("Attributes can only be added to networks")

    # Make a copy of the graph
    new_graph = graph_manager.copy(graph)

    # Set the random seed to be able to reproduce results
    random.seed(BASE_SEED - seed)

    # Traverse the graph and remove edges randomly
    for destination in new_graph.Nodes():
        edges_to_remove = []

        for source in destination.GetInEdges():
            edge = new_graph.GetEI(source, destination.GetId())
            value = random.uniform(0, 1)

            threshold = new_graph.GetFltAttrDatE(edge, "threshold")

            if value < threshold:
                edges_to_remove.append(edge.GetId())

        for edge in edges_to_remove:
            new_graph.DelEdge(edge)

    return new_graph

