#!/usr/bin/env python3

import httpx
from httpx import Proxy

# Create a proxy
proxy = Proxy(url="http://example.com")

# Create an AsyncClient with a proxy
client = httpx.AsyncClient(proxy=proxy)

print("Test completed successfully")