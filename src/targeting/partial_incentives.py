import math
import snap

from src.preprocessing import data_manager


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

    # Initialize the set of unexplored nodes in a dictionary with their current number of unexplored nodes pointed
    unexplored = {node.GetId(): node.GetOutDeg() for node in graph.Nodes()}

    # Store the current number of explored nodes pointing to each node
    neighbors_explored = {node.GetId(): 0 for node in graph.Nodes()}

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = {node.GetId(): 0 for node in graph.Nodes()}

    while budget > 0 and len(unexplored) > 0:
        # Get the identifier of the node with most unexplored neighbors
        max_id = max(unexplored, key=unexplored.get)
        candidate = graph.GetNI(max_id)

        # Compute node index
        threshold = thresholds[candidate.GetId()]
        index = max(0, threshold - neighbors_explored[max_id])

        # Compute node incentive and update the budget
        incentive = min(budget, index)

        incentives[candidate.GetId()] = incentive
        budget -= incentive

        # Lower the number of unexplored neighbors for each node that points to the candidate
        for node_id in set(candidate.GetInEdges()).intersection(unexplored.keys()):
            unexplored[node_id] -= 1

        # Increase the number of explored neighbors for each node pointed by the candidate
        for node_id in candidate.GetOutEdges():
            neighbors_explored[node_id] += 1

        # Add the node to the target set
        unexplored.pop(candidate.GetId())

    return incentives


def tpi(graph, thresholds):

    # Make a temporary copy of the graph to make direct changes
    temp_graph = data_manager.copy_graph(graph)
    temp_thresholds = thresholds.copy()

    # Store incentive assignments in a dictionary indexed on nodes id
    incentives = {node.GetId(): 0 for node in graph.Nodes()}

    # Keep track of nodes not examined yet
    unexplored = {}

    for node in temp_graph.Nodes():
        # Get current threshold and in-degree
        threshold = temp_thresholds[node.GetId()]
        in_degree = node.GetInDeg()

        if in_degree == 0:
            index = threshold
        else:
            index = (threshold * (threshold + 1)) / (in_degree * (in_degree + 1))

        unexplored[node.GetId()] = index

    # Perform operations until all nodes have been examined
    while len(unexplored) > 0:
        explored = set()

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

                # Remove the node if it has no more in-edges
                if in_degree == 0:
                    explored.add(node_id)

        # Remove all nodes with 0 in-degree
        for node_id in explored:
            unexplored.pop(node_id)

        if len(unexplored) == 0:
            # Exit the loop if all nodes have been explored
            break
        else:
            # Choose a vertex to remove from the graph
            max_id = max(unexplored, key=unexplored.get)
            candidate = graph.GetNI(max_id)

            # Mark the edges going out from the candidate to be removed
            for destination in candidate.GetOutEdges():
                temp_graph.DelEdge(candidate.GetId(), destination)

            # Remove the candidate node from the set of those to be examined
            unexplored.pop(candidate.GetId())

    return incentives

