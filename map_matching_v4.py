import osmnx as ox


def map_match_v4(
    G,
    df
):

    print("\n=== MAP MATCHING V4 ===")

    print(
        "Total rows:",
        len(df)
    )

    # ==========================================
    # CLEAN INVALID COORDINATES
    # ==========================================

    df = df.dropna(subset=[

        "latitude",
        "longitude",

        "prev_lat",
        "prev_lon"
    ])

    # ==========================================
    # PREVIOUS NODE
    # ==========================================

    print(
        "Finding previous nodes..."
    )

    u_nodes = ox.distance.nearest_nodes(

        G,

        X=df["prev_lon"].values,

        Y=df["prev_lat"].values
    )

    # ==========================================
    # CURRENT NODE
    # ==========================================

    print(
        "Finding current nodes..."
    )

    v_nodes = ox.distance.nearest_nodes(

        G,

        X=df["longitude"].values,

        Y=df["latitude"].values
    )

    # ==========================================
    # SAVE NODE
    # ==========================================

    df["u_node"] = u_nodes

    df["v_node"] = v_nodes

    # ==========================================
    # REMOVE SAME NODE
    # ==========================================

    df = df[
        df["u_node"] != df["v_node"]
    ]

    print(
        "Matched rows:",
        len(df)
    )

    return df