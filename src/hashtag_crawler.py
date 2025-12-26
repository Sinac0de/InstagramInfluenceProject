from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import csv
import random

HASHTAGS = [
    "gaming",
    "esports",
    "gamer",
    "gamingcommunity",
    "valorant",
    "leagueoflegends"
]

POSTS_PER_HASHTAG = 60
SCROLL_PAUSE = 3


def setup_driver():
    options = Options()
    options.add_argument(
        f"--user-data-dir={os.path.abspath('selenium_profile')}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=options)


def crawl_hashtag(driver, hashtag, max_posts):
    print(f"\n🔍 Crawling #{hashtag}")
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    driver.get(url)
    time.sleep(5)

    post_links = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(post_links) < max_posts:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "/p/" in href:
                post_links.add(href)

        print(f"Collected {len(post_links)} posts so far...")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE + random.uniform(1, 3))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(post_links)[:max_posts]


def main():
    os.makedirs("data/raw", exist_ok=True)

    driver = setup_driver()
    all_posts = []

    for tag in HASHTAGS:
        posts = crawl_hashtag(driver, tag, POSTS_PER_HASHTAG)
        for p in posts:
            all_posts.append({"hashtag": tag, "post_url": p})
        time.sleep(10 + random.uniform(5, 10))

    driver.quit()

    output_file = "data/raw/post_links.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["hashtag", "post_url"])
        writer.writeheader()
        writer.writerows(all_posts)

    print(f"\n✅ Done! Saved {len(all_posts)} post links to {output_file}")


if __name__ == "__main__":
    main()
