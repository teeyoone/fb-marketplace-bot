
# If you're using openai>=1.0.0
import openai
from openai import OpenAI

client = OpenAI(api_key="REMOVED_API_KEY")

from playwright.sync_api import sync_playwright
import time

# === Generate a buyer message using GPT ===
def generate_message(item_name):
    prompt = f"""
You're a friendly college student looking to buy a used {item_name} on Facebook Marketplace.
This is your first message to the seller. Ask if the item is still available, and casually ask if they’re open to negotiating on the price.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a polite, casual buyer trying to negotiate."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# === Automate Facebook listing visit + message ===
def message_seller(listing_url, item_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="facebook_state.json")
        page = context.new_page()

        print("Opening listing...")
        page.goto(listing_url)

        print("Waiting for message input box...")
        page.wait_for_selector('div[role="textbox"]', timeout=15000)
        message_box = page.query_selector('div[role="textbox"]')

        buyer_reply = generate_message(item_name)
        print("🤖 GPT says:", buyer_reply)

        if message_box:
            print("Sending message...")
            message_box.click()
            time.sleep(0.5)
            page.keyboard.type(buyer_reply, delay=50)  # simulate human typing
            page.keyboard.press("Enter")
            print("✅ Message sent.")
        else:
            print("❌ Could not find the message box.")

        time.sleep(3)
        browser.close()

# === Run the bot ===
if __name__ == "__main__":
    listing_url = "https://www.facebook.com/marketplace/item/554668323987144/"  # Use a real listing URL
    item_name = "Fujifilm X-T5"

    message_seller(listing_url, item_name)
