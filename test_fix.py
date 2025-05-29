#!/usr/bin/env python3
"""
Comprehensive test to verify the fix works correctly.
This tests that AsyncClient can be instantiated and the _init_proxy_transport method works.
"""

import asyncio
import sys
import traceback
from httpx import AsyncClient
from httpx._config import Proxy, DEFAULT_LIMITS

async def test_async_client_proxy_transport():
    """Test that AsyncClient._init_proxy_transport works correctly."""
    print("Testing AsyncClient._init_proxy_transport method...")
    
    try:
        # Create an AsyncClient instance
        async with AsyncClient() as client:
            print("✓ AsyncClient instantiated successfully")
            
            # Test the _init_proxy_transport method
            proxy = Proxy("http://proxy.example.com:8080")
            transport = client._init_proxy_transport(
                proxy=proxy,
                ssl_context=None,
                http1=True,
                http2=False,
                limits=DEFAULT_LIMITS
            )
            
            print("✓ _init_proxy_transport method executed successfully")
            print(f"✓ Transport type: {type(transport)}")
            
            # Verify the transport has the expected attributes
            assert hasattr(transport, '_pool'), "Transport should have _pool attribute"
            print("✓ Transport has expected attributes")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
        return False

def test_sync_async_consistency():
    """Test that sync and async versions have consistent behavior."""
    print("\nTesting sync/async consistency...")
    
    try:
        from httpx import Client
        
        # Test sync version
        with Client() as sync_client:
            proxy = Proxy("http://proxy.example.com:8080")
            sync_transport = sync_client._init_proxy_transport(
                proxy=proxy,
                ssl_context=None,
                http1=True,
                http2=False,
                limits=DEFAULT_LIMITS
            )
            print("✓ Sync _init_proxy_transport works")
            
        # Compare method signatures (they should be similar)
        import inspect
        sync_sig = inspect.signature(Client._init_proxy_transport)
        async_sig = inspect.signature(AsyncClient._init_proxy_transport)
        
        # Remove 'self' parameter for comparison
        sync_params = list(sync_sig.parameters.keys())[1:]
        async_params = list(async_sig.parameters.keys())[1:]
        
        if sync_params == async_params:
            print("✓ Sync and async method signatures are consistent")
            return True
        else:
            print(f"✗ Method signatures differ: sync={sync_params}, async={async_params}")
            return False
            
    except Exception as e:
        print(f"✗ Error in consistency test: {e}")
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("Running comprehensive tests for the fix...\n")
    
    # Test 1: Basic functionality
    test1_passed = await test_async_client_proxy_transport()
    
    # Test 2: Sync/async consistency
    test2_passed = test_sync_async_consistency()
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY:")
    print(f"✓ AsyncClient proxy transport test: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✓ Sync/async consistency test: {'PASSED' if test2_passed else 'FAILED'}")
    
    all_passed = test1_passed and test2_passed
    print(f"\nOverall result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)