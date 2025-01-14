from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import aiohttp
import asyncio


# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
#
# driver = webdriver.Chrome(options=options)
#
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#     """
# })
# driver.implicitly_wait(5)
# # driver.get("https://github.com/")
# # driver.get("https://free-proxy-list.net/")
# driver.get("https://free-proxy-list.net/#list")
#
# driver.set_page_load_timeout(60)  # Устанавливает таймаут 60 секунд
#
# # Находим все теги <td> внутри <tbody>
# tbody = driver.find_element(By.TAG_NAME, "tbody")
# td_elements = tbody.find_elements(By.TAG_NAME, "td")
#
# # Шаблон для IP-адреса
# ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
# port_pattern = re.compile(r'^\d+$')
#
# # Ищем td с IP-адресом
# proxy_list = []
# n = len(td_elements)
#
# for i in range(0, n-1, 2):
#     ip = td_elements[i].text
#     port = td_elements[i+1].text
#     if ip_pattern.match(ip) and port_pattern.match(port):
#         proxy_list.append(f'{ip}:{port}')
#
# driver.quit()

proxy_list = ['47.251.122.81:8888', '91.92.155.207:3128', '162.214.165.203:80', '203.115.101.51:82', '50.174.7.159:80', '32.223.6.94:80', '82.119.96.254:80', '5.161.103.41:88', '13.37.89.201:80', '13.37.59.99:3128', '13.36.87.105:3128', '13.37.73.214:80', '44.218.183.55:80', '50.202.75.26:80', '50.169.37.50:80', '50.168.72.113:80', '50.232.104.86:80', '50.175.212.66:80', '50.217.226.47:80', '50.239.72.16:80', '50.168.72.118:80', '50.168.72.119:80', '50.217.226.40:80', '50.221.74.130:80', '50.168.72.112:80', '50.175.212.74:80', '201.148.32.162:80', '50.174.7.152:80', '50.122.86.118:80', '37.187.25.85:80', '54.67.125.45:3128', '23.247.136.254:80', '103.152.112.157:80', '200.174.198.86:8888', '3.71.239.218:3128', '35.72.118.126:80', '3.122.84.99:3128', '35.79.120.242:3128', '3.127.62.252:80', '18.228.149.161:80', '3.127.121.101:80', '3.139.242.184:80', '54.233.119.172:3128', '52.196.1.182:80', '18.228.198.164:80', '52.67.10.183:80', '116.125.141.115:80', '41.204.63.118:80', '20.111.54.16:8123', '46.47.197.210:3128', '195.114.209.50:80', '54.152.3.36:80', '39.109.113.97:4090', '3.141.217.225:80', '77.37.41.168:80', '203.77.215.45:10000', '103.237.144.232:1311', '158.255.77.168:80', '54.248.238.110:80', '50.169.222.243:80', '50.168.72.115:80', '50.168.72.116:80', '50.169.222.241:80', '63.35.64.177:3128', '142.44.210.174:80', '192.81.213.42:10007', '159.65.245.255:80', '219.93.101.60:80', '204.236.137.68:80', '158.255.77.166:80', '23.247.137.142:80', '87.248.129.32:80', '43.200.108.126:3128', '51.255.57.241:80', '20.205.61.143:80', '178.128.113.118:23128', '162.223.90.130:80', '50.207.199.86:80', '133.18.234.13:80', '50.217.226.44:80', '0.0.0.0:80', '211.128.96.206:80', '20.24.43.214:80', '68.185.57.66:80', '50.174.7.156:80', '50.207.199.81:80', '123.30.154.171:7777', '20.206.106.192:8123', '127.0.0.7:80', '20.210.113.32:8123', '13.36.104.85:80', '15.236.106.236:3128', '43.157.124.81:8888', '47.252.29.28:11222', '8.219.97.248:80', '45.91.201.100:8081', '13.208.56.180:80', '46.51.249.135:3128', '158.255.77.169:80', '41.74.91.244:80']
# return proxy_list




async def check_proxy(proxy):
    url = "http://httpbin.org/ip"  # Сервис для проверки IP
    proxy_url = f"http://{proxy}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy_url, timeout=5) as response:
                if response.status == 200:
                    print(f"Proxy {proxy} is working.")
                    return proxy
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")
        return None


async def check_proxies(proxies):
    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    return [proxy for proxy in results if proxy]


working_proxies = asyncio.run(check_proxies(proxy_list))
print(f'{len(working_proxies)} of {len(proxy_list)} proxies is available')


