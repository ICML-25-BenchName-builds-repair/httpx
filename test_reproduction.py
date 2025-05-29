#!/usr/bin/env python3
"""
Reproduction script for the import sorting issue in httpx/__init__.py
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return the result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_ruff_check():
    """Test that ruff check passes on httpx/__init__.py"""
    print("Testing ruff check on httpx/__init__.py...")
    
    # Run ruff check
    returncode, stdout, stderr = run_command("ruff check httpx/__init__.py")
    
    if returncode == 0:
        print("✅ PASS: ruff check passed")
        return True
    else:
        print("❌ FAIL: ruff check failed")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        return False

def test_full_check_script():
    """Test that the full check script passes"""
    print("\nTesting full check script...")
    
    # Run the check script
    returncode, stdout, stderr = run_command("./scripts/check")
    
    if returncode == 0:
        print("✅ PASS: check script passed")
        return True
    else:
        print("❌ FAIL: check script failed")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        return False

def main():
    """Main test function"""
    print("=== HTTPX Import Sorting Issue Reproduction ===\n")
    
    # Test individual ruff check
    ruff_pass = test_ruff_check()
    
    # Test full check script
    check_pass = test_full_check_script()
    
    print("\n=== SUMMARY ===")
    if ruff_pass and check_pass:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())