import pickle

from config_vehicle_v4 import (
    VEHICLE_CONFIG_V4
)

from graph_loader_v4 import (
    load_graph_v4
)

from preprocessing_v4 import (
    preprocess_data_v4
)

from prediction_model_v4 import (
    load_prediction_model_v4,
    predict_eta_v4
)

from lookup_builder_v4 import (
    build_lookup_table_v4
)

G = load_graph_v4()

for vehicle in VEHICLE_CONFIG_V4:

    config = VEHICLE_CONFIG_V4[
        vehicle
    ]

    print(
        f"\nGenerating {vehicle}"
    )

    df = preprocess_data_v4(
        G,
        config["csv"]
    )

    model = load_prediction_model_v4(
        config["model"]
    )

    df = predict_eta_v4(
        df,
        model
    )

    lookup = build_lookup_table_v4(
        df
    )

    with open(
        f"lookup_{vehicle}.pkl",
        "wb"
    ) as f:

        pickle.dump(
            lookup,
            f
        )

print("DONE")