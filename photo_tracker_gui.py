#!/usr/bin/env python3
"""
Photo Tracker - GUI Launcher
Shows a dialog instead of terminal output when launched from app icon
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess

# Import from main tracker
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from photo_tracker import PhotoLibrary, ProgressTracker, format_month_name
except ImportError:
    messagebox.showerror("Error", "Could not load photo_tracker.py")
    sys.exit(1)


class PhotoTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Tracker")
        self.root.geometry("500x400")
        
        # Initialize
        try:
            self.library = PhotoLibrary()
            self.tracker = ProgressTracker()
            self.all_months = self.library.get_all_months()
        except Exception as e:
            messagebox.showerror("Error", f"Could not access Photos library:\n{e}")
            sys.exit(1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root, 
            text="📸 Photo Audit Tracker", 
            font=("SF Pro", 24, "bold")
        )
        title.pack(pady=20)
        
        # Get next month
        next_month = self.tracker.get_next_month(self.all_months)
        
        if next_month:
            stats = self.library.get_month_stats(next_month)
            month_name = format_month_name(next_month)
            
            # Next month info
            info_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
            info_frame.pack(pady=20, padx=40, fill="x")
            
            tk.Label(
                info_frame,
                text=f"Next to review:",
                font=("SF Pro", 12),
                bg="#f0f0f0"
            ).pack()
            
            tk.Label(
                info_frame,
                text=month_name,
                font=("SF Pro", 20, "bold"),
                bg="#f0f0f0"
            ).pack()
            
            tk.Label(
                info_frame,
                text=f"{stats['total']} photos",
                font=("SF Pro", 14),
                bg="#f0f0f0",
                fg="#666"
            ).pack()
            
            if stats['has_screenshots']:
                tk.Label(
                    info_frame,
                    text=f"📱 {stats['screenshots']} screenshots detected",
                    font=("SF Pro", 12),
                    bg="#f0f0f0",
                    fg="#ff6b00"
                ).pack(pady=5)
            
            # Progress
            progress = self.tracker.get_progress_stats(self.all_months)
            if progress and progress['reviewed_count'] > 0:
                tk.Label(
                    self.root,
                    text=f"Progress: {progress['reviewed_count']}/{progress['total_months']} months ({progress['percent_complete']}%)",
                    font=("SF Pro", 11),
                    fg="#666"
                ).pack()
            
            # Buttons
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(pady=20)
            
            start_btn = tk.Button(
                btn_frame,
                text="🚀 Start Review",
                command=lambda: self.start_review(next_month, month_name),
                font=("SF Pro", 14, "bold"),
                bg="#007AFF",
                fg="white",
                padx=20,
                pady=10,
                cursor="hand2"
            )
            start_btn.pack(pady=5)
            
            status_btn = tk.Button(
                btn_frame,
                text="📊 View Status",
                command=self.show_status,
                font=("SF Pro", 12),
                padx=20,
                pady=8,
                cursor="hand2"
            )
            status_btn.pack(pady=5)
            
        else:
            # All done!
            tk.Label(
                self.root,
                text="🎉",
                font=("SF Pro", 48)
            ).pack(pady=20)
            
            tk.Label(
                self.root,
                text="All photos reviewed!",
                font=("SF Pro", 20, "bold")
            ).pack()
            
            progress = self.tracker.get_progress_stats(self.all_months)
            tk.Label(
                self.root,
                text=f"Completed {progress['total_months']} months",
                font=("SF Pro", 14),
                fg="#666"
            ).pack(pady=10)
    
    def start_review(self, year_month, month_name):
        """Start review process"""
        self.root.withdraw()
        
        # Open Photos
        subprocess.run(['osascript', '-e', 'tell application "Photos" to activate'])
        
        # Show instructions
        msg = f"""Review {month_name}

1. In Photos, search for: {month_name}
2. Review and organize photos
3. Delete unwanted ones
4. Create albums if needed

When done, come back here."""
        
        result = messagebox.askquestion(
            "Photo Review",
            msg + "\n\nMark this month as complete now?",
            icon='question'
        )
        
        if result == 'yes':
            self.tracker.update_last_reviewed(year_month)
            messagebox.showinfo(
                "Progress Saved",
                f"✅ {month_name} marked as reviewed!\n\nRun again to continue with the next month."
            )
            self.root.quit()
        else:
            self.root.deiconify()
    
    def show_status(self):
        """Show status window"""
        progress = self.tracker.get_progress_stats(self.all_months)
        sorted_months = sorted(self.all_months.keys())
        
        msg = f"""Photo Audit Status

Months completed: {progress['reviewed_count']}/{progress['total_months']}
Progress: {progress['percent_complete']}%

Date range: 
  {format_month_name(sorted_months[0])} 
  to {format_month_name(sorted_months[-1])}

Last reviewed: """
        
        if self.tracker.data['last_reviewed']:
            msg += format_month_name(self.tracker.data['last_reviewed'])
        else:
            msg += "Not started yet"
        
        messagebox.showinfo("Status", msg)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PhotoTrackerGUI()
    app.run()
