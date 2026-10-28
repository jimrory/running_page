"""Stop a Strava sync from publishing a database that lost historical activities."""

import argparse
import json
import sqlite3
from pathlib import Path

from config import SQL_FILE


def activity_ids():
    # Read-only mode prevents SQLite from silently creating a missing database.
    with sqlite3.connect(
        Path(SQL_FILE).resolve().as_uri() + "?mode=ro", uri=True
    ) as db:
        result = {row[0] for row in db.execute("SELECT run_id FROM activities")}
        if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise RuntimeError("History database integrity check failed")
    if not result:
        raise RuntimeError(
            "History database is empty; restore the backup before syncing"
        )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["snapshot", "verify"])
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    current = activity_ids()
    if args.mode == "snapshot":
        args.snapshot.write_text(json.dumps(sorted(current)))
        print(f"Saved {len(current)} existing activity IDs")
    else:
        previous = set(json.loads(args.snapshot.read_text()))
        if not previous:
            raise RuntimeError("History snapshot is empty")
        missing = previous - current
        if missing:
            raise RuntimeError(
                f"Refusing to publish: {len(missing)} historical IDs missing"
            )
        print(f"All {len(previous)} historical activities retained")


if __name__ == "__main__":
    main()
