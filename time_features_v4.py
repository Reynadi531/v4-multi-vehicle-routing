# ==================================================
# TIME FEATURES V4
# ==================================================

def get_time_bucket_v4(hour):

    """
    Time Window Routing

    early_morning : 00:00 - 05:59
    morning       : 06:00 - 11:59
    afternoon     : 12:00 - 17:59
    night         : 18:00 - 23:59
    """

    if 0 <= hour < 6:

        return "early_morning"

    elif 6 <= hour < 12:

        return "morning"

    elif 12 <= hour < 18:

        return "afternoon"

    else:

        return "night"


def get_day_type_v4(dayofweek):

    if dayofweek < 5:

        return "weekday"

    return "weekend"


def get_hour_category_v4(hour):

    return get_time_bucket_v4(hour)
