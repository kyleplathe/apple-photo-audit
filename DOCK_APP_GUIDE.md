# Create Dock App for Photo Tracker

Add Photo Tracker to your macOS Dock for one-click access!

## Quick Setup (Recommended)

### Option 1: Simple App (Terminal-based)

```bash
./create_dock_app.sh
```

This creates `Photo Tracker.app` on your Desktop that you can:

- Double-click to run
- Drag to Dock for permanent access
- Opens in Terminal for traditional interface

### Option 2: GUI App (Dialog-based)

If you prefer a graphical interface with dialogs instead of Terminal:

```bash
# The GUI version is already created
# Just make it launchable:
chmod +x photo_tracker_gui.py

# Test it:
./photo_tracker_gui.py
```

Then create an app wrapper for it (instructions below).

## Detailed Instructions

### Creating the Terminal App

1. Run the creation script:

```bash
cd /path/to/photo_tracker
./create_dock_app.sh
```

2. Test it:
   - Go to your Desktop
   - Double-click "Photo Tracker.app"
   - Should open Terminal and run the tracker

3. Add to Dock:
   - Drag the app from Desktop to your Dock
   - Or right-click the running app in Dock → Options → Keep in Dock

### Creating the GUI App

For a more native macOS experience with dialog boxes:

1. Open Automator (Applications → Automator)
2. Create New Application — choose "Application" as document type
3. Add Run Shell Script action:
   - Search for "Run Shell Script" in the actions list
   - Drag it to the workflow area
   - Enter this script:

```bash
cd /path/to/your/photo_tracker
python3 photo_tracker_gui.py
```

(Replace `/path/to/your/photo_tracker` with actual path)

4. Save:
   - File → Save (⌘S)
   - Name: "Photo Tracker"
   - Save to: Desktop or Applications
   - Format: Application

5. Add to Dock:
   - Find the saved app
   - Drag it to your Dock

### Using AppleScript Editor (Alternative)

1. Open Script Editor (Applications → Utilities → Script Editor)
2. Paste this code:

```applescript
set scriptPath to "/path/to/your/photo_tracker/photo_tracker.py"

tell application "Terminal"
    activate
    do script "cd $(dirname " & quoted form of scriptPath & ") && " & scriptPath
end tell
```

3. Save as Application:
   - File → Export
   - File Format: Application
   - Name: Photo Tracker
   - Location: Desktop or Applications

## Customizing the Icon

### Finding Good Icons

Free sources:

- SF Symbols app (free from Apple Developer)
- Flaticon
- Icons8
- Noun Project

Suggested keywords: camera, photo album, gallery, pictures

### Applying Custom Icon

1. Prepare your icon:
   - Get an image file (PNG, JPG, or ICNS)
   - Ideally 512x512 pixels or larger
   - Square format works best

2. Copy icon image to clipboard:
   - Open the icon image in Preview
   - Select All (⌘A)
   - Copy (⌘C)

3. Apply to app:
   - Select your "Photo Tracker.app"
   - Get Info (⌘I)
   - Click the tiny icon in top-left corner
   - Paste (⌘V)

Done! The new icon should appear immediately.

### Creating an Icon with Emojis (macOS Monterey+)

1. Get Info on your app (⌘I)
2. Click the small icon in top-left
3. Open Character Viewer (Control-Command-Space)
4. Find a good emoji: 📸 📷 🖼️ 🎨 📚
5. Drag emoji to the icon area

Note: Emoji icons look good but are less "pro" looking.

## Features of Each Version

**Terminal App**

- ✅ Fast startup
- ✅ Full featured (all commands)
- ✅ Familiar terminal interface
- ✅ Easy to create
- ✅ Works on any macOS version

**GUI App**

- ✅ Native macOS look
- ✅ Dialog boxes instead of terminal
- ✅ Click-based interface
- ✅ Better for non-technical users
- ✅ Cleaner appearance

## Testing Your App

### First Test

1. Double-click the app
2. Should see either Terminal window or GUI dialog
3. Should show next month to review

### If It Doesn't Work

**Terminal app opens but shows error:**

- Check the path in the app is correct
- Make sure `photo_tracker.py` is executable (`chmod +x`)

**App bounces in Dock and quits:**

- Right-click app → Show Package Contents
- Check `Contents/MacOS/Photo Tracker`
- Verify paths are correct

**GUI app shows Python errors:**

- Make sure tkinter is installed: `python3 -m tkinter`
- On macOS, it's usually included with Python 3

**Permission errors:**

- System Preferences → Security & Privacy → Privacy
- Full Disk Access → Add Terminal or your app

## Keyboard Shortcuts

Once in Dock, you can:

- ⌘ + number - Launch if app is in that dock position
- ⌥ + click - Show app in Finder
- ⌘ + drag - Rearrange position in Dock

## Automating Further

### Launch at Login

1. System Preferences → Users & Groups
2. Login Items
3. Click + and add your Photo Tracker.app

App will launch when you log in.

Not recommended - photo review should be intentional, not automatic!

### Daily Reminder

Better approach - use Reminders or Calendar:

1. Open Reminders app
2. Create new reminder: "Review Photos"
3. Set to repeat daily at your preferred time
4. Add note: "Run Photo Tracker in Dock"

## Troubleshooting

### App won't open - "unidentified developer"

macOS Gatekeeper might block apps you create:

1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog
4. This adds it to allowed apps

### Wrong Python version

If you have multiple Python installations, edit the app script to use specific Python:

```bash
/usr/local/bin/python3 photo_tracker.py
# or
/opt/homebrew/bin/python3 photo_tracker.py
```

### Dock icon is generic

This is normal for newly created apps. Follow the "Customizing the Icon" section above.

## Advanced: Creating ICNS Icon

For best results, create a proper `.icns` file:

1. Install iconutil (included with Xcode)
2. Create iconset folder:

```bash
mkdir MyIcon.iconset
```

3. Add images at different sizes:
   - icon_16x16.png
   - icon_32x32.png
   - icon_128x128.png
   - icon_256x256.png
   - icon_512x512.png
   - And @2x versions of each

4. Convert to ICNS:

```bash
iconutil -c icns MyIcon.iconset
```

5. Apply to app:
   - Copy `MyIcon.icns` to `Photo Tracker.app/Contents/Resources/`
   - Rename to `AppIcon.icns`
   - Update Info.plist if needed

## Examples

### My Recommended Setup

1. Create GUI app with Automator (clean, modern)
2. Find a nice camera icon from SF Symbols
3. Add to right side of Dock (with other utilities)
4. Set daily reminder for 9 AM
5. Click once per day, review photos, mark complete

### Quick Terminal Setup

1. Run `./create_dock_app.sh`
2. Drag app to Dock
3. Done! No icon customization needed.

Questions? Check the main [README_simple.md](README_simple.md) or open an issue.
