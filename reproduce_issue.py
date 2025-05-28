#!/usr/bin/env python3
"""
Script to reproduce the cookie persistence issue in httpx.

This script demonstrates that cookies from HTTP responses are not being
persisted to the client's cookie jar when using the default settings.
"""

import httpx


def get_and_set_cookies(request: httpx.Request) -> httpx.Response:
    """Mock transport function that sets cookies in responses."""
    if request.url.path == "/echo_cookies":
        data = {"cookies": request.headers.get("cookie")}
        return httpx.Response(200, json=data)
    elif request.url.path == "/set_cookie":
        return httpx.Response(200, headers={"set-cookie": "example-name=example-value"})
    else:
        raise NotImplementedError()


def test_cookie_persistence_issue():
    """Test that reproduces the cookie persistence issue."""
    print("Testing cookie persistence issue...")
    
    # Create client with default settings (no explicit persistent_cookies parameter)
    client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))
    
    print(f"Initial client cookies: {dict(client.cookies)}")
    
    # Make request that sets a cookie
    response = client.get("http://example.org/set_cookie")
    print(f"Response status: {response.status_code}")
    print(f"Response cookies: {dict(response.cookies)}")
    
    # Check if cookie is in response (this should work)
    try:
        response_cookie = response.cookies["example-name"]
        print(f"✓ Cookie found in response: {response_cookie}")
    except KeyError:
        print("✗ Cookie NOT found in response")
        return False
    
    # Check if cookie is persisted to client (this currently fails)
    try:
        client_cookie = client.cookies["example-name"]
        print(f"✓ Cookie found in client: {client_cookie}")
        return True
    except KeyError:
        print("✗ Cookie NOT found in client (THIS IS THE BUG)")
        print(f"Client cookies after response: {dict(client.cookies)}")
        return False


def test_with_explicit_persistent_cookies_true():
    """Test with explicit persistent_cookies=True."""
    print("\nTesting with explicit persistent_cookies=True...")
    
    client = httpx.Client(
        transport=httpx.MockTransport(get_and_set_cookies),
        persistent_cookies=True
    )
    
    response = client.get("http://example.org/set_cookie")
    print(f"Response status: {response.status_code}")
    
    try:
        client_cookie = client.cookies["example-name"]
        print(f"✓ Cookie found in client with persistent_cookies=True: {client_cookie}")
        return True
    except KeyError:
        print("✗ Cookie NOT found in client even with persistent_cookies=True")
        return False


def test_with_explicit_persistent_cookies_false():
    """Test with explicit persistent_cookies=False."""
    print("\nTesting with explicit persistent_cookies=False...")
    
    client = httpx.Client(
        transport=httpx.MockTransport(get_and_set_cookies),
        persistent_cookies=False
    )
    
    response = client.get("http://example.org/set_cookie")
    print(f"Response status: {response.status_code}")
    
    try:
        client_cookie = client.cookies["example-name"]
        print(f"✗ Cookie found in client with persistent_cookies=False: {client_cookie}")
        return False
    except KeyError:
        print("✓ Cookie correctly NOT found in client with persistent_cookies=False")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("HTTPX Cookie Persistence Issue Reproduction")
    print("=" * 60)
    
    # Test the main issue
    issue_reproduced = not test_cookie_persistence_issue()
    
    # Test with explicit settings
    explicit_true_works = test_with_explicit_persistent_cookies_true()
    explicit_false_works = test_with_explicit_persistent_cookies_false()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Issue reproduced (default behavior fails): {issue_reproduced}")
    print(f"Explicit persistent_cookies=True works: {explicit_true_works}")
    print(f"Explicit persistent_cookies=False works: {explicit_false_works}")
    
    if not issue_reproduced and explicit_true_works and explicit_false_works:
        print("\n✓ Issue FIXED: Default behavior now works correctly")
    elif issue_reproduced and explicit_true_works and explicit_false_works:
        print("\n✓ Issue confirmed: Default behavior should be persistent_cookies=True")
    else:
        print("\n? Unexpected behavior detected")
    
    print("=" * 60)