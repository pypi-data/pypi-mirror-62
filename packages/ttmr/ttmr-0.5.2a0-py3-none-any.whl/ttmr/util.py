import os
import re
import sys
from datetime import datetime

import arrow
import pendulum
from dateutil import tz

DEFAULT_TMSTP_FMT = "YYYY-MM-DD HH:mm"

DB_TIMESTAMP = "YYYY-MM-DD HH:mm:ss"

DATE_ENTRY_FORMATS = [DEFAULT_TMSTP_FMT, "YYYYMMDD HH:mm", "MM/DD/YYYY HH:mm"]


class DT(object):
    def __init__(self, timezone):
        self.tz = tz.gettz(timezone)

    def parse_date_input(self, date_input):
        #  return arrow.get(date_input, DATE_ENTRY_FORMATS, tzinfo=self.tz)
        if isinstance(date_input, datetime):
            return date_input
        return datetime.strptime(date_input, DATE_ENTRY_FORMATS)

    def current_timestamp(self):
        return arrow.now(tz=self.tz)

    def to_str(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M")

    def calc_duration(self, end_time, start_time):
        # return minutes
        start_time = start_time.datetime
        end_time = end_time.datetime
        duration = end_time - start_time
        return int(duration.total_seconds() / 60.0)

    def get_duration(self, entry, now):
        if not entry or entry.minutes > 0:
            return None, None
        start_time = self.parse_date_input(entry.start_time)
        duration = self.calc_duration(now, start_time)
        return entry.entry_id, duration


def replace_bad_char(ex):
    return (u"?", ex.start)


class Timer(object):
    def __init__(self, start_time):  # , timezone):
        #  self.timezone = timezone
        if isinstance(start_time, datetime):
            self.start_time = start_time
        elif isinstance(start_time, str):
            self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        else:
            self.start_time = start_time

    def get_lapsed_seconds(self):
        end_time = pendulum.now()
        duration = end_time - self.start_time
        return duration.total_seconds()

    def get_formatted_lapsed_time(self):
        total_seconds = self.get_lapsed_seconds()
        seconds = int(total_seconds) % 60
        total_minutes = int(total_seconds) / 60
        minutes = int(total_minutes % 60)
        hours = int(int(total_minutes) / 60)
        return "{:0>2}:{:0>2}:{:0>2}".format(hours, minutes, seconds)


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, "sql", filename)


def add_table_border(text, border=1):
    lines = [(" " * border) + line for line in text.split("\n")]
    length = max([len(a) for a in lines])

    return "\n".join([l.ljust(length) for l in lines])


def regex_factory(regex):
    """Convenience wrapper around regex with named capture groups.
    """
    reg = re.compile(regex, re.I)

    def _match(text):
        m = reg.match(text)
        if m:
            return m.groupdict()

    return _match
