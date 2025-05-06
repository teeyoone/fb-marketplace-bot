from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import time

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/frontend")
def get_frontend():
    return FileResponse("frontend/index.html")

@app.get("/")
def root():
    return {"message": "Welcome to Passivebot's Facebook Marketplace API."}

@app.get("/crawl_facebook_marketplace")
def crawl_facebook_marketplace(city: str, query: str, max_price: int):
    # Map cities to their Facebook URL slugs
    cities = {
        'Los Angeles': 'la',
        'San Francisco': 'sanfrancisco',
        'New York': 'nyc',
    }

    if city not in cities:
        raise HTTPException(404, f"{city} is not supported. Contact us to add it.")

    city_code = cities[city]
    marketplace_url = f'https://www.facebook.com/marketplace/{city_code}/search/?query={query}&maxPrice={max_price}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="facebook_state.json")
        page = context.new_page()

        page.goto(marketplace_url)
        time.sleep(5)

        for _ in range(10):
            page.keyboard.press('End')
            time.sleep(2)

        soup = BeautifulSoup(page.content(), 'html.parser')
        browser.close()

    parsed = []
    seen_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/marketplace/item/" not in href or href in seen_links:
            continue
        seen_links.add(href)

        spans = a.find_all("span")
        title = next((s.text for s in spans if "$" not in s.text), "N/A")
        price = next((s.text for s in spans if "$" in s.text), "N/A")
        img_tag = a.find("img")
        image = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

        parsed.append({
            "title": title.strip(),
            "price": price.strip(),
            "link": "https://facebook.com" + href,
            "image": image,
            "location": city
        })

    return parsed

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
