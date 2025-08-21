#!/usr/bin/env python3
"""
Simple line counter - returns raw total of all lines in the repository.
Counts all .py, .txt, and .md files excluding generated files.
"""

import subprocess
import sys
from pathlib import Path

def get_total_lines():
    """Get total lines using system tools for accuracy."""
    try:
        # Use find + wc to get accurate line count
        result = subprocess.run([
            'find', '.', '-type', 'f', 
            '(', '-name', '*.py', '-o', '-name', '*.txt', '-o', '-name', '*.md', ')',
            '-not', '-name', 'count_lines.py',
            '-not', '-name', 'LINE_COUNT_REPORT.md',
            '-not', '-name', 'total_lines.py',
            '-exec', 'wc', '-l', '{}', '+'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            total_line = lines[-1]
            total = total_line.strip().split()[0]
            return int(total)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    total = get_total_lines()
    if total is not None:
        print(f"Total lines of code and text: {total}")
    else:
        print("Error calculating total lines")
        sys.exit(1)