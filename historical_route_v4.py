# historical_route_v4.py

import pandas as pd
import numpy as np


class HistoricalRouteEngine:

    def __init__(self, historical_df):

        self.df = historical_df

    def find_similar_routes(
        self,
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon,
        radius=0.05
    ):

        routes = self.df[

            (abs(self.df["origin_lat"] - origin_lat) < radius)
            &
            (abs(self.df["origin_lon"] - origin_lon) < radius)
            &
            (abs(self.df["destination_lat"] - destination_lat) < radius)
            &
            (abs(self.df["destination_lon"] - destination_lon) < radius)

        ]

        return routes

    def get_route_statistics(self, routes):

        if len(routes) == 0:

            return None

        return {

            "trip_count": len(routes),

            "avg_travel_time":

                routes["travel_time_min"].mean(),

            "avg_speed":

                routes["avg_speed"].mean(),

            "distance_km":

                routes["distance_km"].mean()

        }