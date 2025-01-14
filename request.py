import aiohttp
import asyncio


async def test_proxy_request():
    proxy_url = "http://127.0.0.1:8080"  # Локальный прокси-сервер
    target_url = "http://httpbin.org/ip"  # Целевой сайт для тестирования

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_url, proxy=proxy_url, timeout=10) as response:
                print("Response status:", response.status)
                response_data = await response.text()
                print("Response body:", response_data)
        except Exception as e:
            print("Request failed:", e)

if __name__ == "__main__":
    asyncio.run(test_proxy_request())
