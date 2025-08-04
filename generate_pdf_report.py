import os
import datetime
import json
import csv
from math import ceil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

# Configuration
INPUT_IMAGES_DIR = "executed_notebooks"
REPORT_FILE = "Final_Report.pdf"
TITLE = "Your financial report"
DATE_FORMAT = "%B %d, %Y"  # e.g., July 24, 2025
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg"]
PORTFOLIO_SUMMARY_FILE = "portfolio_summary.json"
USER_ASSETS_FILE = "user_assets.json"
PRICE_HISTORY_FILE = "prices_history.csv"

# Asset name translations (Persian → English)
ASSET_TRANSLATIONS = {
    "دلار آمریکا": "US Dollar",
    "ریال": "Iranian Rial",
    "تمام امامی(86)": "Imami Gold Coin (2007)",
    "تمام بهار آزادی": "Full Bahar Azadi Coin",
    "نیم بهار آزادی": "Half Bahar Azadi Coin",
    "ربع بهار آزادی": "Quarter Bahar Azadi Coin"
}


def determine_grid(n: int):
    """
    Find grid size (rows, cols) for n images minimizing |rows - cols| and area.
    """
    best = None
    for cols in range(1, n + 1):
        rows = ceil(n / cols)
        area = rows * cols
        diff = abs(rows - cols)
        if best is None or (diff, area) < (best[0], best[1]):
            best = (diff, area, rows, cols)
    return best[2], best[3]


def load_user_assets(json_path: str):
    """
    Load user assets (detailed items like gold, dollar, rial) from JSON.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"⚠️ Error loading user assets: {e}")
        return {}


def load_portfolio_summary(json_path: str):
    """
    Load latest total_toman and total_dollar from a list of portfolio summaries.
    Assumes the last item is the most recent.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and data:
                latest = data[-1]
                return latest.get("total_toman", 0), latest.get("total_dollar", 0)
    except Exception as e:
        print(f"⚠️ Error loading portfolio summary: {e}")
    return 0, 0


def load_latest_prices(csv_path: str):
    """
    Read the price history CSV and return a dict of latest buy/sell price per asset.
    """
    latest = {}
    if not os.path.exists(csv_path):
        return latest
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith('نام'):  # skip header if present
                continue
            asset = row[0]
            buy = row[1].replace(',', '').replace('"', '')
            sell = row[2].replace(',', '').replace('"', '')
            date = row[3]
            # overwrite so last occurrence remains
            try:
                buy_val = float(buy)
                sell_val = float(sell)
            except:
                continue
            latest[asset] = (buy_val, sell_val)
    return latest


def create_report(output_path: str, images_by_folder: dict, title: str, date_str: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Load data
    total_toman, total_dollar = load_portfolio_summary(PORTFOLIO_SUMMARY_FILE)
    user_assets = load_user_assets(USER_ASSETS_FILE)
    latest_prices = load_latest_prices(PRICE_HISTORY_FILE)

    # Title Page background
    c.setFillColor(colors.whitesmoke)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # Date
    margin_x = 40
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(margin_x, height - 40, date_str)

    # Professional formatting for totals
    c.setFont("Helvetica", 12)
    y_start = height - 60
    line_gap = 18
    totals = [("Total Assets (Toman)", f"{total_toman:,.0f} Toman"),
              ("Total Assets (Dollar)", f"${total_dollar:,.2f}")]
    for label, value in totals:
        label_w = c.stringWidth(label, "Helvetica", 12)
        value_w = c.stringWidth(value, "Helvetica", 12)
        available = width - 2*margin_x - label_w - value_w
        dot_w = c.stringWidth('.', "Helvetica", 12)
        dots = '.' * max(0, int(available / dot_w))
        line = f"{label} {dots} {value}"
        c.drawString(margin_x, y_start, line)
        y_start -= line_gap

    # Detailed User Assets
    c.setFont("Helvetica", 12)
    c.drawString(margin_x, y_start, "Your Assets:")
    y_start -= line_gap
    c.setFont("Helvetica", 11)
    for asset, amount in user_assets.items():
        asset_en = ASSET_TRANSLATIONS.get(asset, asset)
        value = f"{amount:,}"
        label_w = c.stringWidth(asset_en, "Helvetica", 11)
        value_w = c.stringWidth(value, "Helvetica", 11)
        available = width - 2*margin_x - label_w - value_w
        dot_w = c.stringWidth('.', "Helvetica", 11)
        dots = '.' * max(0, int(available / dot_w))
        line = f"{asset_en} {dots} {value}"
        c.drawString(margin_x, y_start, f"- {line}")
        y_start -= line_gap - 4

    # Latest Prices
    c.setFont("Helvetica", 12)
    c.drawString(margin_x, y_start, "Latest Prices:")
    y_start -= line_gap
    c.setFont("Helvetica", 11)
    for asset, (buy, sell) in latest_prices.items():
        asset_en = ASSET_TRANSLATIONS.get(asset, asset)
        price_str = f"Buy: {buy:,.0f}, Sell: {sell:,.0f}"
        label_w = c.stringWidth(asset_en, "Helvetica", 11)
        value_w = c.stringWidth(price_str, "Helvetica", 11)
        available = width - 2*margin_x - label_w - value_w
        dot_w = c.stringWidth('.', "Helvetica", 11)
        dots = '.' * max(0, int(available / dot_w))
        line = f"{asset_en} {dots} {price_str}"
        c.drawString(margin_x, y_start, f"- {line}")
        y_start -= line_gap - 4

    # Report Title
    c.setFont("Helvetica-Bold", 24)
    text_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - text_width) / 2, height / 2, title)
    c.showPage()

    # Image pages
    margin = 50
    padding = 10
    usable_w = width - 2 * margin
    usable_h = height - 2 * margin - 30

    for folder, img_paths in images_by_folder.items():
        if not img_paths:
            continue
        n = len(img_paths)
        rows, cols = determine_grid(n)
        cell_w = usable_w / cols
        cell_h = usable_h / rows

        # Background
        c.setFillColor(colors.whitesmoke)
        c.rect(0, 0, width, height, fill=True, stroke=False)
        # Folder title
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 18)
        title_str = f"{folder} ({n} images)"
        t_w = c.stringWidth(title_str, "Helvetica-Bold", 18)
        c.drawString((width - t_w) / 2, height - margin + 10, title_str)

        # Images grid
        for idx, img_path in enumerate(img_paths):
            try:
                img = ImageReader(img_path)
                iw, ih = img.getSize()
                aspect = iw / ih
                col = idx % cols
                row = idx // cols
                x0 = margin + col * cell_w
                y0 = height - margin - 30 - (row + 1) * cell_h
                max_w = cell_w - 2 * padding
                max_h = cell_h - 2 * padding
                if (max_w / max_h) > aspect:
                    draw_h = max_h
                    draw_w = draw_h * aspect
                else:
                    draw_w = max_w
                    draw_h = draw_w / aspect
                x = x0 + (cell_w - draw_w) / 2
                y = y0 + (cell_h - draw_h) / 2
                c.drawImage(img, x, y, width=draw_w, height=draw_h)
            except Exception as e:
                print(f"⚠️ Failed to load image {img_path}: {e}")
        c.showPage()

    c.save()


def collect_images_by_folder(base_dir: str) -> dict:
    result = {}
    if os.path.exists(base_dir):
        for folder in sorted(os.listdir(base_dir)):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                imgs = []
                for root, _, files in os.walk(folder_path):
                    for file in sorted(files):
                        if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                            imgs.append(os.path.join(root, file))
                result[folder] = imgs
    return result


if __name__ == "__main__":
    print("🖼️ Generating PDF report ...")
    today = datetime.date.today().strftime(DATE_FORMAT)
    images_by_folder = collect_images_by_folder(INPUT_IMAGES_DIR)
    if not images_by_folder:
        print(f"⚠️ No image folders found in '{INPUT_IMAGES_DIR}'.")
    else:
        create_report(REPORT_FILE, images_by_folder, TITLE, today)
        print(f"✅ PDF report created: {REPORT_FILE}")
