import osmnx as ox
import networkx as nx


def run_route_v4(
    G,
    weight_func,
    lat1,
    lon1,
    lat2,
    lon2
):

    print("\n=== ROUTING ENGINE V4 ===")

    print("\n=== INPUT COORDINATES ===")

    print("Origin:", lat1, lon1)

    print("Destination:", lat2, lon2)

    # ==========================================
    # FIND ORIGIN NODE
    # ==========================================

    print("\nFinding origin node...")

    orig = ox.distance.nearest_nodes(
        G,
        X=lon1,
        Y=lat1
    )

    # ==========================================
    # FIND DESTINATION NODE
    # ==========================================

    print("\nFinding destination node...")

    dest = ox.distance.nearest_nodes(
        G,
        X=lon2,
        Y=lat2
    )

    # ==========================================
    # ROUTING INFO
    # ==========================================

    print("\n=== ROUTING INFO ===")

    print("Origin Node:", orig)

    print("Destination Node:", dest)

    # ==========================================
    # SAME NODE HANDLING
    # ==========================================

    if orig == dest:

        print(
            "\nWARNING: "
            "Origin and destination "
            "mapped to same node"
        )

        return [orig]

    # ==========================================
    # HYBRID ROUTING
    # ==========================================

    print("\nRunning hybrid routing...")

    try:

        route = nx.shortest_path(
            G,
            source=orig,
            target=dest,
            weight=weight_func
        )

        print(
            "Hybrid routing success"
        )

    # ==========================================
    # FALLBACK ROUTING
    # ==========================================

    except nx.NetworkXNoPath:

        print(
            "\nNo hybrid path found"
        )

        print(
            "Fallback to travel_time"
        )

        route = nx.shortest_path(
            G,
            source=orig,
            target=dest,
            weight="travel_time"
        )

    # ==========================================
    # EMPTY ROUTE CHECK
    # ==========================================

    if len(route) == 0:

        print(
            "\nWARNING: Empty route"
        )

        return [orig]

    # ==========================================
    # RESULT
    # ==========================================

    print("\n=== ROUTE GENERATED ===")

    print(
        "Total Nodes:",
        len(route)
    )

    return route