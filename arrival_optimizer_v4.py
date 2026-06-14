# ==================================================
# ARRIVAL OPTIMIZER v4
# ==================================================

from routing_weight_v4 import (
    hybrid_weight_v4
)

from routing_engine_v4 import (
    run_route_v4
)

from route_stats_v4 import (
    route_stats_v4
)


def estimate_departure_time_v4(
    G,
    lookup,
    vehicle_type,
    target_arrival_hour,
    lat1,
    lon1,
    lat2,
    lon2
):

    print("\n=== ARRIVAL OPTIMIZER V4 ===")

    best_result = None

    # ==========================================
    # TEST ALL DEPARTURE HOURS
    # ==========================================

    for departure_hour in range(24):

        print(
            f"\nTesting departure hour:"
            f" {departure_hour}:00"
        )

        try:

            # ==================================
            # BUILD WEIGHT
            # ==================================

            weight = hybrid_weight_v4(
                lookup,
                departure_hour,
                vehicle_type
            )

            # ==================================
            # ROUTING
            # ==================================

            route = run_route_v4(
                G,
                weight,
                lat1,
                lon1,
                lat2,
                lon2
            )

            # ==================================
            # STATS
            # ==================================

            stats = route_stats_v4(
                G,
                route
            )

            travel_time_hr = stats[
                "travel_time_hr"
            ]

            estimated_arrival = (
                departure_hour +
                travel_time_hr
            )

            print(
                "Estimated arrival:",
                round(
                    estimated_arrival,
                    2
                )
            )

            # ==================================
            # ARRIVAL ERROR
            # ==================================

            arrival_error = abs(
                estimated_arrival -
                target_arrival_hour
            )

            result = {

                "departure_hour":
                    departure_hour,

                "arrival_hour":
                    estimated_arrival,

                "arrival_error":
                    arrival_error,

                "travel_time_hr":
                    travel_time_hr,

                "route":
                    route,

                "stats":
                    stats
            }

            # ==================================
            # BEST RESULT
            # ==================================

            if best_result is None:

                best_result = result

            elif (
                result["arrival_error"]
                <
                best_result["arrival_error"]
            ):

                best_result = result

        except Exception as e:

            print(
                "Routing failed:",
                str(e)
            )

    return best_result