# ==================================================
# ROUTING WEIGHT V4
# ==================================================

from truck_rules_v4 import (

    is_blocked_for_truck_v4,

    is_vehicle_allowed_v4,

    get_truck_penalty_v4
)

from time_features_v4 import (
    get_time_bucket_v4
)


def hybrid_weight_v4(
    lookup,
    hour,
    vehicle_type
):

    print("\n=== HYBRID WEIGHT V4 ===")

    bucket = get_time_bucket_v4(
        hour
    )

    print(
        "Vehicle:",
        vehicle_type
    )

    print(
        "Time Bucket:",
        bucket
    )

    # ==========================================
    # EDGE WEIGHT FUNCTION
    # ==========================================

    def weight(
        u,
        v,
        data
    ):

        try:

            # ======================================
            # MULTIDIGRAPH HANDLING
            # ======================================

            if isinstance(
                data,
                dict
            ) and 0 in data:

                edge = data[0]

            else:

                edge = data

            # ======================================
            # BLOCKED ROAD
            # ======================================

            if is_blocked_for_truck_v4(
                edge
            ):

                return 1e9

            # ======================================
            # VEHICLE ACCESS
            # ======================================

            if not is_vehicle_allowed_v4(

                edge,
                vehicle_type

            ):

                return 1e9

            # ======================================
            # BASE OSM TRAVEL TIME
            # ======================================

            travel_time_sec = edge.get(
                "travel_time",
                None
            )

            if travel_time_sec is None:

                length_m = edge.get(
                    "length",
                    1
                )

                speed_kmh = edge.get(
                    "speed_kph",
                    40
                )

                travel_time_sec = (

                    length_m / 1000

                ) / speed_kmh * 3600

            osm_time = (
                float(travel_time_sec)
                / 3600
            )

            # ======================================
            # TRUCK PENALTY
            # ======================================

            penalty = (
                get_truck_penalty_v4(
                    edge,
                    vehicle_type
                )
            )

            osm_time *= penalty

            # ======================================
            # HISTORICAL LOOKUP
            # ======================================

            hist = lookup.get(

                (
                    u,
                    v,
                    bucket
                ),

                None
            )

            # ======================================
            # HYBRID ML + OSM
            # ======================================

            if hist is not None:

                ml_time = hist.get(
                    "ml_time",
                    osm_time
                )

                if (
                    ml_time is None
                    or
                    ml_time <= 0
                ):

                    ml_time = osm_time

                hybrid_time = (

                    0.8 * ml_time +

                    0.2 * osm_time

                )

                return hybrid_time

            # ======================================
            # FALLBACK
            # ======================================

            return osm_time

        except Exception as e:

            print(
                "Weight Error:",
                str(e)
            )

            return 1e9

    return weight