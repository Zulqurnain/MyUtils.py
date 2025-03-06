#!/usr/bin/env python3
"""
Batch File Renamer Utility

This script provides functionality to rename multiple files in a directory using
either simple pattern replacement or regular expressions. It includes a dry-run
mode for safe testing and handles duplicate filenames.

Author: Zulqurnain Haider
Email: zulqurnainjj@gmail.com
"""

import os
import re
import argparse
from pathlib import Path

def rename_files(directory, pattern, replacement, regex=False, dry_run=False):
    """
    Rename files in the directory based on pattern.
    
    Args:
        directory (str): Path to the directory containing files to rename
        pattern (str): Pattern to search for in filenames
        replacement (str): Text to replace the pattern with
        regex (bool, optional): Whether to use regex for pattern matching. Defaults to False
        dry_run (bool, optional): Whether to simulate the renaming. Defaults to False
    
    Returns:
        bool: True if all operations were successful, False if any errors occurred
    
    Example:
        >>> rename_files("./docs", "old", "new")
        Found 5 files in directory
        Renamed: oldfile.txt → newfile.txt
        Renamed: old_doc.pdf → new_doc.pdf
        
        Summary:
        Renamed: 2 files
        True
    """
    directory = Path(directory)
    renamed_count = 0
    errors = 0
    
    try:
        # Validate directory
        if not directory.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory}")
        
        # Get list of files
        files = [f for f in directory.iterdir() if f.is_file()]
        if not files:
            print("No files found in directory")
            return True
        
        print(f"Found {len(files)} files in directory")
        if dry_run:
            print("\nDRY RUN - No files will be renamed\n")
        
        for file_path in files:
            try:
                old_name = file_path.name
                if regex:
                    new_name = re.sub(pattern, replacement, old_name)
                else:
                    new_name = old_name.replace(pattern, replacement)
                
                if new_name != old_name:
                    new_path = file_path.parent / new_name
                    
                    # Check if target file already exists
                    if new_path.exists() and not dry_run:
                        print(f"Error: Target file already exists: {new_name}")
                        errors += 1
                        continue
                    
                    if not dry_run:
                        file_path.rename(new_path)
                        print(f"Renamed: {old_name} → {new_name}")
                    else:
                        print(f"Would rename: {old_name} → {new_name}")
                    renamed_count += 1
            
            except Exception as e:
                print(f"Error processing {file_path.name}: {str(e)}")
                errors += 1
        
        print(f"\nSummary:")
        print(f"{'Would rename' if dry_run else 'Renamed'}: {renamed_count} files")
        if errors > 0:
            print(f"Errors encountered: {errors}")
        
        return errors == 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """
    Main function to handle command-line arguments and execute batch renaming.
    
    The script accepts the following arguments:
    1. Directory path
    2. Pattern to search for
    3. Replacement text
    4. Optional flags:
       - --regex: Use regular expressions
       - --dry-run: Simulate the renaming
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Batch rename files in a directory",
        epilog="For issues or suggestions, contact: zulqurnainjj@gmail.com"
    )
    parser.add_argument("directory", help="Directory containing files to rename")
    parser.add_argument("pattern", help="Pattern to search for")
    parser.add_argument("replacement", help="Replacement text")
    parser.add_argument("--regex", action="store_true", help="Use regular expressions")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be renamed without making changes")
    
    args = parser.parse_args()
    success = rename_files(args.directory, args.pattern, args.replacement, args.regex, args.dry_run)
    if not success:
        exit(1)

if __name__ == "__main__":
    main() 