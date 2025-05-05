#!/usr/bin/env python3
"""
bluecross_scraper.py

A template Selenium scraper for BlueCross websites.
Update BASE_URL and the selectors in extract_plan_data() as needed.
"""

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
# 1) Set this to the page you want to scrape:
BASE_URL = "https://www.bluecrossma.org/aboutus/"

# 2) Output CSV file:
OUTPUT_CSV = "bluecross_data.csv"

# 3) ChromeDriver setup (assumes chromedriver is on your PATH):
HEADLESS = False   # set False if you want to see the browser
# ──────────────────────────────────────────────────────────────────────────────

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    # optionally: opts.add_argument("--user-agent=YourAgentString")
    return webdriver.Chrome(options=opts)

def accept_cookies(driver):
    """
    If there's a cookie banner, update this to match its selector.
    """
    try:
        btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[aria-label='Accept Cookies']")))
        btn.click()
        time.sleep(1)
    except Exception:
        pass  # no cookie banner found

def extract_plan_data(driver):
    """
    Example: scrape plan cards. Update selectors to match your target data.
    Returns a list of dicts.
    """
    plans = []
    wait = WebDriverWait(driver, 10)
    # 1) Wait for the container of items
    cards = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".paragraph__column")  # <<— change this!
    ))
    for c in cards:
        try:
            title = c.find_element(By.CSS_SELECTOR, ".paragraph__column").text
        except:
            title = ""
        try:
            link = c.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = ""
        plans.append({
            "title": title,
            # "premium": premium,
            "details_url": link
        })
    return plans

def enrich_with_details(driver, items):
    """
    Follow each item's details_url and scrape more fields.
    """
    wait = WebDriverWait(driver, 10)
    for item in items:
        item["summary"] = None
        if not item["details_url"]:
            continue
        driver.get(item["details_url"])
        # e.g. wait for a summary section
        try:
            summary = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".text-align-center")
            )).text
        except:
            summary = ""
        print(f'summary is {summary}')
        item["summary"] = summary
        # add more fields here...
    return items

def save_csv(items, filename):
    if not items:
        print("No data to save.")
        return
    keys = items[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)
    print(f"Saved {len(items)} records to {filename}")

def main():
    driver = get_driver(HEADLESS)
    try:
        driver.get(BASE_URL)
        accept_cookies(driver)

        # scrape list
        items = extract_plan_data(driver)
        print(items)

        # enrich detail pages
        items = enrich_with_details(driver, items)
        print(f'items after enriching = {items}')

        # save
        save_csv(items, OUTPUT_CSV)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
