import asyncio
import aiohttp
import logging


async def check_proxy(proxy):
    """Функция для проверки доступности прокси."""
    test_urls = ["http://httpbin.org/ip", "https://httpbin.org/ip"]
    proxy_url = f"http://{proxy}"
    for url in test_urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy_url, timeout=5) as response:
                    if response.status == 200:
                        logging.info(f"Proxy {proxy} is working.")
                        return proxy
        except Exception:
            continue
    return None


async def check_proxies(proxies):
    """Асинхронная проверка списка прокси."""
    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    working = [proxy for proxy in results if proxy]
    logging.info(f"Checked proxies. {len(working)} working proxies found.")
    return working
