import logging


def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        filename='proxy_server.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
