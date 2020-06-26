import os
import pickle
import snap

from src.definitions import ROOT_DIR

__RAW_DIR = f"{ROOT_DIR}/data/raw"
__PROCESSED_DIR = f"{ROOT_DIR}/data/processed"


def __init_dirs():
    """Creates data directories if they don't exist."""

    # Create directory for raw data if not exists
    os.makedirs(__RAW_DIR, exist_ok=True)

    # Create directory for processed graphs if not exists
    os.makedirs(__PROCESSED_DIR, exist_ok=True)


def load_graph(file_name, graph_type="directed", file_type="TXT", processed=False):
    """Simply loads a raw/processed graph from .csv, .txt or .graph files from data directory."""

    # Set the base directory
    if processed:
        base_dir = __PROCESSED_DIR
    else:
        base_dir = __RAW_DIR

    # Check that the file exists
    if not os.path.isfile(f"{base_dir}/{file_name}"):
        raise Exception(f"File {base_dir}/{file_name} does not exist")

    # Set the proper graph type for SNAP
    if graph_type == "undirected":
        graph_snap_type = snap.PUNGraph
    elif graph_type == "directed":
        graph_snap_type = snap.PNGraph
    elif graph_type == "network":
        graph_snap_type = snap.PNEANet
    else:
        raise Exception(f"Graphs of type {graph_type} are not supported")

    # Read the file according to the specified file format
    if file_type == "CSV":
        if not file_name.endswith(".csv"):
            raise Exception("File name must end with .csv extension for CSV files")

        return snap.LoadEdgeList(graph_snap_type, f"{base_dir}/{file_name}", 0, 1, ",")
    elif file_type == "TXT":
        if not file_name.endswith(".txt"):
            raise Exception("File name must end with .txt extension for TXT files")

        return snap.LoadEdgeList(graph_snap_type, f"{base_dir}/{file_name}", 0, 1)
    elif file_type == "binary":
        if not file_name.endswith(".graph"):
            raise Exception("File name must end with .graph extension for binary files")

        file_input = snap.TFIn(f"{base_dir}/{file_name}")

        if graph_type == "undirected":
            return snap.TUNGraph.Load(file_input)
        elif graph_type == "directed":
            return snap.TNGraph.Load(file_input)
        elif graph_type == "network":
            return snap.TNEANet.Load(file_input)
        else:
            raise Exception(f"Graphs of type {graph_type} are not supported")
    else:
        raise Exception(f"Files of type {file_type} are not supported")


def store_graph(graph, file_name, file_type="binary", processed=True):
    """Simply stores a graph to data directory in .txt or .graph formats."""

    # Set the base directory
    if processed:
        base_dir = __PROCESSED_DIR
    else:
        base_dir = __RAW_DIR

    # Store the graph according to the specified file format
    if file_type == "TXT":
        if not file_name.endswith(".txt"):
            raise Exception("File name must end with .txt extension for TXT files")

        snap.SaveEdgeList(graph, f"{base_dir}/{file_name}")
    elif file_type == "binary":
        if not file_name.endswith(".graph"):
            raise Exception("File name must end with .graph extension for binary files")

        file_output = snap.TFOut(f"{base_dir}/{file_name}")
        graph.Save(file_output)
        file_output.Flush()
    else:
        raise Exception(f"Files of type {file_type} are not supported")


def copy_graph(graph):
    """Simply clones a graph."""

    return snap.ConvertGraph(type(graph), graph)


def store_node_thresholds(thresholds, file_name):
    """Dumps node thresholds to a pickle."""

    # Ensure thresholds are stored in a dict
    if not isinstance(thresholds, dict):
        raise Exception("Thresholds should be stored in a dictionary")

    if not file_name.endswith(".node.thresholds"):
        raise Exception("File name must end with .node.thresholds extension")

    with open(f"{__PROCESSED_DIR}/{file_name}", "wb") as file:
        pickle.dump(thresholds, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_node_thresholds(file_name):
    """Loads node thresholds from a pickle."""

    with open(f"{__PROCESSED_DIR}/{file_name}", "rb") as file:
        thresholds = pickle.load(file)

    return thresholds


def store_incentives(incentives, file_name):
    """Dumps node incentives to a pickle."""

    # Ensure incentives are stored in a dict
    if not isinstance(incentives, dict):
        raise Exception("Incentives should be stored in a dictionary")

    if not file_name.endswith(".incentives"):
        raise Exception("File name must end with .incentives extension")

    with open(f"{__PROCESSED_DIR}/{file_name}", "wb") as file:
        pickle.dump(incentives, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_incentives(file_name):
    """Loads node incentives from a pickle."""

    with open(f"{__PROCESSED_DIR}/{file_name}", "rb") as file:
        incentives = pickle.load(file)

    return incentives
