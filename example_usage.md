# Example Usage

## First Time Setup

```bash
# Make executable
chmod +x photo_tracker.py

# Check your library
./photo_tracker.py status
```

Example output:

```
Apple Photos Audit Status
==========================================================

Library: /Users/john/Pictures/Photos Library.photoslibrary
Total photos: 15,234
Date range: March 2010 to September 2026
Total months: 199

📍 Not started yet
   Run './photo_tracker.py' to begin with March 2010
```

## Starting Your First Review

```bash
./photo_tracker.py
```

Example output:

```
Apple Photos Audit Tracker
==========================================================

📅 Next month to review: March 2010
   Total photos: 89
   📱 5 potential screenshots

==========================================================
QUICK REVIEW TIPS:
==========================================================

1. Search in Photos: March 2010
2. Find screenshots: screenshot March 2010

What to look for:
  • Delete unwanted screenshots
  • Remove duplicates and similar photos
  • Delete blurry or poor quality shots
  • Create albums for events/trips

==========================================================
Open Photos app? (y/n): y

✓ Photos opened - search for: March 2010

When done, run: ./photo_tracker.py done 2010-03
```

## In Photos App

1. Press ⌘F to open search
2. Type: `March 2010`
3. Review all the photos
4. Delete unwanted ones (⌘ Delete)
5. Create albums if needed (File → New Album)

## Marking Complete

```bash
./photo_tracker.py done 2010-03
```

Output:

```
✓ Marked March 2010 as reviewed!

📊 Progress: 1/199 months (0% complete)
   198 months remaining
```

## Continuing Next Day

```bash
./photo_tracker.py
```

Output:

```
📅 Next month to review: April 2010
   Total photos: 124

📊 Progress: 1/199 months (0%)
```

## Checking Progress

```bash
./photo_tracker.py status
```

After reviewing 50 months:

```
Apple Photos Audit Status
==========================================================

Library: /Users/john/Pictures/Photos Library.photoslibrary
Total photos: 15,234
Date range: March 2010 to September 2026
Total months: 199

📊 Review Progress:
   Last reviewed: April 2014
   Months completed: 50/199
   Progress: 25%
   [██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 25%

   Next up: May 2014
```

## Finding Quick Wins

```bash
./photo_tracker.py small
```

Output:

```
Months with <10 photos (quick review candidates):
==========================================================
  February 2011: 3 photos
  August 2012: 7 photos
  November 2013: 5 photos
  December 2019: 2 photos
  February 2021: 4 photos

Total: 5 months
```

These are perfect for a quick 2-minute review session!

## Reviewing Multiple Months in One Session

You can keep going without marking done:

```bash
# Day 1 - review June, July, August 2015
./photo_tracker.py  # Shows June 2015
# Review June...
# Review July...
# Review August...

# Mark all three done
./photo_tracker.py done 2015-08  # Marks through August
```

## Jumping Ahead

Maybe you want to start with recent photos instead:

```bash
# Edit progress file
nano ~/.photo_progress.json
```

Change to:

```json
{
  "last_reviewed": "2025-12"
}
```

Next run starts from January 2026!

## Real-World Example: Weekend Batch

Saturday morning - check what's next:

```bash
./photo_tracker.py status
# Shows: Next up: June 2015 (67 photos)
```

Start review:

```bash
./photo_tracker.py
# Opens Photos, shows "June 2015"
```

In Photos:

- Search "June 2015" → 67 photos
- Search "screenshot June 2015" → 12 screenshots
- Delete 8 unwanted screenshots
- Notice 15 photos from a hiking trip
- Select all 15
- File → New Album → "Mt. Rainier Hike June 2015"
- Find 3 duplicates, delete 2
- Find 5 blurry photos, delete them

Result: Deleted 15 photos, created 1 album

Feeling motivated, continue:

```bash
./photo_tracker.py
# Now shows July 2015 (89 photos)
```

Repeat the process...

After reviewing June, July, August:

```bash
./photo_tracker.py done 2015-08
```

Output:

```
✓ Marked August 2015 as reviewed!

📊 Progress: 68/199 months (34% complete)
   131 months remaining
```

Not bad for a Saturday!

## Tips from the Example

- Screenshots are low-hanging fruit - search for them first
- Create albums while reviewing - fresh in your memory
- Batch similar months - if motivated, keep going!
- It's okay to be imperfect - quick pass is better than none
- Check progress regularly - it's motivating to see the bar fill up!
