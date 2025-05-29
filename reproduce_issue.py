#!/usr/bin/env python3
"""
Script to reproduce the mypy type checking issue.
This script runs mypy on the specific file and shows the errors.
"""

import subprocess
import sys

def run_mypy_check():
    """Run mypy on the httpx/_client.py file to reproduce the issue."""
    print("Running mypy on httpx/_client.py to reproduce the issue...")
    
    try:
        result = subprocess.run(
            ["mypy", "httpx/_client.py"],
            capture_output=True,
            text=True,
            cwd="/lca-workspace/repos/encode__httpx"
        )
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        if result.returncode != 0:
            print("\n✗ MyPy found type errors (as expected)")
            return False
        else:
            print("\n✓ MyPy passed (issue is fixed)")
            return True
            
    except FileNotFoundError:
        print("Error: mypy not found. Please install mypy.")
        return False

if __name__ == "__main__":
    success = run_mypy_check()
    sys.exit(0 if success else 1)