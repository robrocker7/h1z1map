import pytz
import re
import logging

from datetime import datetime


def get_now_datetime_cst():
    central = pytz.timezone('America/Chicago')
    now = datetime.now()
    return central.localize(now)


def parse_loc_string(loc_string):
    pattern = re.compile(r'x=(?P<x_cord>[0-9\.-]+).*z=(?P<z_cord>[0-9\.-]+).*:\s(?P<heading>[0-9\.-]+).*(?P<cmd>/loc[0-9\.\s-]+)')

    matches = re.match(pattern, loc_string)
    if matches is None:
        return None, None, None

    matches = matches.groupdict()

    lat = matches.get('x_cord', None)
    lng = matches.get('z_cord', None)
    heading = matches.get('heading', None)
    cmd_string = matches.get('cmd', None)

    if lat is None or lng is None:
        cmd_args = cmd_string.split(' ')
        lat = cmd_args[1]
        lng = cmd_args[3]

    return float(lat), float(lng), float(heading)