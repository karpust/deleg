import asyncio
import re

import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import random
import logging

# Настройка логирования
logging.basicConfig(
    filename='../proxy_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Список рабочих прокси (обновляется периодически)
working_proxies = []

# Сайты с публичными прокси
PROXY_SITES = [
    "https://free-proxy-list.net/",
    "https://www.us-proxy.org/",
    "https://www.socks-proxy.net/",
    "https://www.sslproxies.org/",
    "https://free-proxy-list.net/uk-proxy.html",
]


async def fetch_proxies_from_site(url):
    """Функция для парсинга прокси с одного сайта."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Шаблон для IP-адреса
                ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
                port_pattern = re.compile(r'^\d+$')

                tbody = soup.find('tbody')
                ips = tbody.find_all('td', string=ip_pattern)
                ports = tbody.find_all('td', string=port_pattern)

                proxy_list = []
                for i, ip in enumerate(ips):
                    proxy_list.append(f'{ip.text}:{ports[i].text}')

                print(len(proxy_list))
                return proxy_list
    except Exception as e:
        logging.error(f"Error fetching proxies from {url}: {e}")
        return []


async def fetch_proxies():
    """Функция для сбора прокси с нескольких сайтов."""
    tasks = [fetch_proxies_from_site(url) for url in PROXY_SITES]
    results = await asyncio.gather(*tasks)
    proxies = set(proxy for sublist in results for proxy in sublist)
    logging.info(f"Fetched {len(proxies)} proxies.")
    print(f'all proxies is {len(proxies)}')
    return list(proxies)


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


async def update_proxies_periodically():
    """Фоновая задача для периодического обновления списка рабочих прокси."""
    global working_proxies
    while True:
        proxies = await fetch_proxies()
        working_proxies = await check_proxies(proxies)
        print(f'working_proxies is {len(working_proxies)}')
        logging.info("Updated list of working proxies.")
        await asyncio.sleep(600)  # Обновляем каждые 10 минут


async def handle_request(request):
    """Обработка входящих запросов и ретрансляция через рабочий прокси."""
    global working_proxies
    if not working_proxies:
        logging.warning("No proxies available.")
        return web.Response(text="No proxies available", status=503)

    proxy = random.choice(working_proxies)
    proxy_url = f"http://{proxy}"
    logging.info(f"Forwarding request through proxy: {proxy}")

    # target_url = str(request.rel_url)  # Извлечение пути и параметров
    target_url = f"{request.scheme}://{request.host}{request.rel_url}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=request.headers,
                data=await request.read(),
                proxy=proxy_url,
                timeout=10
            ) as resp:
                response_data = await resp.read()
                return web.Response(body=response_data, status=resp.status, headers=resp.headers)
        except Exception as e:
            logging.error(f"Error forwarding request: {e}")
            return web.Response(text=f"Proxy error: {e}", status=502)



async def start_proxy_server():
    """Запуск HTTP и HTTPS прокси сервера."""
    app = web.Application()
    app.router.add_route('*', '/{path:.*}', handle_request)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=8080)
    await site.start()
    logging.info("Proxy server is running on http://0.0.0.0:8080")


async def main():
    """Основная функция для запуска прокси-сервера и фонового обновления прокси."""
    await asyncio.gather(
        start_proxy_server(),
        update_proxies_periodically()
    )


if __name__ == '__main__':
    asyncio.run(main())
