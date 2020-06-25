import math
import snap

from src.preprocessing import graphs_manager


def degree_frac(graph, budget, seed):
    """Selects each vertex fractionally proportional to its degree."""

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = dict()

    # Compute the fractional budget based on the number of edges and keep track of the amount spent
    budget_fraction = budget / graph.GetEdges()
    spent = 0

    # Set initial incentives to be proportional to the out-degree of each node
    for node in graph.Nodes():
        node_budget = math.floor(budget_fraction * node.GetOutDeg())

        incentives[node.GetId()] = node_budget
        spent += node_budget

    # Set snap random seed to be able to reproduce results
    snap.TRnd(seed)

    # Get the remainder unassigned budget and add it randomly
    remainder = budget - spent

    for i in range(0, remainder):
        incentives[graph.GetRndNId()] += 1

    return incentives


def discount_frac(graph, thresholds, budget):
    """Selects the vertex having the highest degree at each step and assigns to it a budged equal to the minimum
       amount that allows to activate it.
    """

    # Initialize the target set with the empty set and the unexplored set with the whole set of nodes in the graph
    target = set()
    unexplored = set([node.GetId() for node in graph.Nodes()])

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = dict((node.GetId(), 0) for node in graph.Nodes())

    while budget > 0 and len(target) < graph.GetNodes():
        candidate = dict()

        # Find the node with most neighbors not yet activated
        for node_id in unexplored:
            node = graph.GetNI(node_id)

            destinations = set(node.GetOutEdges())
            degree = len(destinations.difference(target))

            if "node" not in candidate or degree > candidate["degree"]:
                candidate["node"] = node
                candidate["degree"] = degree

        # Compute node index
        threshold = thresholds[candidate["node"].GetId()]
        sources = set(candidate["node"].GetInEdges())

        index = max(0, threshold - len(sources.intersection(target)))

        # Compute node incentive and update budgets
        incentive = min(budget, index)

        incentives[candidate["node"].GetId()] = incentive
        budget -= incentive

        # Add the node to the target set
        unexplored.remove(candidate["node"].GetId())
        target.add(candidate["node"].GetId())

    return incentives


def tpi(graph, thresholds):

    # Make a temporary copy of the graph to make direct changes
    temp_graph = graphs_manager.copy(graph)
    temp_thresholds = thresholds.copy()

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = dict((node.GetId(), 0) for node in graph.Nodes())

    # Keep track of nodes not examined yet
    unexplored = set([node.GetId() for node in temp_graph.Nodes()])

    # Perform operations until all nodes have been examined
    while len(unexplored) > 0:
        # Track whether a node with a threshold greater than its in-degree exists or not
        threshold_increased = False
        
        for node_id in unexplored:
            # Get the node iterator from its identifier
            node = temp_graph.GetNI(node_id)

            # Get current threshold and in-degree to see if condition holds
            threshold = temp_thresholds[node.GetId()]
            in_degree = node.GetInDeg()

            if threshold > in_degree:
                # Get the current incentive for the node
                incentive = incentives[node.GetId()]

                # Update both incentive and threshold for the node
                incentives[node.GetId()] = incentive + threshold - in_degree
                temp_thresholds[node.GetId()] = in_degree

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
                threshold = temp_thresholds[node.GetId()]
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

    return incentives

