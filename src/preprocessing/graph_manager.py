import os
import snap

from src.definitions import ROOT_DIR

RAW_DATA_DIR = f"{ROOT_DIR}/data/raw"
PROCESSED_DATA_DIR = f"{ROOT_DIR}/data/processed"


def __init_data_dirs__():
    """Creates data directories if they don't exist."""

    # Create directory for raw data if not exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    # Create directory for processed graphs if not exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def load(file_name, graph_type="network", file_type="TXT", processed=False):
    """Simply loads a raw/processed graph from .csv, .txt or .graph files from data directory."""

    # Set the base directory
    if processed:
        base_dir = PROCESSED_DATA_DIR
    else:
        base_dir = RAW_DATA_DIR

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


def copy(graph):
    """Simply clones a graph."""

    # Quickly copy nodes and edges if graph cannot have attributes
    if not isinstance(graph, snap.PNEANet):
        return snap.ConvertGraph(type(graph), graph)

    # Create the new graph
    new_graph = snap.TNEANet.New()

    # Check whether to copy node attributes or not
    try:
        graph.GetAttrIndN("threshold")
        copy_node_thresholds = True
    except:
        copy_node_thresholds = False

    # Copy nodes with the associated threshold if set
    for node in graph.Nodes():
        new_graph.AddNode(node.GetId())

        if copy_node_thresholds:
            threshold = graph.GetIntAttrDatN(node, "threshold")
            new_graph.AddIntAttrDatN(node.GetId(), threshold, "threshold")

    # Check whether to copy edge attributes or not
    try:
        graph.GetAttrIndE("threshold")
        copy_edge_thresholds = True
    except:
        copy_edge_thresholds = False

    # Copy edges with the associated threshold if set
    for edge in graph.Edges():
        new_graph.AddEdge(edge.GetSrcNId(), edge.GetDstNId(), edge.GetId())

        if copy_edge_thresholds:
            threshold = graph.GetFltAttrDatE(edge, "threshold")
            new_graph.AddFltAttrDatE(edge.GetId(), threshold, "threshold")

    return new_graph

