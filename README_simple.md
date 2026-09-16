# Simple Photo Audit Tracker

A lightweight tool to help you systematically audit your Apple Photos library, month by month.

## What It Does

Simple progress tracking - it remembers where you left off reviewing photos. You control the pace.

## Quick Start

```bash
# Make executable
chmod +x photo_tracker.py

# Start your first review
./photo_tracker.py
```

The tool will:

- Show you the next month to review
- Tell you how many photos are in that month
- Open Photos app
- You search for the month (e.g., "June 2015")
- You review at your own pace
- When done, you mark it complete

## Usage

### Start a review session

```bash
./photo_tracker.py
```

Output:

```
📅 Next month to review: June 2015
   Total photos: 147
   📱 12 potential screenshots

📊 Progress: 5/132 months (4%)

QUICK REVIEW TIPS:
1. Search in Photos: June 2015
2. Find screenshots: screenshot June 2015

✓ Photos opened - search for: June 2015

When done, run: ./photo_tracker.py done 2015-06
```

### Mark month as complete

```bash
./photo_tracker.py done 2015-06
```

### Check your progress

```bash
./photo_tracker.py status
```

Output:

```
Library: ~/Pictures/Photos Library.photoslibrary
Total photos: 24,567
Date range: January 2010 to September 2026
Total months: 201

📊 Review Progress:
   Last reviewed: June 2015
   Months completed: 65/201
   Progress: 32%
   [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 32%
```

### Find quick-win months

```bash
./photo_tracker.py small
```

Lists months with fewer than 10 photos - these are quick to review!

### Start over

```bash
./photo_tracker.py reset
```

## Daily Workflow

Morning routine (2 minutes):

```bash
./photo_tracker.py
# Opens Photos, tells you what month to search
```

During the day (5-30 minutes when you have time):

- Search for the month in Photos app (⌘F)
- Review photos:
  - Delete unwanted screenshots
  - Remove duplicates
  - Delete blurry photos
  - Create albums for memories
- Go at your own pace - do 1 month or 5 months, up to you!

When finished:

```bash
./photo_tracker.py done 2015-06
```

## Features

### Smart Tips

- Shows photo count per month
- Alerts you if there are screenshots to review
- Suggests search queries

### Flexible Pace

- No minimum photos requirement
- Review one month or keep going
- Take breaks anytime
- Pick up where you left off

### Progress Tracking

- Stores progress in `~/.photo_progress.json`
- Shows percentage complete
- Progress bar visualization
- Tells you how many months remaining

## Search Tips for Photos App

Once Photos is open, use these searches:

**Basic search:**

- `June 2015` - all photos from that month

**Find specific types:**

- `screenshot June 2015` - find screenshots
- `portrait June 2015` - portrait photos
- `video June 2015` - videos only
- `burst June 2015` - burst photo sequences

**Combine with deletions:**

- Search for what you want to delete
- Select all (⌘A)
- Review quickly
- Delete unwanted (⌘ Delete)

## Configuration

### Custom Photos Library Location

If your library isn't in the default location, the tool will find it automatically. If it fails, you can specify:

```python
# Edit the script and set:
LIBRARY_PATH = "/path/to/Photos Library.photoslibrary"
```

### Progress File Location

Progress is saved in: `~/.photo_progress.json`

Format:

```json
{
  "last_reviewed": "2015-06",
  "library_date_range": {
    "first_photo": "2010-01",
    "last_photo": "2026-09"
  }
}
```

You can manually edit this to:

- Skip months (set `last_reviewed` to a later month)
- Start over (delete the file)
- Jump to a specific date

## Troubleshooting

### "Could not find Photos library"

Specify the path in the script or ensure your library is at:

`~/Pictures/Photos Library.photoslibrary`

### "Permission denied"

Grant Full Disk Access:

1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access
3. Add Terminal (or your terminal app)
4. Restart Terminal

### Check if tool can access library

```bash
# Should show your photos
sqlite3 ~/Pictures/Photos\ Library.photoslibrary/database/Photos.sqlite \
  "SELECT COUNT(*) FROM ZASSET WHERE ZTRASHEDSTATE = 0"
```

## Tips & Tricks

### Make it easier to run

Add to `~/.zshrc` or `~/.bashrc`:

```bash
alias photo='cd /path/to/photo_tracker && ./photo_tracker.py'
alias photo-done='cd /path/to/photo_tracker && ./photo_tracker.py done'
```

Then just run: `photo`

### Review strategy

Weekday reviews (quick, 10 min):

- Focus on obvious deletions
- Screenshots, duplicates, clearly bad photos

Weekend reviews (thorough, 30-60 min):

- Create albums for events
- Review similar photos carefully
- Add descriptions and keywords

### Batch small months

Use `./photo_tracker.py small` to find months with <10 photos, then review several in one session.

### Don't be perfect

The goal is progress, not perfection. It's okay to:

- Skip reviewing and just mark it done
- Do a quick pass and come back later
- Focus only on deletions some days

## Scheduling

### Daily reminder (macOS Reminders)

Create a daily reminder:

```
9:00 AM - Review Photos
Run: photo
```

### Automate with launchd (optional)

Create daily notification at 9 AM - see advanced scheduling in original README.

## What This Tool Doesn't Do

- No automated deletion (you control everything)
- No complex analysis (keeps it fast)
- No minimum photo requirements
- No forced workflow

Philosophy: Simple bookmark system that gets out of your way.

## Advanced Usage

### Review multiple months

```bash
# Review June 2015
./photo_tracker.py
# ... review photos ...

# Don't mark done yet, just run again
./photo_tracker.py
# It still shows June, but you can manually review July too

# When you finish both months:
./photo_tracker.py done 2015-07
```

### Jump to a specific month

Edit `~/.photo_progress.json`:

```json
{
  "last_reviewed": "2020-12"
}
```

Next run will start from January 2021.

### Export your progress

```bash
# See detailed progress
./photo_tracker.py status

# View raw data
cat ~/.photo_progress.json
```

### Customization

The script is simple (~300 lines) and easy to modify:

- Change screenshot detection logic
- Add more search tips
- Customize output format
- Add additional statistics

## License

Free to use and modify as needed!
