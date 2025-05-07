# Facebook Marketplace Scraper

<h3 align="center">A Python bot that scrapes Facebook Marketplace listings using Playwright, BeautifulSoup, and FastAPI — with a Streamlit GUI frontend.</h3>

> Use this software at your own risk. Automating Facebook interactions may violate their terms of service and could result in account restrictions.
> Using Playwright imitates human behavior, which helps bypass bot detection — but it is still not guaranteed.

---

## Overview

This program scrapes listings from Facebook Marketplace using headless browser automation. You can:

* Choose a city or region
* Enter a product query (e.g., “Sony A7III”)
* Set a maximum price

Scraped data includes:

* Title
* Price
* Location
* Listing URL
* Image preview

You can view results in:

* A **Streamlit GUI**, or
* A **static HTML frontend** (via FastAPI)

---

## 🔧 Requirements

* Python 3.8+
* [Playwright](https://playwright.dev/python/)
* [BeautifulSoup (bs4)](https://pypi.org/project/beautifulsoup4/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Streamlit](https://streamlit.io/)
* [Uvicorn](https://www.uvicorn.org/)

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/facebook-marketplace-scraper.git
cd facebook-marketplace-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file (optional, for OpenAI integration)

Create a `.env` file in the project root:

```bash
touch .env
```

Then add your API key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Generate your own Facebook login session

This only needs to be done once to save your credentials securely:

```bash
python src/save_facebook_login.py
```

A browser window will open. Log in manually. Once logged in, your session will be saved in `facebook_state.json` (which is ignored in version control).

---

## Running the App

### Option 1: Streamlit GUI

```bash
streamlit run src/gui.py
```

### Option 2: FastAPI + Static Frontend

Start the backend server:

```bash
uvicorn src.app:app --reload
```

Then visit in your browser:

* [http://127.0.0.1:8000/frontend](http://127.0.0.1:8000/frontend)
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure

```
marketplace-bot/
├── src/
│   ├── app.py                  # FastAPI backend
│   ├── gui.py                  # Streamlit GUI
│   ├── scraper.py              # Facebook scraper logic
│   ├── tracker.py              # Tracks and exports listings
│   └── save_facebook_login.py  # FB login session initializer
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── .gitignore
├── requirements.txt
├── saved_products.json         # User-defined tracked items (gitignored)
└── marketplace_results.csv     # Output file (gitignored)
```

---

## Notes

* `facebook_state.json` is your personal login session. It is gitignored and only exists locally.
* `saved_products.json` and `marketplace_results.csv` are output files saved by your scraper/tracker.
* You can add OpenAI-powered features later and push updates.

---
