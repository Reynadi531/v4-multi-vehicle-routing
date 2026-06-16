# ==================================================
# ROUTE STATS V4
# Hybrid Travel Time
# ==================================================

from routing_weight_v4 import (
    hybrid_weight_v4
)


def route_stats_v4(
    G,
    route,
    lookup,
    vehicle_type,
    hour
):

    print("\n=== ROUTE STATISTICS V4 ===")

    # ==========================================
    # HYBRID WEIGHT
    # ==========================================

    weight_fn = hybrid_weight_v4(
        lookup,
        hour,
        vehicle_type
    )

    # ==========================================
    # INITIALIZATION
    # ==========================================

    total_dist_m = 0

    total_time_sec = 0

    total_edges = 0

    # ==========================================
    # LOOP EDGE
    # ==========================================

    for u, v in zip(
        route[:-1],
        route[1:]
    ):

        edge_data = G.get_edge_data(
            u,
            v
        )

        if edge_data is None:

            continue

        # ======================================
        # MULTIDIGRAPH HANDLING
        # ======================================

        edge = list(
            edge_data.values()
        )[0]

        # ======================================
        # DISTANCE
        # ======================================

        length = edge.get(
            "length",
            0
        )

        total_dist_m += length

        # ======================================
        # HYBRID TRAVEL TIME
        # ======================================

        hybrid_time_hr = weight_fn(
            u,
            v,
            edge_data
        )

        total_time_sec += (
            hybrid_time_hr * 3600
        )

        # ======================================
        # EDGE COUNT
        # ======================================

        total_edges += 1

    # ==========================================
    # CONVERSION
    # ==========================================

    dist_km = (
        total_dist_m / 1000
    )

    time_hr = (
        total_time_sec / 3600
    )

    # ==========================================
    # AVERAGE SPEED
    # ==========================================

    if time_hr > 0:

        avg_speed = (
            dist_km / time_hr
        )

    else:

        avg_speed = 0

    # ==========================================
    # RESULT
    # ==========================================

    result = {

        "distance_km":
            dist_km,

        "travel_time_hr":
            time_hr,

        "average_speed_kmh":
            avg_speed,

        "total_edges":
            total_edges,

        "total_nodes":
            len(route)
    }

    # ==========================================
    # PRINT RESULT
    # ==========================================

    print(
        "Distance:",
        round(dist_km, 2),
        "km"
    )

    print(
        "Travel Time:",
        round(time_hr, 2),
        "hour"
    )

    print(
        "Average Speed:",
        round(avg_speed, 2),
        "km/h"
    )

    print(
        "Edges:",
        total_edges
    )

    print(
        "Nodes:",
        len(route)
    )

    return result
