import httpx
from http.cookiejar import CookieJar

def get_and_set_cookies(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/set_cookie":
        return httpx.Response(200, headers={"set-cookie": "example-name=example-value"})
    else:
        raise NotImplementedError()

# Create a client with persistent_cookies=True
client = httpx.Client(transport=httpx.MockTransport(get_and_set_cookies), persistent_cookies=True)

# Print the initial state
print("Initial client.cookies:", client.cookies)
print("Initial client._persistent_cookies:", client._persistent_cookies)

# Make a request that sets a cookie
response = client.get("http://example.org/set_cookie")

# Print the response cookies
print("\nResponse cookies:", response.cookies)
print("Response headers:", response.headers)

# Print the client cookies after the request
print("\nClient cookies after request:", client.cookies)

# Manually extract cookies from the response
print("\nManually extracting cookies...")
client.cookies.extract_cookies(response)

# Print the client cookies after manual extraction
print("Client cookies after manual extraction:", client.cookies)

# Create a new CookieJar and extract cookies
print("\nCreating a new CookieJar and extracting cookies...")
jar = CookieJar()
urllib_response = client.cookies._CookieCompatResponse(response)
urllib_request = client.cookies._CookieCompatRequest(response.request)
jar.extract_cookies(urllib_response, urllib_request)

# Print the jar contents
print("New jar contents:")
for cookie in jar:
    print(f"  {cookie.name}={cookie.value} for {cookie.domain}")