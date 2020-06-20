import os.path as path
import snap


RAW_DATA_DIR = "../../data/raw"
PROCESSED_DATA_DIR = "../../data/processed"


def load(file_name, graph_type="network", file_type="TXT", processed=False):
    """Simply loads a raw/processed graph from .csv, .txt or .graph files from data directory."""

    # Set the base directory
    if processed:
        base_dir = PROCESSED_DATA_DIR
    else:
        base_dir = RAW_DATA_DIR

    # Check that the file exists
    if not path.isfile(f"{base_dir}/{file_name}"):
        raise Exception(f"File {base_dir}/{file_name} does not exist")

    # Set the proper graph type for SNAP
    if graph_type == "undirected":
        graph_snap_type = snap.PUNGraph
    elif graph_type == "directed":
        graph_snap_type = snap.PNGraph
    elif graph_type == "network":
        graph_snap_type = snap.PNEANet
    else:
        raise Exception(f"Graphs of type {graph_type} not supported")

    # Read the file according to the specified file format
    if file_type == "CSV":
        if not file_name.endswith(".csv"):
            raise Exception("File name must end with .csv extension for CSV files")

        return snap.LoadEdgeList(graph_snap_type, f"{base_dir}/{file_name}", 0, 1, ",")
    elif file_type == "TXT":
        if not file_name.endswith(".txt"):
            raise Exception("File name must end with .csv extension for TXT files")

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


def store(graph, file_name, file_type="binary", processed=True):
    """Simply stores a graph to data directory in .txt or .graph formats."""

    # Set the base directory
    if processed:
        base_dir = PROCESSED_DATA_DIR
    else:
        base_dir = RAW_DATA_DIR

    # Store the graph according to the specified file format
    if file_type == "TXT":
        if not file_name.endswith(".txt"):
            raise Exception("File name must end with .csv extension for TXT files")

        snap.SaveEdgeList(graph, f"{base_dir}/{file_name}")
    elif file_type == "binary":
        if not file_name.endswith(".graph"):
            raise Exception("File name must end with .graph extension for binary files")

        file_output = snap.TFOut(f"{base_dir}/{file_name}")
        graph.Save(file_output)
        file_output.Flush()
    else:
        raise Exception(f"Files of type {file_type} are not supported")

