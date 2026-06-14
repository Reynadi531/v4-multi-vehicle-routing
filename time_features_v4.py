def get_time_bucket_v4(hour):

    """
    Membagi waktu menjadi:
    - morning_peak
    - evening_peak
    - off_peak
    """

    # =========================
    # MORNING PEAK
    # =========================

    if 7 <= hour <= 9:

        return "morning_peak"

    # =========================
    # EVENING PEAK
    # =========================

    elif 16 <= hour <= 19:

        return "evening_peak"

    # =========================
    # OFF PEAK
    # =========================

    else:

        return "off_peak"


def get_day_type_v4(dayofweek):

    """
    0 = Monday
    6 = Sunday
    """

    # =========================
    # WEEKDAY
    # =========================

    if dayofweek < 5:

        return "weekday"

    # =========================
    # WEEKEND
    # =========================

    return "weekend"


def get_hour_category_v4(hour):

    """
    Kategori waktu lebih detail
    """

    # =========================
    # EARLY MORNING
    # =========================

    if 0 <= hour < 6:

        return "early_morning"

    # =========================
    # MORNING
    # =========================

    elif 6 <= hour < 12:

        return "morning"

    # =========================
    # AFTERNOON
    # =========================

    elif 12 <= hour < 18:

        return "afternoon"

    # =========================
    # NIGHT
    # =========================

    else:

        return "night"