#!/usr/bin/env python3
"""
Reproduction script to verify the SSLContext.__repr__ coverage issue.
"""

import httpx

def test_ssl_context_repr():
    """Test that SSLContext.__repr__ works correctly."""
    
    # Test with verify=True (default)
    context1 = httpx.SSLContext()
    repr_str1 = repr(context1)
    print(f"SSLContext() repr: {repr_str1}")
    assert "SSLContext" in repr_str1
    assert "verify=True" in repr_str1
    
    # Test with verify=False
    context2 = httpx.SSLContext(verify=False)
    repr_str2 = repr(context2)
    print(f"SSLContext(verify=False) repr: {repr_str2}")
    assert "SSLContext" in repr_str2
    assert "verify=False" in repr_str2
    
    # Test with verify as a string path
    import certifi
    context3 = httpx.SSLContext(verify=certifi.where())
    repr_str3 = repr(context3)
    print(f"SSLContext(verify=path) repr: {repr_str3}")
    assert "SSLContext" in repr_str3
    assert "verify=" in repr_str3
    
    print("All SSLContext.__repr__ tests passed!")

if __name__ == "__main__":
    test_ssl_context_repr()