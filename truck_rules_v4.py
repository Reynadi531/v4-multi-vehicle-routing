# ==================================================
# TRUCK RULES V4
# ==================================================
# Vehicle-aware routing rules
#
# Support:
# - Light Truck
# - Medium Truck
# - Heavy Truck
#
# Functions:
# - get_highway_type_v4
# - is_blocked_for_truck_v4
# - is_vehicle_allowed_v4
# - get_truck_penalty_v4
# ==================================================


# ==================================================
# GET HIGHWAY TYPE
# ==================================================

def get_highway_type_v4(edge):

    """
    Ambil tipe jalan dari edge OSM.
    """

    hw = edge.get(
        "highway",
        "unknown"
    )

    # kadang highway berupa list
    if isinstance(hw, list):

        if len(hw) > 0:

            hw = hw[0]

        else:

            hw = "unknown"

    return hw


# ==================================================
# BLOCKED ROAD
# ==================================================

def is_blocked_for_truck_v4(edge):

    """
    Jalan yang benar-benar
    tidak boleh dilewati truck.
    """

    hw = get_highway_type_v4(
        edge
    )

    blocked = [

        # pedestrian
        "footway",
        "pedestrian",
        "steps",
        "path",

        # bicycle
        "cycleway",

        # small track
        "track",

        # private corridor
        "corridor",

        # horse path
        "bridleway",

        # rail
        "platform",

        # escape
        "escape"
    ]

    return hw in blocked


# ==================================================
# VEHICLE ACCESS RULE
# ==================================================

def is_vehicle_allowed_v4(
    edge,
    vehicle_type
):

    """
    Validasi apakah kendaraan
    boleh melewati tipe jalan tertentu.
    """

    hw = get_highway_type_v4(
        edge
    )

    # ==========================================
    # LIGHT TRUCK
    # ==========================================

    if vehicle_type == "light":

        allowed = [

            # major road
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",

            # local road
            "residential",
            "service",
            "unclassified",

            # additional
            "living_street",
            "road"
        ]

    # ==========================================
    # MEDIUM TRUCK
    # ==========================================

    elif vehicle_type == "medium":

        allowed = [

            # major road
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",

            # limited local
            "service",

            # additional
            "road"
        ]

    # ==========================================
    # HEAVY TRUCK
    # ==========================================

    elif vehicle_type == "heavy":

        allowed = [

            # main freight road
            "motorway",
            "trunk",
            "primary",

            # limited access
            "secondary"
        ]

    # ==========================================
    # UNKNOWN VEHICLE
    # ==========================================

    else:

        allowed = []

    return hw in allowed


# ==================================================
# ROAD PENALTY
# ==================================================

def get_truck_penalty_v4(
    edge,
    vehicle_type
):

    """
    Penalty jalan.

    Semakin besar:
    semakin dihindari.
    """

    hw = get_highway_type_v4(
        edge
    )

    # ==========================================
    # LIGHT TRUCK
    # ==========================================

    if vehicle_type == "light":

        penalties = {

            # ======================
            # HIGH PRIORITY
            # ======================

            "motorway": 1.0,
            "trunk": 1.0,

            # ======================
            # MEDIUM
            # ======================

            "primary": 1.1,
            "secondary": 1.2,
            "tertiary": 1.5,

            # ======================
            # LOCAL
            # ======================

            "residential": 2.0,
            "service": 2.5,
            "living_street": 3.0,

            # ======================
            # OTHER
            # ======================

            "unclassified": 3.5,
            "road": 4.0,

            # ======================
            # UNKNOWN
            # ======================

            "unknown": 10.0
        }

    # ==========================================
    # MEDIUM TRUCK
    # ==========================================

    elif vehicle_type == "medium":

        penalties = {

            # ======================
            # HIGH PRIORITY
            # ======================

            "motorway": 1.0,
            "trunk": 1.0,

            # ======================
            # MEDIUM
            # ======================

            "primary": 1.3,
            "secondary": 1.7,
            "tertiary": 2.5,

            # ======================
            # LOCAL
            # ======================

            "residential": 5.0,
            "service": 6.0,
            "living_street": 8.0,

            # ======================
            # OTHER
            # ======================

            "unclassified": 7.0,
            "road": 8.0,

            # ======================
            # UNKNOWN
            # ======================

            "unknown": 15.0
        }

    # ==========================================
    # HEAVY TRUCK
    # ==========================================

    elif vehicle_type == "heavy":

        penalties = {

            # ======================
            # MAIN FREIGHT ROAD
            # ======================

            "motorway": 1.0,
            "trunk": 1.0,

            # ======================
            # MAJOR ROAD
            # ======================

            "primary": 1.5,

            # ======================
            # LESS PREFERRED
            # ======================

            "secondary": 4.0,
            "tertiary": 8.0,

            # ======================
            # LOCAL ROAD
            # ======================

            "residential": 20.0,
            "service": 25.0,
            "living_street": 40.0,

            # ======================
            # OTHER
            # ======================

            "unclassified": 30.0,
            "road": 40.0,

            # ======================
            # UNKNOWN
            # ======================

            "unknown": 100.0
        }

    # ==========================================
    # DEFAULT
    # ==========================================

    else:

        penalties = {

            "unknown": 100.0
        }

    return penalties.get(
        hw,
        100.0
    )