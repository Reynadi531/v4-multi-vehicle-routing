# recommendation_engine_v4.py

TIME_CATEGORIES = [

    "early_morning",
    "morning",
    "afternoon",
    "night"

]


class RecommendationEngine:

    def __init__(self):

        pass

    def hybrid_travel_time(

        self,
        historical_time,
        osrm_time

    ):

        return (

            0.8 * historical_time
            +
            0.2 * osrm_time

        )

    def build_recommendations(

        self,
        historical_lookup,
        osrm_duration_min

    ):

        recommendations = []

        for category in TIME_CATEGORIES:

            historical_time = \
                historical_lookup[category]

            hybrid_time = \
                self.hybrid_travel_time(

                    historical_time,
                    osrm_duration_min

                )

            recommendations.append({

                "time_category": category,

                "historical_time":

                    round(historical_time, 2),

                "osrm_time":

                    round(osrm_duration_min, 2),

                "hybrid_time":

                    round(hybrid_time, 2)

            })

        return recommendations