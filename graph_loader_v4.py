import os
import osmnx as ox
import networkx as nx


def load_graph_v4():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
        #     os.path.abspath(__file__)
        )
    )

    graph_path = os.path.join(
        BASE_DIR,
        "graphsv2",
        "truck_network_realistic.graphml"
    )

    print("\n=== LOADING GRAPH ===")

    print(graph_path)

    G = ox.load_graphml(
        graph_path
    )

    G = G.subgraph(

        max(
            nx.strongly_connected_components(G),
            key=len
        )

    ).copy()

    return G
