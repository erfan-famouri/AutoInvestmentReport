import json
import os

ASSETS_FILE = 'user_assets.json'

asset_map = {
    "usd": "دلار آمریکا",
    "emami": "تمام امامی(86)",
    "bahar": "تمام بهار آزادی",
    "half": "نیم بهار آزادی",
    "quarter": "ربع بهار آزادی",
    "rial": "ریال"
}

default_assets = {
    "دلار آمریکا": 0,
    "تمام امامی(86)": 0,
    "تمام بهار آزادی": 0,
    "نیم بهار آزادی": 0,
    "ربع بهار آزادی": 0,
    "ریال": 0
}

if not os.path.exists(ASSETS_FILE):
    with open(ASSETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_assets, f, ensure_ascii=False, indent=2)
    print("Created 'user_assets.json' with default values.")

with open(ASSETS_FILE, 'r', encoding='utf-8') as f:
    user_assets = json.load(f)

change = input("Has there been any change in your assets? (yes/no): ").strip().lower()
if change not in ["yes", "y"]:
    print("No changes made.")
    exit()

for eng_key, fa_key in asset_map.items():
    answer = input(f"Has '{eng_key}' ({fa_key}) changed? (yes/no): ").strip().lower()
    if answer in ["yes", "y"]:
        while True:
            new_val = input(f"Enter new integer value for '{eng_key}' ({fa_key}): ").strip()
            if new_val.isdigit():
                user_assets[fa_key] = int(new_val)
                break
            else:
                print("Please enter a valid integer number.")

with open(ASSETS_FILE, 'w', encoding='utf-8') as f:
    json.dump(user_assets, f, ensure_ascii=False, indent=2)

print("Assets updated successfully.")
