# ==================================================
# ROUTE VISUALIZER v4
# ==================================================
# Features:
# - Folium interactive map
# - Vehicle-aware route color
# - Start/end marker
# - Auto fit bounds
# - Save HTML map
# ==================================================

import folium


def plot_route_v4(
    G,
    route,
    vehicle_type="light",
    filename="route_v4.html"
):

    print("\n=== ROUTE VISUALIZER v4 ===")

    # ==========================================
    # VEHICLE COLOR
    # ==========================================

    vehicle_colors = {

        "light": "blue",

        "medium": "orange",

        "heavy": "red"
    }

    route_color = vehicle_colors.get(
        vehicle_type,
        "blue"
    )

    # ==========================================
    # ROUTE COORDINATES
    # ==========================================

    coords = [

        (
            G.nodes[n]["y"],
            G.nodes[n]["x"]
        )

        for n in route
    ]

    # ==========================================
    # START & END
    # ==========================================

    start_coord = coords[0]

    end_coord = coords[-1]

    # ==========================================
    # CREATE MAP
    # ==========================================

    m = folium.Map(

        location=start_coord,

        zoom_start=11,

        control_scale=True
    )

    # ==========================================
    # ROUTE LINE
    # ==========================================

    folium.PolyLine(

        coords,

        color=route_color,

        weight=6,

        opacity=0.85,

        tooltip=(
            f"{vehicle_type.upper()} ROUTE"
        )

    ).add_to(m)

    # ==========================================
    # START MARKER
    # ==========================================

    folium.Marker(

        location=start_coord,

        popup=f"""

        <b>START POINT</b><br>

        Vehicle: {vehicle_type}<br>

        Latitude:
        {start_coord[0]:.6f}<br>

        Longitude:
        {start_coord[1]:.6f}

        """,

        tooltip="START",

        icon=folium.Icon(
            color="green",
            icon="play"
        )

    ).add_to(m)

    # ==========================================
    # END MARKER
    # ==========================================

    folium.Marker(

        location=end_coord,

        popup=f"""

        <b>DESTINATION</b><br>

        Vehicle: {vehicle_type}<br>

        Latitude:
        {end_coord[0]:.6f}<br>

        Longitude:
        {end_coord[1]:.6f}

        """,

        tooltip="DESTINATION",

        icon=folium.Icon(
            color="red",
            icon="stop"
        )

    ).add_to(m)

    # ==========================================
    # FIT BOUNDS
    # ==========================================

    m.fit_bounds(coords)

    # ==========================================
    # SAVE MAP
    # ==========================================

    m.save(filename)

    print("\n=== VISUALIZATION SAVED ===")

    print(filename)

    return m