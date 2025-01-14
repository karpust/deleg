import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import re
from variables import PROXY_SITES


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

