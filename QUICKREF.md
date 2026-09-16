# Photo Tracker - Quick Reference

## Commands

| Command | What it does |
|---|---|
| `./photo_tracker.py` | Show next month to review & open Photos |
| `./photo_tracker.py done 2015-06` | Mark June 2015 as complete |
| `./photo_tracker.py status` | Show progress stats |
| `./photo_tracker.py small` | List months with <10 photos |
| `./photo_tracker.py reset` | Start over from beginning |
| `./photo_tracker.py help` | Show help |

## Daily Workflow

```bash
# 1. Start review
./photo_tracker.py

# 2. In Photos app, search for the month shown (e.g., "June 2015")

# 3. Review photos at your own pace

# 4. Mark complete when done
./photo_tracker.py done 2015-06
```

## Photos App Search Tips

| Search | What it finds |
|---|---|
| `June 2015` | All photos from June 2015 |
| `screenshot June 2015` | Screenshots from that month |
| `video June 2015` | Videos only |
| `burst June 2015` | Burst sequences |
| `portrait June 2015` | Portrait mode photos |

## What to Look For

- ☐ Unwanted screenshots
- ☐ Duplicate photos
- ☐ Multiple similar shots (keep best)
- ☐ Blurry or poor quality
- ☐ Create albums for events

## Progress File

Location: `~/.photo_progress.json`

```json
{
  "last_reviewed": "2015-06"
}
```

Edit this file to skip months or jump to a specific date.

## Troubleshooting

**Permission denied?**

1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access → Add Terminal

**Can't find library?**

- Default location: `~/Pictures/Photos Library.photoslibrary`
- Tool auto-searches with Spotlight

## Tips

- Review at your own pace (1 month or 10 months)
- Use `small` command to find quick-review months
- Check `status` to see progress anytime
- It's okay to skip ahead - just edit the progress file
