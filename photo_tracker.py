#!/usr/bin/env python3
"""
Simple Photo Audit Tracker
A lightweight tool to track your progress auditing Apple Photos month by month.
"""

import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path


PROGRESS_FILE = os.path.expanduser("~/.photo_progress.json")


class PhotoLibrary:
    """Interface to Apple Photos library"""
    
    def __init__(self):
        self.library_path = self._find_library_path()
        self.db_path = os.path.join(self.library_path, "database/Photos.sqlite")
    
    def _find_library_path(self):
        """Find the Photos library path"""
        default_path = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
        if os.path.exists(default_path):
            return default_path
        
        # Try spotlight
        try:
            result = subprocess.run(
                ["mdfind", "kMDItemKind == 'Photos Library'"],
                capture_output=True,
                text=True,
                timeout=5
            )
            libraries = [l for l in result.stdout.strip().split('\n') if l]
            if libraries:
                return libraries[0]
        except:
            pass
        
        raise Exception("Could not find Photos library")
    
    def get_all_months(self):
        """Get list of all year-months with photos"""
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            strftime('%Y-%m', datetime(ZDATECREATED + 978307200, 'unixepoch')) as month,
            COUNT(*) as count
        FROM ZASSET
        WHERE ZTRASHEDSTATE = 0 AND ZDATECREATED IS NOT NULL
        GROUP BY month
        ORDER BY month ASC
        """
        
        cursor.execute(query)
        months = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return months
    
    def get_month_stats(self, year_month):
        """Get statistics for a specific month"""
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN ZKINDSUBTYPE = 10 THEN 1 ELSE 0 END) as screenshots,
            SUM(CASE WHEN ZFILENAME LIKE '%screenshot%' 
                      OR ZFILENAME LIKE '%screen shot%' 
                      OR ZFILENAME LIKE '%screen_shot%' THEN 1 ELSE 0 END) as screenshot_files
        FROM ZASSET
        WHERE ZTRASHEDSTATE = 0 
        AND strftime('%Y-%m', datetime(ZDATECREATED + 978307200, 'unixepoch')) = ?
        """
        
        cursor.execute(query, (year_month,))
        total, screenshots_meta, screenshot_files = cursor.fetchone()
        
        conn.close()
        
        screenshots = max(screenshots_meta or 0, screenshot_files or 0)
        
        return {
            'total': total or 0,
            'screenshots': screenshots,
            'has_screenshots': screenshots > 0
        }


class ProgressTracker:
    """Track audit progress"""
    
    def __init__(self):
        self.data = self._load()
    
    def _load(self):
        """Load progress from file"""
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            'last_reviewed': None,
            'library_date_range': {}
        }
    
    def save(self):
        """Save progress to file"""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def update_last_reviewed(self, year_month):
        """Update last reviewed month"""
        self.data['last_reviewed'] = year_month
        self.save()
    
    def update_library_range(self, first_month, last_month):
        """Update library date range"""
        self.data['library_date_range'] = {
            'first_photo': first_month,
            'last_photo': last_month
        }
        self.save()
    
    def get_next_month(self, all_months):
        """Get next month to review"""
        if not all_months:
            return None
        
        sorted_months = sorted(all_months.keys())
        
        if not self.data['last_reviewed']:
            # Start from the beginning
            return sorted_months[0]
        
        # Find next month after last reviewed
        last = self.data['last_reviewed']
        try:
            idx = sorted_months.index(last)
            if idx + 1 < len(sorted_months):
                return sorted_months[idx + 1]
            else:
                return None  # All done!
        except ValueError:
            # Last reviewed month not in list, start from beginning
            return sorted_months[0]
    
    def get_progress_stats(self, all_months):
        """Calculate progress statistics"""
        if not all_months:
            return None
        
        sorted_months = sorted(all_months.keys())
        total_months = len(sorted_months)
        
        if not self.data['last_reviewed']:
            return {
                'reviewed_count': 0,
                'total_months': total_months,
                'percent_complete': 0
            }
        
        try:
            idx = sorted_months.index(self.data['last_reviewed'])
            reviewed_count = idx + 1
            return {
                'reviewed_count': reviewed_count,
                'total_months': total_months,
                'percent_complete': int((reviewed_count / total_months) * 100)
            }
        except ValueError:
            return {
                'reviewed_count': 0,
                'total_months': total_months,
                'percent_complete': 0
            }


def format_month_name(year_month):
    """Convert YYYY-MM to 'Month YYYY'"""
    return datetime.strptime(year_month, "%Y-%m").strftime("%B %Y")


def open_photos_app():
    """Open Photos app"""
    applescript = '''
    tell application "Photos"
        activate
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript], stderr=subprocess.DEVNULL)


def show_next_month(library, tracker):
    """Show next month to review and open Photos"""
    print("Apple Photos Audit Tracker")
    print("=" * 60)
    
    # Get all months
    all_months = library.get_all_months()
    
    if not all_months:
        print("\n❌ No photos found in library")
        return
    
    # Update library range
    sorted_months = sorted(all_months.keys())
    tracker.update_library_range(sorted_months[0], sorted_months[-1])
    
    # Get next month
    next_month = tracker.get_next_month(all_months)
    
    if not next_month:
        print("\n🎉 All photos have been reviewed!")
        print(f"\nYou've completed {len(sorted_months)} months")
        print(f"From {format_month_name(sorted_months[0])} to {format_month_name(sorted_months[-1])}")
        return
    
    # Get stats for this month
    stats = library.get_month_stats(next_month)
    
    print(f"\n📅 Next month to review: {format_month_name(next_month)}")
    print(f"   Total photos: {stats['total']}")
    
    if stats['has_screenshots']:
        print(f"   📱 {stats['screenshots']} potential screenshots")
    
    # Show progress
    progress = tracker.get_progress_stats(all_months)
    if progress and progress['reviewed_count'] > 0:
        print(f"\n📊 Progress: {progress['reviewed_count']}/{progress['total_months']} months ({progress['percent_complete']}%)")
    
    # Tips
    print("\n" + "=" * 60)
    print("QUICK REVIEW TIPS:")
    print("=" * 60)
    print(f"\n1. Search in Photos: {format_month_name(next_month)}")
    
    if stats['has_screenshots']:
        print(f"2. Find screenshots: screenshot {format_month_name(next_month)}")
    
    print("\nWhat to look for:")
    print("  • Delete unwanted screenshots")
    print("  • Remove duplicates and similar photos")
    print("  • Delete blurry or poor quality shots")
    print("  • Create albums for events/trips")
    
    print("\n" + "=" * 60)
    response = input("\nOpen Photos app? (y/n): ").strip().lower()
    
    if response == 'y':
        open_photos_app()
        print(f"\n✓ Photos opened - search for: {format_month_name(next_month)}")
        print(f"\nWhen done, run: ./photo_tracker.py done {next_month}")
    else:
        print(f"\nRun again when ready to review {format_month_name(next_month)}")


def mark_month_done(library, tracker, year_month):
    """Mark a month as reviewed"""
    try:
        # Validate format
        datetime.strptime(year_month, "%Y-%m")
    except ValueError:
        print(f"❌ Invalid format. Use YYYY-MM (e.g., 2015-07)")
        return
    
    tracker.update_last_reviewed(year_month)
    
    all_months = library.get_all_months()
    progress = tracker.get_progress_stats(all_months)
    
    print(f"✓ Marked {format_month_name(year_month)} as reviewed!")
    
    if progress:
        print(f"\n📊 Progress: {progress['reviewed_count']}/{progress['total_months']} months ({progress['percent_complete']}% complete)")
        
        if progress['reviewed_count'] < progress['total_months']:
            remaining = progress['total_months'] - progress['reviewed_count']
            print(f"   {remaining} months remaining")
        else:
            print("\n🎉 All done! You've reviewed your entire library!")


def show_status(library, tracker):
    """Show current progress status"""
    all_months = library.get_all_months()
    
    print("Apple Photos Audit Status")
    print("=" * 60)
    
    if not all_months:
        print("\n❌ No photos found in library")
        return
    
    sorted_months = sorted(all_months.keys())
    total_photos = sum(all_months.values())
    
    print(f"\nLibrary: {library.library_path}")
    print(f"Total photos: {total_photos:,}")
    print(f"Date range: {format_month_name(sorted_months[0])} to {format_month_name(sorted_months[-1])}")
    print(f"Total months: {len(sorted_months)}")
    
    if tracker.data['last_reviewed']:
        progress = tracker.get_progress_stats(all_months)
        print(f"\n📊 Review Progress:")
        print(f"   Last reviewed: {format_month_name(tracker.data['last_reviewed'])}")
        print(f"   Months completed: {progress['reviewed_count']}/{progress['total_months']}")
        print(f"   Progress: {progress['percent_complete']}%")
        
        # Progress bar
        bar_length = 40
        filled = int((progress['percent_complete'] / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"   [{bar}] {progress['percent_complete']}%")
        
        next_month = tracker.get_next_month(all_months)
        if next_month:
            print(f"\n   Next up: {format_month_name(next_month)}")
    else:
        print(f"\n📍 Not started yet")
        print(f"   Run './photo_tracker.py' to begin with {format_month_name(sorted_months[0])}")


def list_small_months(library):
    """List months with few photos (quick delete candidates)"""
    all_months = library.get_all_months()
    
    small_months = {m: c for m, c in all_months.items() if c < 10}
    
    if not small_months:
        print("No months with fewer than 10 photos")
        return
    
    print("Months with <10 photos (quick review candidates):")
    print("=" * 60)
    
    for month, count in sorted(small_months.items()):
        print(f"  {format_month_name(month)}: {count} photos")
    
    print(f"\nTotal: {len(small_months)} months")


def reset_progress():
    """Reset progress tracker"""
    response = input("Reset progress and start over? (yes/no): ").strip().lower()
    
    if response == 'yes':
        if os.path.exists(PROGRESS_FILE):
            backup = PROGRESS_FILE + '.backup'
            os.rename(PROGRESS_FILE, backup)
            print(f"✓ Backed up to {backup}")
        
        os.remove(PROGRESS_FILE) if os.path.exists(PROGRESS_FILE) else None
        print("✓ Progress reset! Run './photo_tracker.py' to start fresh")
    else:
        print("Cancelled")


def print_usage():
    """Print usage information"""
    print("""
Usage:
  ./photo_tracker.py              Show next month to review
  ./photo_tracker.py done YYYY-MM Mark month as complete
  ./photo_tracker.py status       Show progress statistics
  ./photo_tracker.py small        List months with <10 photos
  ./photo_tracker.py reset        Reset progress
  ./photo_tracker.py help         Show this help

Examples:
  ./photo_tracker.py              # Show next month
  ./photo_tracker.py done 2015-07 # Mark July 2015 as done
  ./photo_tracker.py status       # Check your progress
""")


def main():
    """Main entry point"""
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == 'help':
                print_usage()
                return
            elif command == 'reset':
                reset_progress()
                return
            
            # Commands that need library access
            library = PhotoLibrary()
            tracker = ProgressTracker()
            
            if command == 'done':
                if len(sys.argv) < 3:
                    print("Usage: ./photo_tracker.py done YYYY-MM")
                    print("Example: ./photo_tracker.py done 2015-07")
                    return
                mark_month_done(library, tracker, sys.argv[2])
            
            elif command == 'status':
                show_status(library, tracker)
            
            elif command == 'small':
                list_small_months(library)
            
            else:
                print(f"Unknown command: {command}")
                print_usage()
        
        else:
            # Default: show next month
            library = PhotoLibrary()
            tracker = ProgressTracker()
            show_next_month(library, tracker)
    
    except KeyboardInterrupt:
        print("\n\nCancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
