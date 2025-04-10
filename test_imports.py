#!/usr/bin/env python3
"""
A simple script to verify import sorting issues in the repository.
"""

import subprocess
import sys

def main():
    """Run ruff check on the specified files to verify import sorting."""
    files_to_check = [
        "httpx/_config.py",
        "httpx/_transports/default.py"
    ]
    
    print("Checking import sorting in files:")
    for file in files_to_check:
        print(f"- {file}")
    
    # Run ruff check on the specific files
    result = subprocess.run(
        ["ruff", "check"] + files_to_check,
        capture_output=True,
        text=True
    )
    
    print("\nRuff check output:")
    print(result.stdout)
    
    if result.returncode != 0:
        print("Import sorting issues found!")
        return 1
    else:
        print("No import sorting issues found.")
        return 0

if __name__ == "__main__":
    sys.exit(main())