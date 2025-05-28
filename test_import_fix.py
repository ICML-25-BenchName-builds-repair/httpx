#!/usr/bin/env python3
"""
Test script to reproduce and verify the import sorting issue.
"""
import subprocess
import sys

def run_ruff_check():
    """Run ruff check and return the result."""
    try:
        result = subprocess.run(
            ["ruff", "check", "httpx", "tests"],
            capture_output=True,
            text=True,
            cwd="/lca-workspace/repos/encode__httpx"
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def main():
    print("Testing import sorting issues...")
    print("=" * 50)
    
    # Run ruff check
    returncode, stdout, stderr = run_ruff_check()
    
    print(f"Return code: {returncode}")
    print(f"STDOUT:\n{stdout}")
    if stderr:
        print(f"STDERR:\n{stderr}")
    
    # Check for specific errors that should NOT be present after fix
    problematic_errors = [
        "httpx/_config.py:1:1: I001",
        "httpx/_transports/default.py:26:1: I001"
    ]
    
    found_errors = []
    for error in problematic_errors:
        if error in stdout:
            found_errors.append(error)
    
    if found_errors:
        print("\nProblematic errors still found:")
        for error in found_errors:
            print(f"  ✗ {error}")
    else:
        print("\n✅ No problematic import errors found!")
    
    # Check for any I001 errors at all
    if "I001" in stdout:
        print(f"\n⚠️  WARNING: Other I001 import errors detected:\n{stdout}")
    
    if returncode == 0:
        print("\n✅ SUCCESS: No import sorting issues found!")
        return True
    else:
        print(f"\n❌ FAILURE: Import sorting issues detected (exit code: {returncode})")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)