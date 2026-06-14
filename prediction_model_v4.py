import joblib


def load_prediction_model_v4(
    model_path
):

    print("\n=== LOAD MODEL ===")

    print(model_path)

    model = joblib.load(
        model_path
    )

    print("\n=== MODEL FEATURES ===")

    print(model.feature_names_in_)

    return model


def predict_eta_v4(
    df,
    model
):

    FEATURES = list(
        model.feature_names_in_
    )

    print("\n=== FEATURES USED ===")

    print(FEATURES)

    missing = [

        f for f in FEATURES

        if f not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing features: {missing}"
        )

    X = df[FEATURES]

    df["time_pred"] = model.predict(X)

    return df