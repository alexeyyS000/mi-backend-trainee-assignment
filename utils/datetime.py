import calendar
from datetime import datetime


def get_uts_from_datetime(dt: datetime) -> int:
    """
    Convert datetime object into unix timestamp.

    :param dt: datatime instance
    :return: Unix timestamp
    """
    current_timetuple = dt.utctimetuple()
    return calendar.timegm(current_timetuple)
