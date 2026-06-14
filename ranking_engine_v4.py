# ranking_engine_v4.py


class RankingEngine:

    def __init__(self):

        pass

    def rank_recommendations(

        self,
        recommendations

    ):

        ranked = sorted(

            recommendations,

            key=lambda x:

            x["hybrid_time"]

        )

        for idx, rec in enumerate(ranked):

            rec["rank"] = idx + 1

        return ranked

    def get_best(self, ranked):

        return ranked[0]