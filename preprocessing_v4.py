import pandas as pd
import numpy as np

from map_matching_v4 import (
    map_match_v4
)

from time_features_v4 import (
    get_time_bucket_v4
)


def preprocess_data_v4(
    G,
    filepath
):

    print(f"\n=== PREPROCESSING ===")
    print(filepath)

    # =====================================
    # LOAD CSV
    # =====================================

    df = pd.read_csv(filepath)

    # =====================================
    # PARSE DATETIME
    # =====================================

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    # =====================================
    # TIME FEATURES
    # =====================================

    df["hour"] = (
        df["time"].dt.hour
    )

    df["dayofweek"] = (
        df["time"].dt.dayofweek
    )

    df["time_bucket"] = (
        df["hour"].apply(
            get_time_bucket_v4
        )
    )

    # =====================================
    # MOVEMENT FEATURES
    # =====================================

    df["delta_lat"] = (
        df["latitude"]
        - df["prev_lat"]
    )

    df["delta_lon"] = (
        df["longitude"]
        - df["prev_lon"]
    )

    # =====================================
    # HEADING
    # =====================================

    df["heading"] = np.degrees(
        np.arctan2(
            df["delta_lon"],
            df["delta_lat"]
        )
    )

    # =====================================
    # ROLLING SPEED
    # =====================================

    df["speed_avg_3"] = (

        df["speed_kmh"]

        .rolling(
            window=3,
            min_periods=1
        )

        .mean()
    )

    # =====================================
    # CLEANING
    # =====================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.dropna()

    # =====================================
    # MAP MATCHING
    # =====================================

    print("\n=== MAP MATCHING ===")

    df = map_match_v4(
        G,
        df
    )

    print(
        f"Rows after preprocessing: {len(df)}"
    )

    return df