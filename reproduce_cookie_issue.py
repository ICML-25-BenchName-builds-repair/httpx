import httpx

def get_and_set_cookies(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/echo_cookies":
        data = {"cookies": request.headers.get("cookie")}
        return httpx.Response(200, json=data)
    elif request.url.path == "/set_cookie":
        return httpx.Response(200, headers={"set-cookie": "example-name=example-value"})
    else:
        raise NotImplementedError()

def test_get_cookie():
    url = "http://example.org/set_cookie"
    
    client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))
    response = client.get(url)
    
    print("Response cookies:", response.cookies)
    print("Client cookies:", client.cookies)
    
    try:
        assert response.cookies["example-name"] == "example-value"
        assert client.cookies["example-name"] == "example-value"
        print("Test passed!")
    except (AssertionError, KeyError) as e:
        print(f"Test failed: {e}")

def test_cookie_persistence():
    client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))
    
    response = client.get("http://example.org/echo_cookies")
    print("Initial response cookies:", response.json())
    
    response = client.get("http://example.org/set_cookie")
    print("Set-cookie response cookies:", response.cookies)
    print("Client cookies after set-cookie:", client.cookies)
    
    try:
        assert response.cookies["example-name"] == "example-value"
        assert client.cookies["example-name"] == "example-value"
        print("Test passed!")
    except (AssertionError, KeyError) as e:
        print(f"Test failed: {e}")

def cookie_sessions(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/":
        cookie = request.headers.get("Cookie")
        if cookie is not None:
            content = b"Logged in"
        else:
            content = b"Not logged in"
        return httpx.Response(200, content=content)
    
    elif request.url.path == "/login":
        status_code = 303  # SEE_OTHER
        headers = {
            "location": "/",
            "set-cookie": (
                "session=eyJ1c2VybmFtZSI6ICJ0b21; path=/; Max-Age=1209600; "
                "httponly; samesite=lax"
            ),
        }
        return httpx.Response(status_code, headers=headers)

def test_redirect_cookie_behavior():
    client = httpx.Client(
        transport=httpx.MockTransport(cookie_sessions), follow_redirects=True
    )
    
    # The client is not logged in.
    response = client.get("https://example.com/")
    print("Initial response:", response.text)
    
    # Login redirects to the homepage, setting a session cookie.
    response = client.post("https://example.com/login")
    print("Login response URL:", response.url)
    print("Login response text:", response.text)
    print("Client cookies after login:", client.cookies)
    
    try:
        assert response.text == "Logged in"
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    print("\n=== Testing get_cookie ===")
    test_get_cookie()
    
    print("\n=== Testing cookie_persistence ===")
    test_cookie_persistence()
    
    print("\n=== Testing redirect_cookie_behavior ===")
    test_redirect_cookie_behavior()