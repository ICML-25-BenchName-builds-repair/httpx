import httpx

async def test_async_client_with_proxy():
    # Create a proxy URL
    proxy = "http://localhost:8080"
    
    # Create an AsyncClient with a proxy
    async with httpx.AsyncClient(proxy=proxy) as client:
        # This should work without errors
        pass

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_async_client_with_proxy())