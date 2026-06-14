# ==================================================
# MAIN MULTI VEHICLE PIPELINE V4
# ==================================================

# ==================================================
# MAIN MULTI VEHICLE PIPELINE V4
# ==================================================

from config_vehicle_v4 import (
    VEHICLE_CONFIG_V4
)

from graph_loader_v4 import (
    load_graph_v4
)

from preprocessing_v4 import (
    preprocess_data_v4
)

from prediction_model_v4 import (
    load_prediction_model_v4,
    predict_eta_v4
)

from lookup_builder_v4 import (
    build_lookup_table_v4
)

from route_visualizer_v4 import (
    plot_route_v4
)

from arrival_optimizer_v4 import (
    estimate_departure_time_v4
)


# ==================================================
# VEHICLE TYPE
# ==================================================

# pilihan:
# "light"
# "medium"
# "heavy"

vehicle_type = "light"


# ==================================================
# VALIDATION
# ==================================================

if vehicle_type not in VEHICLE_CONFIG_V4:

    raise ValueError(
        f"Unknown vehicle type: {vehicle_type}"
    )


# ==================================================
# CONFIG
# ==================================================

config = VEHICLE_CONFIG_V4[
    vehicle_type
]

csv_path = config["csv"]

model_path = config["model"]


# ==================================================
# TARGET ARRIVAL
# ==================================================

target_arrival_hour = 17

# contoh:
# target sampai jam 17:00


# ==================================================
# COORDINATES
# ==================================================

lat1, lon1 = (
    -7.099579,
    107.433602
)

lat2, lon2 = (
    -7.226421,
    12.354076
)

# NOTE:
# gunakan koordinat
# yang masih dalam coverage graph


# ==================================================
# OUTPUT FILE
# ==================================================

filename = (
    f"route_{vehicle_type}.html"
)


# ==================================================
# LOAD GRAPH
# ==================================================

print("\n===================================")
print("LOAD GRAPH")
print("===================================")

G = load_graph_v4()


# ==================================================
# PREPROCESS
# ==================================================

print("\n===================================")
print("PREPROCESS")
print("===================================")

df = preprocess_data_v4(
    G,
    csv_path
)

print(
    "Total rows:",
    len(df)
)


# ==================================================
# LOAD MODEL
# ==================================================

print("\n===================================")
print("LOAD MODEL")
print("===================================")

model = load_prediction_model_v4(
    model_path
)


# ==================================================
# ML PREDICTION
# ==================================================

print("\n===================================")
print("ML PREDICTION")
print("===================================")

df = predict_eta_v4(
    df,
    model
)


# ==================================================
# BUILD LOOKUP
# ==================================================

print("\n===================================")
print("BUILD LOOKUP")
print("===================================")

lookup = build_lookup_table_v4(
    df
)

print(
    "Lookup size:",
    len(lookup)
)


# ==================================================
# ARRIVAL OPTIMIZATION
# ==================================================

print("\n===================================")
print("ARRIVAL OPTIMIZATION")
print("===================================")

result = estimate_departure_time_v4(

    G,

    lookup,

    vehicle_type,

    target_arrival_hour,

    lat1,
    lon1,

    lat2,
    lon2
)


# ==================================================
# RESULT EXTRACTION
# ==================================================

best_departure = result[
    "departure_hour"
]

estimated_arrival = result[
    "arrival_hour"
]

route = result[
    "route"
]

stats = result[
    "stats"
]

dist = stats[
    "distance_km"
]

time = stats[
    "travel_time_hr"
]

speed = stats[
    "average_speed_kmh"
]


# ==================================================
# FINAL RESULT
# ==================================================

print("\n===================================")
print("FINAL RESULT")
print("===================================")

print(
    "Vehicle:",
    vehicle_type.upper()
)

print(
    "Target Arrival:",
    f"{target_arrival_hour}:00"
)

print(
    "Recommended Departure:",
    f"{best_departure}:00"
)

print(
    "Estimated Arrival:",
    round(
        estimated_arrival,
        2
    )
)

print(
    "Distance:",
    round(dist, 2),
    "km"
)

print(
    "Travel Time:",
    round(time, 2),
    "hour"
)

print(
    "Average Speed:",
    round(speed, 2),
    "km/h"
)

print(
    "Total Nodes:",
    len(route)
)


# ==================================================
# VISUALIZATION
# ==================================================

print("\n===================================")
print("VISUALIZATION")
print("===================================")

plot_route_v4(
    G,
    route,
    vehicle_type=vehicle_type,
    filename=filename
)

print(
    "Saved map:",
    filename
)


# ==================================================
# FINISHED
# ==================================================

print("\n===================================")
print("PROCESS FINISHED")
print("===================================")