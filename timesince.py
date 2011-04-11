#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from i18n import __

def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    logging.debug ('timesince [%s] %s', dt, type(dt))
    if isinstance (dt, str) or isinstance (dt, unicode) :
        dt = datetime.strptime (dt.rsplit('.', 1)[0], '%Y-%m-%d %H:%M:%S')

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return u' '.join ([str(period), __(singular) if period == 1 else __(plural), __('ago')])
    return __(default)

