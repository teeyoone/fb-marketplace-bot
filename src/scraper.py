from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv
import re  # <-- Add this line
import logging
from datetime import datetime


def scrape_facebook_marketplace(city, query, max_price, export_csv=False):
    # Logging setup
    logging.basicConfig(level=logging.INFO)
    
    cities = {
        'Los Angeles': 'la',
        'San Diego': 'sandiego',
        'San Jose': 'sanjose',
        'San Francisco': 'sanfrancisco',
        'Sacramento': 'sac'
    }

    if city not in cities:
        raise ValueError(f"City '{city}' not supported. Please choose from: {', '.join(cities.keys())}")
    
    city_code = cities[city]
    marketplace_url = f"https://www.facebook.com/marketplace/{city_code}/search/?query={query}&maxPrice={max_price}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state="facebook_state.json")
            page = context.new_page()

            logging.info(f"Navigating to: {marketplace_url}")
            page.goto(marketplace_url)
            time.sleep(10)

            for _ in range(5):
                page.keyboard.press("End")
                time.sleep(3)

            soup = BeautifulSoup(page.content(), "html.parser")
            context.close()
            browser.close()

    except Exception as e:
        logging.error("Error launching browser or loading page: %s", str(e))
        return []

    listings = soup.find_all("a", href=True)
    seen_links = set()
    results = []

    for a in listings:
        href = a["href"]
        if "/marketplace/item/" not in href or href in seen_links:
            continue
        seen_links.add(href)

        spans = a.find_all("span")
        price_texts = [s.text for s in spans if "$" in s.text]
        title_texts = [s.text for s in spans if "$" not in s.text]

        prices = re.findall(r"\$\d+(?:,\d+)?", ''.join(price_texts))
        price = prices[0] if prices else "N/A"
        title = title_texts[0] if title_texts else a.get("aria-label", "N/A")

        # ✅ Skip personal FBM reminders
        if "Let people know if you've sold your item" in title:
            continue

        # ✅ Fix malformed double facebook.com links
        cleaned_href = href.replace("https://facebook.comhttps://www.facebook.com", "https://www.facebook.com")
        full_link = cleaned_href if cleaned_href.startswith("http") else "https://facebook.com" + cleaned_href

        img_tag = a.find("img")
        image_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"

        results.append({
            "title": title.strip(),
            "price": price.strip(),
            "link": full_link,
            "product": query,
            "city": city,
            "image": image_url,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    if export_csv and results:
        filename = f"{query.replace(' ', '_')}_{city.replace(' ', '_')}_results.csv"
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        logging.info(f"Exported {len(results)} listings to {filename}")

    return results
