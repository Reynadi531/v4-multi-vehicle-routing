# ==================================================
# ROUTE STATS v4
# ==================================================
# Menghitung:
# - total distance
# - total travel time
# - average speed
# - edge count
#
# Support:
# - OSMnx MultiDiGraph
# - Hybrid routing
# - Vehicle-aware routing
# ==================================================


def route_stats_v4(
    G,
    route
):

    print("\n=== ROUTE STATISTICS V4 ===")

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

        # ======================================
        # SAFETY CHECK
        # ======================================

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
        # TRAVEL TIME
        # ======================================

        travel_time = edge.get(
            "travel_time",
            0
        )

        total_time_sec += travel_time

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

        "distance_km": dist_km,

        "travel_time_hr": time_hr,

        "average_speed_kmh": avg_speed,

        "total_edges": total_edges,

        "total_nodes": len(route)
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