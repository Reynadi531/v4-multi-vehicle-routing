import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

VEHICLE_CONFIG_V4 = {

    "light": {

        "csv": r"D:/type_Light_Truck.csv",

        "model": os.path.join(
            BASE_DIR,
            "saved_models",
            "Light_Truck_RF.joblib"
        ),

        "route_color": "blue"
    },

    "medium": {

        "csv": r"D:/type_Medium_Truck.csv",

        "model": os.path.join(
            BASE_DIR,
            "saved_models",
            "Medium_Truck_RF.joblib"
        ),

        "route_color": "orange"
    },

    "heavy": {

        "csv": r"D:/type_Heavy_Truck.csv",

        "model": os.path.join(
            BASE_DIR,
            "saved_models",
            "Heavy_Truck_RF.joblib"
        ),

        "route_color": "red"
    }
}