import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def scrape_indeed_stealth(pages=5, delay=3.0):
    # 1) Stealthy ChromeOptions (no experimental_option calls)
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # 2) Launch undetected-chromedriver (it auto-manages the driver binary)
    driver = uc.Chrome(options=options)

    results = []
    base_url = "https://www.indeed.com/jobs?q=data+scientist&l=Boston%2C+MA"

    for page in range(pages):
        url = f"{base_url}&start={page * 10}"
        print(f"[Page {page+1}] Loading {url}")
        driver.get(url)
        time.sleep(delay)

        # bail if we still hit a verification page
        if "verify" in driver.current_url:
            print("⚠️ Hit a verification page; stopping early.")
            break

        # print(f'driver = {driver}')
        # scrape job cards
        cards = driver.find_elements(By.CSS_SELECTOR, "#mosaic-provider-jobcards div.job_seen_beacon")
        # print(f'cards = {cards}')
        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle > a > span").text.strip()
                results.append({"title": title})
            except Exception as e:
                print(e)
                print('continue')
                continue

    driver.quit()
    return results

if __name__ == "__main__":
    jobs = scrape_indeed_stealth(pages=5, delay=3.0)
    print(f"Scraped {len(jobs)} listings.")

    # write out CSV
    with open("indeed_data_scientist_boston.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company"])
        writer.writeheader()
        writer.writerows(jobs)

    print("Done. Results saved to indeed_data_scientist_boston.csv")

    #TODO: add the JD, the salary more information if possible.