import os
import osmnx as ox
import joblib

BASE_DIR = r"C:\B 9477 TEZ - WB035"

graphml_path = os.path.join(
    BASE_DIR,
    "graphsv2",
    "truck_network_realistic.graphml"
)

output_path = os.path.join(
    BASE_DIR,
    "graphsv2",
    "truck_network_realistic.pkl"
)

print("Loading GraphML...")

G = ox.load_graphml(
    graphml_path
)

print("Saving pickle...")

joblib.dump(
    G,
    output_path
)

print("DONE")