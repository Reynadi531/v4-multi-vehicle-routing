# ==================================================
# HYBRID ROUTING API V4
# ==================================================

import pickle

from fastapi import FastAPI
from pydantic import BaseModel

from graph_loader_v4 import (
    load_graph_v4
)

# from arrival_optimizer_v4 import (
#     estimate_departure_time_v4
# )

from scenario_router_v4 import (
    route_scenario_v4
)

# ==================================================
# FASTAPI
# ==================================================

app = FastAPI(
    title="Hybrid Routing API",
    version="4.0"
)

# ==================================================
# LOAD GRAPH
# ==================================================

print("\n===================================")
print("LOADING GRAPH")
print("===================================")

G = load_graph_v4()

# ==================================================
# LOAD LOOKUP
# ==================================================

print("\n===================================")
print("LOADING LOOKUP")
print("===================================")

with open(
    "lookup_medium.pkl",
    "rb"
) as f:

    LOOKUP_MEDIUM = pickle.load(f)

print("LOOKUP LOADED")

# ==================================================
# CONFIG
# ==================================================

DEFAULT_VEHICLE = "medium"

TIME_SCENARIOS = {

    "early_morning": 3,

    "morning": 9,

    "afternoon": 15,

    "night": 21
}

# ==================================================
# REQUEST MODEL
# ==================================================

class RouteRequest(BaseModel):

    origin_lat: float
    origin_lon: float

    destination_lat: float
    destination_lon: float

# ==================================================
# CONVERT NODE ROUTE TO COORDINATES
# ==================================================

def route_to_coordinates(route):

    coordinates = []

    for node in route:

        try:

            lon = round(
                G.nodes[node]["x"],
                6
            )

            lat = round(
                G.nodes[node]["y"],
                6
            )

            coordinates.append([
                lon,
                lat
            ])

        except Exception:
            pass

    return coordinates

# ==================================================
# MAIN ROUTE API
# ==================================================

@app.post("/route")
def get_route(request: RouteRequest):

    lookup = LOOKUP_MEDIUM

    recommendations = {}

    for period_name, arrival_hour in TIME_SCENARIOS.items():

        try:

            result = route_scenario_v4(

                G,

                lookup,

                DEFAULT_VEHICLE,

                arrival_hour,

                request.origin_lat,
                request.origin_lon,

                request.destination_lat,
                request.destination_lon
            )

            route = result[
                "route"
            ]

            stats = result[
                "stats"
            ]

            route_coordinates = (
                route_to_coordinates(
                    route
                )
            )

            recommendations[
                period_name
            ] = {

                "distance_km":
                    round(
                        stats["distance_km"],
                        2
                    ),

                "travel_time_hr":
                    round(
                        stats["travel_time_hr"],
                        2
                    ),

                "average_speed_kmh":
                    round(
                        stats[
                            "average_speed_kmh"
                        ],
                        2
                    ),

                "route_point_count":
                    len(
                        route_coordinates
                    ),

                "route_coordinates":
                    route_coordinates
            }

        except Exception as e:

            recommendations[
                period_name
            ] = {

                "error":
                    str(e)
            }

    return {

        "vehicle":
            DEFAULT_VEHICLE.upper(),

        "origin": {

            "lat":
                request.origin_lat,

            "lon":
                request.origin_lon
        },

        "destination": {

            "lat":
                request.destination_lat,

            "lon":
                request.destination_lon
        },

        "recommendations":
            recommendations
    }

# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {

        "message":
            "Hybrid Routing API V4 Running",

        "vehicle":
            DEFAULT_VEHICLE,

        "scenarios":
            list(
                TIME_SCENARIOS.keys()
            )
    }

# ==================================================
# MULTI SCENARIO ROUTING API
# ==================================================

@app.get("/route/v1/driving/scenarios/{coordinates}")
def route_scenarios(
    coordinates: str
):

    start, end = coordinates.split(";")

    lon1, lat1 = map(
        float,
        start.split(",")
    )

    lon2, lat2 = map(
        float,
        end.split(",")
    )

    routes = []

    for scenario, hour in TIME_SCENARIOS.items():

        try:

            result = route_scenario_v4(
                G,
                LOOKUP_MEDIUM,
                DEFAULT_VEHICLE,
                hour,
                lat1,
                lon1,
                lat2,
                lon2
            )

            route = result["route"]

            stats = result["stats"]

            route_coordinates = (
                route_to_coordinates(
                    route
                )
            )

            routes.append({

                "scenario":
                    scenario,

                "distance_km":
                    round(
                        stats["distance_km"],
                        2
                    ),

                "travel_time_hr":
                    round(
                        stats["travel_time_hr"],
                        2
                    ),

                "average_speed_kmh":
                    round(
                        stats[
                            "average_speed_kmh"
                        ],
                        2
                    ),

                "route_point_count":
                    len(
                        route_coordinates
                    ),

                "route_coordinates":
                    route_coordinates
            })

        except Exception as e:

            routes.append({

                "scenario":
                    scenario,

                "error":
                    str(e)
            })

    return {

        "vehicle":
            DEFAULT_VEHICLE.upper(),

        "origin": {

            "lat":
                lat1,

            "lon":
                lon1
        },

        "destination": {

            "lat":
                lat2,

            "lon":
                lon2
        },

        "routes":
            routes
    }

@app.get("/route/v1/driving/arrival/{coordinates}")
def arrival_route(
    coordinates: str,
    overview: str = "false"
):

    try:

        # ==========================================
        # PARSE ARRIVAL TIME
        # ==========================================

        arrival_str, rest = coordinates.split(
            ",",
            1
        )

        hour, minute = arrival_str.split(
            ":"
        )

        target_arrival_hour = (

            int(hour)

            +

            int(minute) / 60
        )

        # ==========================================
        # PARSE COORDINATES
        # ==========================================

        start, end = rest.split(";")

        lon1, lat1 = map(
            float,
            start.split(",")
        )

        lon2, lat2 = map(
            float,
            end.split(",")
        )

        # ==========================================
        # ARRIVAL OPTIMIZATION
        # ==========================================

        result = estimate_departure_time_v4(

            G,

            LOOKUP_MEDIUM,

            DEFAULT_VEHICLE,

            target_arrival_hour,

            lat1,
            lon1,

            lat2,
            lon2
        )

        route = result["route"]

        stats = result["stats"]

        coordinates_geo = (
            route_to_coordinates(
                route
            )
        )

        route_point_count = len(
            coordinates_geo
        )

        # ==========================================
        # FORMAT DEPARTURE TIME
        # ==========================================

        departure_hour = result[
            "departure_hour"
        ]

        dep_h = int(
            departure_hour
        )

        dep_m = int(

            (
                departure_hour
                -
                dep_h
            )
            *
            60
        )

        # ==========================================
        # FORMAT ARRIVAL TIME
        # ==========================================

        arrival_hour = result[
            "arrival_hour"
        ]

        arr_h = int(
            arrival_hour
        )

        arr_m = int(

            (
                arrival_hour
                -
                arr_h
            )
            *
            60
        )

        # ==========================================
        # RESPONSE
        # ==========================================

        response = {

            "code":
                "Ok",

            "vehicle":
                DEFAULT_VEHICLE.upper(),

            "target_arrival":

                f"{int(hour):02d}:"
                f"{int(minute):02d}",

            "recommended_departure":

                f"{dep_h:02d}:"
                f"{dep_m:02d}",

            "estimated_arrival":

                f"{arr_h:02d}:"
                f"{arr_m:02d}",

            "arrival_error_minutes":

                round(

                    result[
                        "arrival_error"
                    ]
                    *
                    60,

                    1
                ),

            "routes": [

                {

                    "weight_name":
                        "routability",

                    "weight":

                        round(

                            stats[
                                "travel_time_hr"
                            ]
                            *
                            3600,

                            2
                        ),

                    "duration":

                        round(

                            stats[
                                "travel_time_hr"
                            ]
                            *
                            3600,

                            2
                        ),

                    "distance":

                        round(

                            stats[
                                "distance_km"
                            ]
                            *
                            1000,

                            2
                        ),

                    "distance_km":

                        round(

                            stats[
                                "distance_km"
                            ],

                            2
                        ),

                    "travel_time_hr":

                        round(

                            stats[
                                "travel_time_hr"
                            ],

                            2
                        ),

                    "average_speed_kmh":

                        round(

                            stats[
                                "average_speed_kmh"
                            ],

                            2
                        ),

                    "route_point_count":
                        route_point_count,

                    "route_coordinates":
                        coordinates_geo,

                    "legs": [

                        {

                            "summary": "",

                            "weight":

                                round(

                                    stats[
                                        "travel_time_hr"
                                    ]
                                    *
                                    3600,

                                    2
                                ),

                            "duration":

                                round(

                                    stats[
                                        "travel_time_hr"
                                    ]
                                    *
                                    3600,

                                    2
                                ),

                            "distance":

                                round(

                                    stats[
                                        "distance_km"
                                    ]
                                    *
                                    1000,

                                    2
                                ),

                            "steps": []
                        }
                    ]
                }
            ],

            "waypoints": [

                {

                    "location":

                        [
                            lon1,
                            lat1
                        ],

                    "name": "",

                    "distance": 0
                },

                {

                    "location":

                        [
                            lon2,
                            lat2
                        ],

                    "name": "",

                    "distance": 0
                }
            ]
        }

        # ==========================================
        # OPTIONAL GEOMETRY
        # ==========================================

        if overview == "full":

            response[
                "routes"
            ][0][
                "geometry"
            ] = {

                "type":
                    "LineString",

                "coordinates":
                    coordinates_geo
            }

        return response

    except Exception as e:

        return {

            "code":
                "Error",

            "message":
                str(e)
        }
@app.get("/route/v1/driving/{coordinates}")
def osrm_route(
    coordinates: str,
    overview: str = "false"
):

    start, end = coordinates.split(";")

    lon1, lat1 = map(
        float,
        start.split(",")
    )

    lon2, lat2 = map(
        float,
        end.split(",")
    )

    result = route_scenario_v4(
        G,
        LOOKUP_MEDIUM,
        DEFAULT_VEHICLE,
        9,
        lat1,
        lon1,
        lat2,
        lon2
    )

    route = result["route"]
    stats = result["stats"]

    coordinates_geo = (
        route_to_coordinates(route)
    )

    response = {

        "code": "Ok",

        "routes": [

            {

                "weight_name":
                    "routability",

                "weight":
                    stats[
                        "travel_time_hr"
                    ] * 3600,

                "duration":
                    stats[
                        "travel_time_hr"
                    ] * 3600,

                "distance":
                    stats[
                        "distance_km"
                    ] * 1000,

                "legs": [

                    {

                        "summary": "",

                        "weight":
                            stats[
                                "travel_time_hr"
                            ] * 3600,

                        "duration":
                            stats[
                                "travel_time_hr"
                            ] * 3600,

                        "distance":
                            stats[
                                "distance_km"
                            ] * 1000,

                        "steps": []
                    }
                ]
            }
        ],

        "waypoints": [

            {
                "location":
                    [lon1, lat1],

                "name": "",

                "distance": 0
            },

            {
                "location":
                    [lon2, lat2],

                "name": "",

                "distance": 0
            }
        ]
    }

    if overview == "full":

        response["routes"][0][
            "geometry"
        ] = {

            "type":
                "LineString",

            "coordinates":
                coordinates_geo
        }

    return response
