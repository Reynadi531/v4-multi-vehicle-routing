from routing_weight_v4 import (
    hybrid_weight_v4
)

from routing_engine_v4 import (
    run_route_v4
)

from route_stats_v4 import (
    route_stats_v4
)


def route_scenario_v4(
    G,
    lookup,
    vehicle_type,
    hour,
    lat1,
    lon1,
    lat2,
    lon2
):

    weight = hybrid_weight_v4(
        lookup,
        hour,
        vehicle_type
    )

    route = run_route_v4(
        G,
        weight,
        lat1,
        lon1,
        lat2,
        lon2
    )

    stats = route_stats_v4(
        G,
        route
    )

    return {

        "hour": hour,

        "route": route,

        "stats": stats
    }