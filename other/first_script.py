from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# driver.get("https://www.sslproxies.org/")  # -
# driver.get("https://www.us-proxy.org/")  # +
# driver.get("https://www.socks-proxy.net/")  # -
driver.get("https://free-proxy-list.net/")  # +
# driver.get("https://free-proxy-list.net/uk-proxy.html")  # -
# driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()