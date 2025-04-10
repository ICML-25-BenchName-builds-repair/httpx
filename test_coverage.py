import httpx

# Test SSLContext.__repr__
def test_ssl_context_repr():
    context = httpx.SSLContext()
    repr_str = repr(context)
    assert repr_str == f"<SSLContext [verify={context.verify}]>"
    
    context_no_verify = httpx.SSLContext(verify=False)
    repr_str_no_verify = repr(context_no_verify)
    assert repr_str_no_verify == f"<SSLContext [verify={context_no_verify.verify}]>"

# Test Proxy.raw_auth
def test_proxy_raw_auth():
    proxy = httpx.Proxy("https://username:password@example.com")
    raw_auth = proxy.raw_auth
    assert raw_auth == (b"username", b"password")
    
    proxy_no_auth = httpx.Proxy("https://example.com")
    raw_auth_none = proxy_no_auth.raw_auth
    assert raw_auth_none is None

if __name__ == "__main__":
    test_ssl_context_repr()
    test_proxy_raw_auth()
    print("All tests passed!")