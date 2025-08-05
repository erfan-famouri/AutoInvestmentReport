# AutoInvestmentReport

**AutoInvestmentReport** is a modular Python project designed for real-world usage to automatically track, analyze, and report your financial assets in Iranian Rial, US Dollar, and cash. It retrieves daily gold coin and dollar prices from an online exchange, calculates your total holdings, and generates detailed visual and tabular reports.

---

## 📌 Project Purpose

This project serves as a foundation for a personal finance management system. It helps users:

- Track daily, monthly, and yearly asset values in Rial, Dollar, and cash
- Analyze profits and losses over custom time frames
- Automate data retrieval and report generation

---

## 💼 Use Cases

- Individuals holding both Rial and Dollar assets
- Users seeking automated profit/loss analysis per day, month, and year
- Anyone who wants a hands‑off solution to monitor personal investments

---

## ⚙️ Features

- 🔄 **Daily price retrieval** for Dollar and Gold Coin
- 🧮 **Automatic asset calculation** in Rial, Dollar, and cash
- 📊 **Bar charts** showing asset values and profit/loss per day, month, and year
- 🗄️ **Data snapshots** in `assets_summary.csv`, `portfolio_summary.json`, `prices_history.csv`
- 📄 **PDF report** generation (`final_report.pdf`) with all charts and price history
- 🧩 **Modular architecture** for easy extension (e.g., add cryptocurrencies, rental incomes)
- 🔧 **Interactive prompts** to record manual asset changes on each run

---

## 🧱 Project Structure

```bash
AutoInvestmentReport/
│
├── assets_summary.py                          # Script to summarize current asset values
├── extract_prices.py                          # Fetch dollar and gold coin prices from exchange
├── refactored_get_html.py                     # HTML fetching utilities
├── portfo.py                                  # Portfolio snapshot generator
├── update.py                                  # Main script to update data & prompt user changes
├── update_assets.py                           # Helper for user asset adjustments
├── get_report.py                              # Script to generate or update final_report.pdf
├── generate_pdf_report.py                     # PDF creation module with reportlab
├── Display profit and loss_dollar.ipynb        # Notebook for dollar profit/loss charts
├── Display profit and loss_toman.ipynb         # Notebook for rial profit/loss charts
├── cash.ipynb                                 # Notebook for cash flow charts
├── requirements.txt                           # Python dependencies
├── assets_summary.csv                         # CSV: daily asset values (Rial & Dollar)
├── prices_history.csv                         # CSV: historical price data per day
├── portfolio_summary.json                     # JSON: combined asset snapshot including cash
├── user_assets.json                           # Stored manual asset inputs
├── final_report.pdf                           # Generated PDF report with bar charts
├── executed_notebooks/                        # Latest chart images (dollar.png, toman.png, cash.png)
└── doc/                                       # Sample report and screenshots
    ├── Final_Report_sampel.pdf                # Example PDF output
    └── executed_notebooks_sampel/             # Sample chart images
```

---

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Libraries**:
  - Selenium
  - BeautifulSoup4
  - NumPy
  - ReportLab
  - Standard libraries: `os`, `subprocess`, `shutil`, `sys`, `typing`, `datetime`, `json`, `csv`, `math`, `logging`, `time`

---

## 📥 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/erfan-famouri/AutoInvestmentReport.git
   cd AutoInvestmentReport
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. **Update data**:

   ```bash
   python update.py
   ```

   - Prompts: "Have there been any manual changes to your assets?"
   - Updates `assets_summary.csv`, `portfolio_summary.json`, `prices_history.csv`.

2. **Generate report**:

   ```bash
   python get_report.py
   ```

   - Produces or updates `final_report.pdf` with bar charts for each asset and P/L metrics.
   - Updates images in `executed_notebooks/` (dollar.png, toman.png, cash.png).

> 💡 Tip: Schedule these commands via `cron` (Linux/macOS) or Task Scheduler (Windows) for full automation.

---

## 🎯 Outputs

- **CSV**:
  - `assets_summary.csv`: Daily asset values (Rial & Dollar)
  - `prices_history.csv`: Historical price data per day
- **JSON**:
  - `portfolio_summary.json`: Combined asset snapshot including cash
- **PDF**:
  - `final_report.pdf`: Consolidated report with bar charts and price history
- **Images**:
  - `executed_notebooks/dollar.png`, `toman.png`, `cash.png`

---

## 🔒 Security & Data Privacy

All data is stored locally on the user's machine. No sensitive financial information is transmitted externally.

---

## ⚠️ Limitations

- First run: No profit/loss will be shown due to absence of historical data.
- Dollar price may slightly differ from real market rates.

---

## 🚀 Future Improvements

- Add support for **cryptocurrencies**
- Develop a **GUI** for interactive dashboards
- Integrate with a **database** for scalable storage
- Extend to track **rental incomes** or other asset types

---

## 📝 requirements.txt

```text
selenium
beautifulsoup4
numpy
reportlab
```

*Standard libraries are part of Python and do not require listing.*

---

## 🙋‍♂️ Author

Created with ❤️ by erfan famouri
Based on a modular design for automated personal finance reporting.

