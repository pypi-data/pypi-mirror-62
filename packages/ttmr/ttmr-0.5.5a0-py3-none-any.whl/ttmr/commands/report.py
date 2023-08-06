from pathlib import Path
from tempfile import NamedTemporaryFile
import csvy
from tabulate import tabulate
from ..console import BG_WHITE
from ..console import BLACK
from ..console import Console
from ..ui import default_text_input
from ..ui import text_input
from ..util import add_table_border
from ..database import Category
from ..database import Entry
from ..database import Project
from ..time import FMT_DATE
from ..time import FMT_DATETIME
from .util import db_session
from .util import open_file
from .. import gui



def display_config(conf):
    Console.write(str(conf))


def load(conf):
    load_incidences(conf)


@db_session
def list_categories(conf):

    categories = Category.get_all(conf.db)

    Console.write(BG_WHITE)
    Console.write(BLACK)

    table = tabulate(
        [(c.name, c.active, c.created, c.modified) for c in categories],
        headers=("CATEGORY", "ACTIVE", "CREATED", "MODIFED"),
        numalign="decimal",
    )
    Console.write(add_table_border(table))
    Console.newline()
    Console.clear_formating()


@db_session
def list_projects(conf):
    projects = Project.get_all(conf.db)

    Console.write(BG_WHITE)
    Console.write(BLACK)

    table = tabulate(
        [(c.identifier, c.name, c.active, c.created, c.modified) for c in projects],
        headers=("IDENTIFIER", "NAME", "ACTIVE", "CREATED", "MODIFED"),
        numalign="decimal",
    )
    Console.write(add_table_border(table))
    Console.newline()
    Console.clear_formating()


def _list_entries(list_of_entries):
    entries = [
        (
            e.category.name,
            e.project.identifier,
            e.project.name,
            e.note,
            e.start_time,
            e.end_time,
            e.minutes,
            e.hours
        )
        for e in list_of_entries
    ]

    total_minutes = int(sum([e[6] for e in entries]))
    total_hours = sum([e[6] for e in entries]) / 60.0

    entries.append(("", "", "", "", entries[0][4], entries[-1][5], total_minutes, total_hours))

    headers = ("CATEGORY", "PROJECT ID", "PROJECT NAME", "NOTE", "START", "END", "DURATION", "HOURS")
    formatters = (None, None, None, None, FMT_DATETIME, FMT_DATETIME, "{:}", "{:.3}")

    gui.write_table(entries, headers, formatters)

    entries.insert(0, headers)
    return entries


@db_session
def list_entries(conf):
    _list_entries(Entry.get_all(conf.db))


@db_session
def list_current_weeks_entries(conf):
    entries = _list_entries(Entry.current_week(conf.db))
    if conf.cli_args.get("--csv"):
        filename = Path(NamedTemporaryFile().name).name
        filepath = Path(conf.user_cache_dir, filename + ".csv")
        print(filepath)
        with csvy.writer(filepath) as csv:
            csv.writerows(entries)
        open_file(filepath)



@db_session
def day_summary(conf):
    """
    Displays a summary of the current days total time.

    """
    rows = Entry.day_summary(conf.db)
    gui.write_table(rows, ("DAY", "START", "END", "MINUTES", "HOURS"), ("{:%Y-%m-%d}", "{:%H:%M}", "{:%H:%M}", None, "{:.3}"))


@db_session
def weekly_summary(conf):
    """Displays a summary of times for a given range of days.

    """
    rows = Entry.week_summary(conf.db)
    gui.write_table(rows, ("CATEGORY", "ENTRIES", "MINUTES"))
