#!/bin/bash
# Create Photo Tracker app for Dock - Simple version using osacompile

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_PATH="$HOME/Desktop/Photo Tracker.app"

echo "Creating Photo Tracker app..."

# Create AppleScript that launches the tracker
cat > /tmp/photo_tracker_launcher.applescript << EOF
on run
	do shell script "cd '$SCRIPT_DIR' && open -a Terminal '$SCRIPT_DIR/photo_tracker.py'"
end run
EOF

# Compile to application
osacompile -o "$APP_PATH" /tmp/photo_tracker_launcher.applescript

# Clean up
rm /tmp/photo_tracker_launcher.applescript

echo ""
echo "✅ Photo Tracker.app created on Desktop!"
echo ""
echo "📍 Location: ~/Desktop/Photo Tracker.app"
echo ""
echo "To add to Dock:"
echo "  • Drag the app from Desktop to your Dock"
echo ""
echo "To customize icon:"
echo "  1. Download a photos icon (PNG/ICNS)"
echo "  2. Right-click Photo Tracker.app → Get Info"
echo "  3. Drag icon to the small icon in top-left of Info window"
echo ""
echo "Suggested icon sources:"
echo "  • SF Symbols app (free from Apple)"
echo "  • https://www.flaticon.com/search?word=photos"
echo "  • https://icons8.com/icons/set/photo-gallery"
echo ""

cat << 'ICON_INFO'

╔══════════════════════════════════════════════════════════╗
║  SUGGESTED ICON: 📸                                      ║
╟──────────────────────────────────────────────────────────╢
║  The app will use a default icon initially.              ║
║  To add a nice custom icon:                              ║
║                                                          ║
║  1. Find/create an icon that represents photos          ║
║  2. Get Info on Photo Tracker.app (⌘I)                  ║
║  3. Drag your icon to the tiny icon in top-left         ║
║                                                          ║
║  Icon ideas:                                             ║
║  • Camera icon 📷                                        ║
║  • Photo album icon 🖼️                                   ║
║  • Gallery icon 🎨                                       ║
║  • Magnifying glass over photos 🔍                      ║
╚══════════════════════════════════════════════════════════╝

ICON_INFO

echo "Done! Double-click the app to test it."
