import json
import pandas as pd
from src.scraper import scrape_facebook_marketplace

# Load saved products from JSON
with open("saved_products.json", "r") as f:
    saved_products = json.load(f)

all_results = []

# Loop through each saved product and scrape results
for product in saved_products:
    product_name = product["product"]
    city = product["city"]
    max_price = product["max_price"]

    print(f"🔍 Scraping listings for: {product_name} in {city} under ${max_price}")
    listings = scrape_facebook_marketplace(city, product_name, max_price)

    for listing in listings:
        listing["product"] = product_name
        listing["city"] = city
        all_results.append(listing)

# Export results to CSV
df = pd.DataFrame(all_results)
df.to_csv("marketplace_results.csv", index=False)
print("✅ Data exported to marketplace_results.csv")
