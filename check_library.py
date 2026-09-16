#!/usr/bin/env python3
"""
Quick diagnostic script to check Photos library access
"""

import os
import sys
import sqlite3
import subprocess
from pathlib import Path


def find_photos_library():
    """Try to find Photos library"""
    print("Searching for Photos library...\n")
    
    # Check default location
    default_path = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
    if os.path.exists(default_path):
        print(f"✓ Found at default location:")
        print(f"  {default_path}")
        return default_path
    
    # Try spotlight
    try:
        result = subprocess.run(
            ["mdfind", "kMDItemKind == 'Photos Library'"],
            capture_output=True,
            text=True,
            timeout=10
        )
        libraries = [l for l in result.stdout.strip().split('\n') if l]
        if libraries:
            print(f"✓ Found {len(libraries)} Photos library(s):")
            for lib in libraries:
                print(f"  {lib}")
            return libraries[0]
    except:
        pass
    
    print("❌ Could not find Photos library")
    return None


def check_database_access(library_path):
    """Check if we can read the database"""
    print("\nChecking database access...")
    
    db_path = os.path.join(library_path, "database/Photos.sqlite")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at:")
        print(f"  {db_path}")
        return False
    
    try:
        # Try to open in read-only mode
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Try a simple query
        cursor.execute("SELECT COUNT(*) FROM ZASSET WHERE ZTRASHEDSTATE = 0")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✓ Successfully connected to database")
        print(f"  Found {count:,} photos (excluding trash)")
        return True
        
    except sqlite3.OperationalError as e:
        print(f"❌ Permission denied")
        print(f"  Error: {e}")
        print(f"\nYou may need to grant Full Disk Access:")
        print(f"  1. System Preferences → Security & Privacy → Privacy")
        print(f"  2. Full Disk Access")
        print(f"  3. Add Terminal (or your terminal app)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def get_photo_stats(library_path):
    """Get some basic stats"""
    print("\nGetting photo statistics...")
    
    db_path = os.path.join(library_path, "database/Photos.sqlite")
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Total photos
        cursor.execute("SELECT COUNT(*) FROM ZASSET WHERE ZTRASHEDSTATE = 0")
        total = cursor.fetchone()[0]
        
        # Date range
        cursor.execute("""
            SELECT 
                MIN(datetime(ZDATECREATED + 978307200, 'unixepoch')),
                MAX(datetime(ZDATECREATED + 978307200, 'unixepoch'))
            FROM ZASSET 
            WHERE ZTRASHEDSTATE = 0 AND ZDATECREATED IS NOT NULL
        """)
        min_date, max_date = cursor.fetchone()
        
        # Photos by year
        cursor.execute("""
            SELECT 
                strftime('%Y', datetime(ZDATECREATED + 978307200, 'unixepoch')) as year,
                COUNT(*)
            FROM ZASSET 
            WHERE ZTRASHEDSTATE = 0 AND ZDATECREATED IS NOT NULL
            GROUP BY year
            ORDER BY year
        """)
        by_year = cursor.fetchall()
        
        conn.close()
        
        print(f"\n  Total photos: {total:,}")
        print(f"  Date range: {min_date[:10]} to {max_date[:10]}")
        print(f"\n  Photos by year:")
        for year, count in by_year:
            bar = '█' * min(50, count // 100)
            print(f"    {year}: {count:>6,} {bar}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False


def main():
    print("="*60)
    print("Apple Photos Library Diagnostic")
    print("="*60)
    print()
    
    # Find library
    library_path = find_photos_library()
    if not library_path:
        print("\nTo manually specify library location:")
        print("  Create ~/.photo_auditor_config.json with:")
        print('  {"library_path": "/path/to/Photos Library.photoslibrary"}')
        sys.exit(1)
    
    # Check access
    if not check_database_access(library_path):
        sys.exit(1)
    
    # Get stats
    get_photo_stats(library_path)
    
    print("\n" + "="*60)
    print("✓ Everything looks good!")
    print("="*60)
    print("\nYou're ready to run the photo auditor:")
    print("  ./photo_tracker.py")
    print()


if __name__ == "__main__":
    main()
