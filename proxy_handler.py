import random
import aiohttp
import logging
from aiohttp import web
import variables


async def handle_request(request):
    """Обработка входящих запросов и ретрансляция через рабочий прокси."""
    if not variables.WORKING_PROXIES:
        logging.warning("No proxies available.")
        return web.Response(text="No proxies available", status=503)

    proxy = random.choice(variables.WORKING_PROXIES)
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
