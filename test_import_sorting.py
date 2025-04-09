#!/usr/bin/env python3
"""
Test script to verify the import sorting issue in httpx/__init__.py
"""

import subprocess
import sys

def main():
    """Run ruff check on httpx/__init__.py and report the result."""
    print("Testing import sorting in httpx/__init__.py...")
    
    # Run ruff check on the file
    result = subprocess.run(
        ["ruff", "check", "httpx/__init__.py"],
        capture_output=True,
        text=True
    )
    
    # Print the output
    print("\nCommand output:")
    print(result.stdout)
    
    if result.stderr:
        print("Error output:")
        print(result.stderr)
    
    # Check if there was an error
    if result.returncode != 0:
        print(f"\nTest FAILED: ruff check found issues (exit code {result.returncode})")
        return 1
    else:
        print("\nTest PASSED: No import sorting issues found")
        return 0

if __name__ == "__main__":
    sys.exit(main())