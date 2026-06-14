def build_lookup_table_v4(df):

    grouped = df.groupby(

        [
            "u_node",
            "v_node",
            "time_bucket"
        ]

    ).agg({

        "time_pred": "mean",

        "time_diff": "mean",

        "speed_kmh": "mean"

    }).reset_index()

    lookup = {

        (
            row.u_node,
            row.v_node,
            row.time_bucket
        ): {

            "ml_time": row.time_pred,

            "hist_time": row.time_diff,

            "speed": row.speed_kmh
        }

        for _, row in grouped.iterrows()
    }

    return lookup