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
        print("Response cookie value:", response.cookies["example-name"])
        print("Client cookie value:", client.cookies["example-name"])
    except KeyError as e:
        print(f"KeyError: {e}")

def test_cookie_persistence():
    client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))
    
    response = client.get("http://example.org/echo_cookies")
    print("Initial echo cookies response:", response.json())
    
    response = client.get("http://example.org/set_cookie")
    print("Set cookie response cookies:", response.cookies)
    print("Client cookies after set_cookie:", client.cookies)
    
    try:
        print("Client cookie value:", client.cookies["example-name"])
    except KeyError as e:
        print(f"KeyError: {e}")
    
    response = client.get("http://example.org/echo_cookies")
    print("Final echo cookies response:", response.json())

if __name__ == "__main__":
    print("Testing get_cookie:")
    test_get_cookie()
    print("\nTesting cookie_persistence:")
    test_cookie_persistence()