import math
import random


__BASE_SEED = 1


def constant_thresholds(graph, value):
    """Sets a constant threshold for every node of the graph."""

    # Store threshold assignment in a dictionary
    thresholds = dict()

    # Add a constant attribute to each node
    for node in graph.Nodes():
        thresholds[node.GetId()] = value

    return thresholds


def degree_proportional_thresholds(graph, fraction=0.5):
    """Sets a threshold for every node of the graph to be proportional to its in-degree."""

    # Store threshold assignment in a dictionary
    thresholds = dict()

    # Compute the threshold based on the in-degree and add it to every node
    for node in graph.Nodes():
        degree = node.GetInDeg()
        threshold = math.floor(degree * fraction) + 1

        thresholds[node.GetId()] = threshold

    return thresholds


def random_thresholds(graph, seed):
    """Sets a threshold for every node of the graph to be a random integer between 1 and its degree."""

    # Store threshold assignment in a dictionary
    thresholds = dict()

    # Set the random seed to be able to reproduce results
    random.seed(__BASE_SEED + seed)

    # Add a random attribute to each node
    for node in graph.Nodes():
        thresholds[node.GetId()] = random.randint(1, node.GetDeg())

    return thresholds

