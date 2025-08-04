import csv
import os
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict

TARGETS = [" دلار آمریکا", "تمام امامی", "تمام بهار", "نیم بهار", "ربع بهار"]
FIELDNAMES = ["subject", "buy_price", "sell_price", "date"]




def extract_prices_from_html(html_content: str) -> List[Dict]:

    """
    Parse HTML and extract prices for defined targets.

    Args:
        html_content (str): Raw HTML content.

    Returns:
        list[dict]: List of extracted price records.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    extracted = []

    for target in TARGETS:
        for table in soup.find_all("table"):
            if target in table.text:
                for row in table.find_all("tr"):
                    if target in row.text:
                        cells = row.find_all("td")
                        if len(cells) >= 3:
                            extracted.append({
                                "subject": cells[0].text.strip().replace(" ", " ").strip(),
                                "buy_price": cells[1].text.strip(),
                                "sell_price": cells[2].text.strip(),
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                        break
    return extracted


def save_prices_to_csv(prices: list[dict], file_path: str = "prices_history.csv") -> None:
    """
    Save extracted prices to a CSV file.

    Args:
        prices (list[dict]): List of price records.
        file_path (str): Path to the CSV file.
    """
    file_exists = os.path.exists(file_path)
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(prices)
    logging.info(f"✅ {len(prices)} records saved to {file_path}")


def main():
    """
    Main pipeline to extract and save prices from page.html.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    html_path = "page.html"

    if not os.path.exists(html_path):
        logging.error(f"HTML file not found: {html_path}")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    prices = extract_prices_from_html(html)
    if not prices:
        logging.warning("No prices extracted from HTML.")
    else:
        save_prices_to_csv(prices)


if __name__ == "__main__":
    main()
