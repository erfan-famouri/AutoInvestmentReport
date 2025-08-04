import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
###########################################################

def init_driver(headless: bool = True) -> webdriver.Chrome:
    """Initialize and return a configured Chrome WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def fetch_page(driver: webdriver.Chrome, url: str, output_path: str) -> None:
    """Navigate to a URL and save the page HTML to a file."""
    logging.info(f"🌐 Navigating to {url}")
    driver.get(url)
    time.sleep(2)  # Wait for dynamic content
    html = driver.page_source
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    logging.info(f"💾 Saved page HTML to {output_path}")


def parse_html(html_path: str) -> dict:
    """Parse HTML and extract desired data (e.g., coin price)."""
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # TODO: Customize this selector to your actual HTML element
    price_tag = soup.select_one("#coin-price")
    if not price_tag:
        logging.warning("⚠️ Price element not found in HTML")
        return {}

    price = price_tag.get_text(strip=True)
    return {"coin_price": price}


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("get_html.log", encoding="utf-8")
        ]
    )

    url = "https://www.sarafiyaran.com/"
    output_path = "page.html"
    driver = None

    try:
        driver = init_driver(headless=True)
        fetch_page(driver, url, output_path)
        data = parse_html(output_path)
        logging.info(f"✅ Extracted Data: {data}")

    except Exception as e:
        logging.exception("❌ An unexpected error occurred.")
        sys.exit(1)

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
