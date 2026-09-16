# Apple Photo Audit Tracker

A lightweight Python tool to help you systematically audit your Apple Photos library month by month, starting from your oldest photos.

## 🎯 What It Does

Simple progress tracking that remembers where you left off. You control the pace - review one month or keep going, completely up to you!

## ✨ Features

- 📅 **Month-by-month organization** - Review chronologically from oldest to newest
- 📊 **Progress tracking** - Never lose your place
- 🔍 **Search-based workflow** - Faster than creating smart albums
- 📱 **Screenshot detection** - Alerts you to potential cleanup opportunities
- 📈 **Statistics** - Photo counts, progress bars, completion percentage
- 🎯 **Small month finder** - Identify months with <10 photos for quick reviews
- 🖥️ **Dock app support** - Optional GUI or click-to-run app icon
- 🔒 **Read-only & safe** - Never modifies your Photos library
- ⚡ **Zero dependencies** - Pure Python 3 stdlib (GUI version optional)

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/kyleplathe/apple-photo-audit.git
cd apple-photo-audit

# Make executable
chmod +x photo_tracker.py

# Run it!
./photo_tracker.py
```

That's it! The tool will:

1. Show you the next month to review (e.g., "June 2015")
2. Tell you how many photos are in that month
3. Open Photos app
4. You search for that month and review
5. When done, mark it complete

## 📖 Full Documentation

- [START_HERE.md](START_HERE.md) - 2-minute quick start guide
- [QUICKREF.md](QUICKREF.md) - One-page command reference
- [README_simple.md](README_simple.md) - Complete documentation
- [example_usage.md](example_usage.md) - Detailed walkthrough with examples
- [DOCK_APP_GUIDE.md](DOCK_APP_GUIDE.md) - Create a Dock icon

## 💻 Commands

```bash
./photo_tracker.py              # Show next month to review
./photo_tracker.py done 2015-06 # Mark June 2015 as complete
./photo_tracker.py status       # Check your progress
./photo_tracker.py small        # Find months with <10 photos
./photo_tracker.py reset        # Start over
```

## 🖥️ Optional Dock App

Want a click-to-run icon in your Dock?

```bash
# Terminal-based app (simple)
./create_dock_app.sh

# Or try the GUI version
./photo_tracker_gui.py
```

See [DOCK_APP_GUIDE.md](DOCK_APP_GUIDE.md) for full instructions.

## 📸 Daily Workflow

1. **Run the tracker** - Shows next month and stats
2. **Open Photos app** - Auto-opens or press 'y'
3. **Search for month** - Type "June 2015" in Photos search
4. **Review & organize:**
   - Delete unwanted screenshots
   - Remove duplicates
   - Delete blurry photos
   - Create albums for memories
5. **Mark complete** - `./photo_tracker.py done 2015-06`

Takes 5-30 minutes depending on the month!

## 🎨 What to Look For

- ☐ Screenshots you don't need anymore
- ☐ Duplicates - keep only the best version
- ☐ Similar photos - burst sequences, multiple attempts
- ☐ Blurry/poor quality shots
- ☐ Create albums for trips, events, milestones

## 📊 Example Session

```
$ ./photo_tracker.py

📅 Next month to review: June 2015
   Total photos: 147
   📱 12 potential screenshots

📊 Progress: 5/132 months (4%)

QUICK REVIEW TIPS:
1. Search in Photos: June 2015
2. Find screenshots: screenshot June 2015

Open Photos app? (y/n): y

✓ Photos opened - search for: June 2015

When done, run: ./photo_tracker.py done 2015-06
```

## 🔧 Requirements

- macOS (Apple Photos is macOS only)
- Python 3 (pre-installed on macOS)
- Photos app with your photo library

Optional:

- tkinter for GUI version (usually pre-installed)

## 🛡️ Safety & Privacy

- ✅ Read-only database access - Never modifies Photos library
- ✅ No automated deletions - You control everything manually
- ✅ Local storage - Progress saved in `~/.photo_progress.json`
- ✅ No network access - Completely offline tool
- ✅ No data collection - 100% private

## 🗂️ Progress Tracking

Progress is stored in `~/.photo_progress.json`:

```json
{
  "last_reviewed": "2015-06",
  "library_date_range": {
    "first_photo": "2010-03",
    "last_photo": "2026-09"
  }
}
```

You can edit this file to:

- Skip ahead to a specific month
- Go back to re-review months
- Reset your progress

## 🤝 Contributing

Contributions welcome! This is a simple, personal tool - PRs for:

- Bug fixes
- Better Photos database queries
- Enhanced detection algorithms
- macOS integration improvements
- Documentation improvements

## 📝 License

MIT License - Free to use, modify, and distribute

## 🆘 Troubleshooting

**"Permission denied" error**

Grant Full Disk Access:

1. System Preferences → Security & Privacy → Privacy
2. Full Disk Access
3. Add Terminal (or your terminal app)
4. Restart Terminal

**"Could not find Photos library"**

Default location: `~/Pictures/Photos Library.photoslibrary`

If yours is elsewhere, the tool will try to find it automatically.

**More Help**

- [README_simple.md](README_simple.md) - Detailed troubleshooting
- [DOCK_APP_GUIDE.md](DOCK_APP_GUIDE.md) - Dock app issues
- Open an issue on GitHub

## 🌟 Tips

Make it easier to run:

```bash
# Add to your ~/.zshrc or ~/.bashrc
alias photo='~/path/to/apple-photo-audit/photo_tracker.py'
```

Set a daily reminder:

- Use Reminders app: "9:00 AM - Review Photos"
- Takes 5-15 minutes most days
- Consistency beats perfection!

Batch small months:

- Run `./photo_tracker.py small` to find quick wins
- Review several tiny months in one session

## 📚 Alternative Tools

This tool is intentionally simple and lightweight. If you need more features:

- [osxphotos](https://github.com/RhetTbull/osxphotos) - Comprehensive Photos library tool
- Photos Duplicate Cleaner - GUI app for duplicates
- Photos app built-in - Duplicates album (macOS Ventura+)

## 🎯 Philosophy

Simple over sophisticated - Manual review is better than automated deletion
Progress over perfection - Quick pass is better than no pass
Flexible pace - Life happens, pick up where you left off
Your photos, your rules - Tool suggests, you decide

Made with ❤️ for people drowning in 15 years of iPhone photos

Questions? Open an issue or check the docs!
