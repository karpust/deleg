import asyncio
import logging

from aiohttp import web

from proxy_checker import check_proxies
from proxy_fetcher import fetch_proxies
from proxy_handler import handle_request
from utils import setup_logging
import variables


async def update_proxies_periodically():
    """Фоновая задача для периодического обновления списка рабочих прокси."""
    while True:
        proxies = await fetch_proxies()
        variables.WORKING_PROXIES = await check_proxies(proxies)
        print(f'working_proxies is {len(variables.WORKING_PROXIES)}')
        logging.info("Updated list of working proxies.")
        await asyncio.sleep(600)  # Обновляем каждые 10 минут


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
    setup_logging()
    await asyncio.gather(
        start_proxy_server(),
        update_proxies_periodically()
    )


if __name__ == '__main__':
    asyncio.run(main())

