from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

profile_path = os.path.abspath("selenium_profile")

options = Options()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)
driver.get("https://www.instagram.com/")

print("⏳ لطفاً لاگین کن، بعد از لاگین ENTER بزن...")
input()

driver.quit()
print("✅ لاگین ذخیره شد")
