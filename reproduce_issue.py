import httpx
import logging
import http.cookiejar

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("httpx")

# Monkey patch CookieJar.extract_cookies to add debug logging
original_extract_cookies = http.cookiejar.CookieJar.extract_cookies

def debug_extract_cookies(self, response, request):
    print(f"CookieJar.extract_cookies called with response: {response}, request: {request}")
    print(f"Response headers: {response.info()}")
    print(f"Request URL: {request.get_full_url()}")
    print(f"CookieJar before: {list(self)}")
    result = original_extract_cookies(self, response, request)
    print(f"CookieJar after: {list(self)}")
    return result

http.cookiejar.CookieJar.extract_cookies = debug_extract_cookies

def get_and_set_cookies(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/echo_cookies":
        data = {"cookies": request.headers.get("cookie")}
        return httpx.Response(200, json=data)
    elif request.url.path == "/set_cookie":
        return httpx.Response(200, headers={"set-cookie": "example-name=example-value"})
    else:
        raise NotImplementedError()

def cookie_sessions(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/":
        cookie = request.headers.get("Cookie")
        if cookie is not None:
            content = b"Logged in"
        else:
            content = b"Not logged in"
        return httpx.Response(200, content=content)
    elif request.url.path == "/login":
        status_code = httpx.codes.SEE_OTHER
        headers = {
            "location": "/",
            "set-cookie": (
                "session=eyJ1c2VybmFtZSI6ICJ0b21; path=/; Max-Age=1209600; "
                "httponly; samesite=lax"
            ),
        }
        return httpx.Response(status_code, headers=headers)
    else:
        raise NotImplementedError()

# Test 1: Cookie persistence
def test_cookie_persistence():
    client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))
    print(f"Test 1 - Client persistent_cookies: {client._persistent_cookies}")
    
    # First request doesn't set any cookies
    response = client.get("http://example.org/echo_cookies")
    print(f"Test 1 - First response cookies: {response.json()}")
    
    # Second request should set a cookie
    response = client.get("http://example.org/set_cookie")
    print(f"Test 1 - Response cookies: {response.cookies}")
    
    # Check if the cookie is in the client's cookie jar
    print(f"Test 1 - Client cookies jar: {list(client.cookies.jar)}")
    try:
        print(f"Test 1 - Client cookies: {client.cookies['example-name']}")
        print("Test 1 PASSED")
    except KeyError:
        print("Test 1 FAILED: Cookie not found in client's cookie jar")

# Test 2: Redirect cookie behavior
def test_redirect_cookie_behavior():
    client = httpx.Client(
        transport=httpx.MockTransport(cookie_sessions), follow_redirects=True
    )
    
    # The client is not logged in.
    response = client.get("https://example.com/")
    print(f"Test 2 - Initial state: {response.text}")
    
    # Login redirects to the homepage, setting a session cookie.
    response = client.post("https://example.com/login")
    print(f"Test 2 - After login: {response.text}")
    
    if response.text == "Logged in":
        print("Test 2 PASSED")
    else:
        print("Test 2 FAILED: Not logged in after redirect")

if __name__ == "__main__":
    print("Running test for cookie persistence...")
    test_cookie_persistence()
    
    print("\nRunning test for redirect cookie behavior...")
    test_redirect_cookie_behavior()