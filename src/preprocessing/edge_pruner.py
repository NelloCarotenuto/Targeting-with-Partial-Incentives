import random
import snap

from src.preprocessing import data_manager


__BASE_SEED = 9223372036854775807


def random_prune(graph, edge_thresholds, seed):
    """Removes edges from the graph by generating random numbers and comparing them to their activation thresholds."""

    # Make a copy of the graph
    new_graph = data_manager.copy_graph(graph)

    # Set the random seed to be able to reproduce results
    random.seed(__BASE_SEED - seed)

    # Traverse the graph and remove edges randomly
    for destination in new_graph.Nodes():
        edges_to_remove = list()

        for source in destination.GetInEdges():
            edge = new_graph.GetEI(source, destination.GetId())
            threshold = edge_thresholds[edge.GetId()]

            value = random.uniform(0, 1)

            if value < threshold:
                edges_to_remove.append(edge.GetId())

        for edge in edges_to_remove:
            if isinstance(graph, snap.PNEANet):
                new_graph.DelEdge(edge)
            else:
                new_graph.DelEdge(edge[0], edge[1])

    return new_graph

