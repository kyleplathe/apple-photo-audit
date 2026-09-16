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

PROGRESS_FILE = os.path.expanduser("~/.photo_progress.json")

def main():
    print("Apple Photos Audit Tracker")
    print("Run './photo_tracker.py help' for usage")
    
if __name__ == "__main__":
    main()
