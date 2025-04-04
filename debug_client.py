import httpx

def get_and_set_cookies(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/set_cookie":
        return httpx.Response(200, headers={"set-cookie": "example-name=example-value"})
    else:
        raise NotImplementedError()

# Create a client with persistent_cookies=True
client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies))

# Print the client's attributes
print("Client attributes:")
for attr in dir(client):
    if not attr.startswith('_') or attr == '_persistent_cookies':
        try:
            value = getattr(client, attr)
            if not callable(value):
                print(f"  {attr}: {value}")
        except Exception as e:
            print(f"  {attr}: Error - {e}")

# Make a request that sets a cookie
response = client.get("http://example.org/set_cookie")

# Print the response cookies
print("\nResponse cookies:", response.cookies)

# Print the client cookies after the request
print("\nClient cookies after request:", client.cookies)