# Photo Tracker - Start Here

Welcome! This is a simple tool to help you audit your Apple Photos library.

## What You Got

A lightweight Python script that:

- Tracks which months you've reviewed
- Opens Photos app with search instructions
- Shows helpful stats (photo count, screenshots detected)
- Lets you review at your own pace
- Optional enhancements included (small month finder, screenshot detection)

## Quick Start (2 minutes)

### 1. Run it

```bash
./photo_tracker.py
```

### 2. It will show you:

- Next month to review (e.g., "June 2015")
- How many photos in that month
- How many screenshots detected
- Your progress (if not first time)

### 3. Opens Photos app

- Press ⌘F (search)
- Type the month it told you (e.g., "June 2015")
- Review photos, delete unwanted ones, create albums

### 4. When done

```bash
./photo_tracker.py done 2015-06
```

That's it! Run again tomorrow for the next month.

## All Commands

```bash
./photo_tracker.py              # Show next month & open Photos
./photo_tracker.py done 2015-06 # Mark month complete
./photo_tracker.py status       # Check progress
./photo_tracker.py small        # Find months with <10 photos
./photo_tracker.py reset        # Start over
./photo_tracker.py help         # Show help
```

## Documentation

- [QUICKREF.md](QUICKREF.md) - One-page command reference
- [example_usage.md](example_usage.md) - Detailed walkthrough with examples
- [README_simple.md](README_simple.md) - Complete documentation

## Troubleshooting

**"Permission denied" error**

Grant Full Disk Access to Terminal:

1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access
3. Click lock to unlock
4. Click + and add Terminal (or iTerm, etc.)
5. Restart Terminal

**Can't find Photos library**

Default location: `~/Pictures/Photos Library.photoslibrary`

If yours is elsewhere, the script will try to find it with Spotlight.

## Tips

**Make it easier to run**

Add to your `~/.zshrc`:

```bash
alias photo='~/path/to/photo_tracker.py'
```

Then just type: `photo`

**Daily habit**

Set a daily reminder:

- "9:00 AM - Review photos"
- Takes 5-15 minutes
- Run `photo` and go through one month

**Don't overthink it**

- It's okay to review multiple months at once
- It's okay to do a quick pass
- Progress over perfection!

## Features Included

- ✅ Simple progress tracking (JSON file)
- ✅ Shows next month to review
- ✅ Opens Photos app automatically
- ✅ Photo count per month
- ✅ Screenshot detection hints
- ✅ Progress bar and statistics
- ✅ Small month finder (<10 photos)
- ✅ Flexible pace - no minimums
- ✅ Search-based workflow (faster than smart albums)

## What to Look For While Reviewing

- 📱 Screenshots you don't need
- 🔄 Duplicate photos
- 👁️ Multiple similar shots (keep the best)
- 🌫️ Blurry or poor quality
- 📚 Create albums for trips/events

## Example Session

```
$ ./photo_tracker.py

📅 Next month to review: June 2015
   Total photos: 147
   📱 12 potential screenshots

QUICK REVIEW TIPS:
1. Search in Photos: June 2015
2. Find screenshots: screenshot June 2015

Open Photos app? (y/n): y

✓ Photos opened - search for: June 2015
When done, run: ./photo_tracker.py done 2015-06
```

Ready? → `./photo_tracker.py`

Questions? Check [README_simple.md](README_simple.md) or [example_usage.md](example_usage.md)
