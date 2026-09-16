#!/usr/bin/env python3
"""
Check Apple Photos library access and print basic stats.

Use this to diagnose permissions, library path, and database connectivity
before running the audit tracker.
"""

import os
import sqlite3
import subprocess
import sys


def find_library_path():
    default_path = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
    if os.path.exists(default_path):
        return default_path

    try:
        result = subprocess.run(
            ["mdfind", "kMDItemKind == 'Photos Library'"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        libraries = [line for line in result.stdout.strip().split("\n") if line]
        if libraries:
            return libraries[0]
    except Exception:
        pass

    return None


def main():
    print("Apple Photos Library Check")
    print("=" * 60)

    library_path = find_library_path()
    if not library_path:
        print("Could not find a Photos library.")
        print("Default location: ~/Pictures/Photos Library.photoslibrary")
        print("If yours is elsewhere, grant Full Disk Access to Terminal and retry.")
        sys.exit(1)

    db_path = os.path.join(library_path, "database/Photos.sqlite")
    print(f"Library: {library_path}")
    print(f"Database: {db_path}")

    if not os.path.exists(db_path):
        print("Photos.sqlite was not found inside the library.")
        sys.exit(1)

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ZASSET WHERE ZTRASHEDSTATE = 0")
        total = cursor.fetchone()[0]
        cursor.execute(
            """
            SELECT
                strftime('%Y-%m', datetime(MIN(ZDATECREATED) + 978307200, 'unixepoch')),
                strftime('%Y-%m', datetime(MAX(ZDATECREATED) + 978307200, 'unixepoch')),
                COUNT(DISTINCT strftime('%Y-%m', datetime(ZDATECREATED + 978307200, 'unixepoch')))
            FROM ZASSET
            WHERE ZTRASHEDSTATE = 0 AND ZDATECREATED IS NOT NULL
            """
        )
        first_month, last_month, month_count = cursor.fetchone()
        conn.close()
    except sqlite3.OperationalError as exc:
        print(f"Could not read Photos.sqlite: {exc}")
        print("Grant Full Disk Access to Terminal (System Settings → Privacy).")
        sys.exit(1)

    print(f"Total photos: {total:,}")
    print(f"Date range: {first_month} to {last_month}")
    print(f"Months with photos: {month_count}")
    print("\nLibrary is readable. You can run ./photo_tracker.py")


if __name__ == "__main__":
    main()
