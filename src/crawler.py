from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

options = Options()
options.add_argument(f"--user-data-dir={os.path.abspath('selenium_profile')}")

driver = webdriver.Chrome(options=options)
driver.get("https://www.instagram.com/explore/tags/gaming/")
time.sleep(20)
driver.quit()
