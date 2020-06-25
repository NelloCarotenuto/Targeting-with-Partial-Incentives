import random


__BASE_SEED = 1


def random_thresholds(graph, seed):
    """Sets a random activation threshold for every edge of the graph."""

    # Store threshold assignment in a dictionary
    thresholds = dict()

    # Set the random seed to be able to reproduce results
    random.seed(__BASE_SEED + seed)

    # Generate a random threshold for each edge in the graph and add it
    for destination in graph.Nodes():
        for source in destination.GetInEdges():
            edge = graph.GetEI(source, destination.GetId())
            threshold = random.uniform(0, 1)

            thresholds[edge.GetId()] = threshold

    return thresholds


def degree_proportional_thresholds(graph):
    """Sets the activation threshold for each edge to be proportional to the degree of the destination node."""

    # Store threshold assignment in a dictionary
    thresholds = dict()

    # Compute the threshold based on the in-degree of each node and add it to its edges
    for destination in graph.Nodes():
        degree = destination.GetInDeg()

        if degree == 0:
            continue

        threshold = 1 / degree

        for source in destination.GetInEdges():
            edge = graph.GetEI(source, destination.GetId())
            thresholds[edge.GetId()] = threshold

    return thresholds

