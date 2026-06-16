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

    weight_fn = hybrid_weight_v4(
        lookup,
        hour,
        vehicle_type
    )

    total_dist_m = 0
    total_time_sec = 0

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

        edge = list(
            edge_data.values()
        )[0]

        total_dist_m += edge.get(
            "length",
            0
        )

        hybrid_time_hr = (
            weight_fn(
                u,
                v,
                edge_data
            )
        )

        total_time_sec += (
            hybrid_time_hr * 3600
        )
