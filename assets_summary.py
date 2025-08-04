from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
def main():
    # خواندن فایل HTML
    with open("page.html", "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    targets = [" دلار آمریکا", "تمام امامی", "تمام بهار", "نیم بهار", "ربع بهار"]
    new_prices = {}

    # استخراج قیمت‌های جدید
    for target_text in targets:
        tables = soup.find_all("table")
        for table in tables:
            if target_text in table.text:
                for row in table.find_all("tr"):
                    if target_text in row.text:
                        cells = row.find_all("td")
                        if len(cells) >= 3:
                            subject = cells[0].text.strip()
                            buy_price = int(cells[1].text.strip().replace(",", ""))
                            new_prices[subject] = buy_price
                            break

    # موجودی تو (قابل تنظیم)
    Dollar_you = 0
    Emami_you = 1
    Azadi_you = 0
    nim_Azadi_you = 1
    rob_Azadi_you = 1

    # استخراج قیمت‌ها از دیکشنری
    Dollar = new_prices.get("دلار آمریکا", 0)
    Emami = new_prices.get("تمام امامی(86)", new_prices.get("تمام امامی", 0))
    Azadi = new_prices.get("تمام بهار آزادی", 0)
    nim_Azadi = new_prices.get("نیم بهار آزادی", 0)
    rob_Azadi = new_prices.get("ربع بهار آزادی", 0)

    # محاسبه دارایی
    assets_rial = (
        (Dollar_you * Dollar) +
        (Emami_you * Emami) +
        (Azadi_you * Azadi) +
        (nim_Azadi_you * nim_Azadi) +
        (rob_Azadi_you * rob_Azadi)
    )
    assets_dollar = round(assets_rial / (Dollar + 10000), 2) if Dollar != 0 else 0

    # ذخیره در فایل
    summary_row = {
        "assets_rial": assets_rial,
        "assets_dollar": assets_dollar,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    file_exists = os.path.exists("assets_summary.csv")

    with open("assets_summary.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["assets_rial", "assets_dollar", "date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(summary_row)

    print("✅ Asset information was saved successfully.")
if __name__ == "__main__":
    main()
