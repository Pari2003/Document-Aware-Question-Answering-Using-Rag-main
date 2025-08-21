#!/usr/bin/env python3
"""
Line Counter Tool - Count total lines of code including comments and text content.

This script counts all lines in text-based files within the repository,
including Python files, text files, markdown, and configuration files.
"""

import os
from pathlib import Path
from collections import defaultdict


def count_lines_in_file(file_path):
    """Count lines in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def find_text_files(root_dir):
    """Find all text-based files in the repository."""
    text_extensions = {
        '.py', '.txt', '.md', '.json', '.toml', '.yaml', '.yml', 
        '.ini', '.cfg', '.rst', '.html', '.css', '.js', '.ts',
        '.xml', '.csv', '.sql', '.sh', '.bat'
    }
    
    text_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            # Skip hidden files and directories
            if any(part.startswith('.') for part in file_path.parts[:-1]):
                if '.git' in str(file_path):
                    continue
            
            # Check if it's a text file by extension
            if file_path.suffix.lower() in text_extensions:
                text_files.append(file_path)
            
            # Also check files without extensions that might be text
            elif not file_path.suffix:
                # Check some common text files without extensions
                name = file_path.name.lower()
                if any(keyword in name for keyword in ['readme', 'license', 'changelog', 'makefile']):
                    text_files.append(file_path)
    
    return text_files


def main():
    """Main function to count lines across all text files."""
    # Get the repository root directory - scan the whole directory tree
    repo_root = Path(__file__).parent
    
    print("=" * 80)
    print("LINE COUNTER - Document-Aware Question Answering Using RAG")
    print("=" * 80)
    print(f"Scanning directory: {repo_root}")
    print()
    
    # Find all text files
    text_files = find_text_files(repo_root)
    
    if not text_files:
        print("No text files found!")
        return
    
    # Count lines by file type
    stats_by_extension = defaultdict(lambda: {'files': 0, 'lines': 0})
    total_lines = 0
    total_files = 0
    
    # Detailed file listing
    print("DETAILED FILE BREAKDOWN:")
    print("-" * 80)
    print(f"{'File':<60} {'Lines':<10} {'Type':<10}")
    print("-" * 80)
    
    for file_path in sorted(text_files):
        lines = count_lines_in_file(file_path)
        extension = file_path.suffix.lower() or 'no_ext'
        
        # Relative path for cleaner display
        rel_path = file_path.relative_to(repo_root)
        
        print(f"{str(rel_path):<60} {lines:<10} {extension:<10}")
        
        stats_by_extension[extension]['files'] += 1
        stats_by_extension[extension]['lines'] += lines
        total_lines += lines
        total_files += 1
    
    print("-" * 80)
    print()
    
    # Summary by file type
    print("SUMMARY BY FILE TYPE:")
    print("-" * 50)
    print(f"{'Type':<15} {'Files':<10} {'Lines':<10} {'%':<10}")
    print("-" * 50)
    
    for ext, stats in sorted(stats_by_extension.items()):
        percentage = (stats['lines'] / total_lines * 100) if total_lines > 0 else 0
        print(f"{ext:<15} {stats['files']:<10} {stats['lines']:<10} {percentage:<10.1f}")
    
    print("-" * 50)
    print()
    
    # Final totals
    print("FINAL TOTALS:")
    print("=" * 30)
    print(f"Total Files: {total_files}")
    print(f"Total Lines: {total_lines}")
    print("=" * 30)
    print()
    print("Note: This count includes ALL lines - code, comments, blank lines, and text content.")


if __name__ == "__main__":
    main()