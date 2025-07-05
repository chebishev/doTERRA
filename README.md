# doTERRA Price List Parser

[![Update Prices (Cron)](https://github.com/chebishev/doTERRA/actions/workflows/update_json_file.yml/badge.svg)](https://github.com/chebishev/doTERRA/actions/workflows/update.yml)
![Last Commit](https://img.shields.io/github/last-commit/chebishev/doTERRA)
![Repo Size](https://img.shields.io/github/repo-size/chebishev/doTERRA)
![License](https://img.shields.io/github/license/chebishev/doTERRA)

This Python project downloads the latest **doTERRA Bulgaria price list (PDF)**, extracts structured product information using `pdfplumber`, and saves it as a clean `products.json` file. It runs **weekly** via GitHub Actions to keep the data fresh.

## 🔍 Features

- 📥 Downloads the latest [doTERRA BG Price List](https://media.doterra.com/bg/bg/forms/price-list.pdf)
- 📊 Parses product name, unit, PV, points, retail price, and wholesale price
- 🧼 Cleans product names (e.g., removes `™`, normalizes characters)
- 📦 Detects product **bundles/packs** and adds a `context` field
- 💾 Saves the result to `products.json`
- 🔁 Automatically updates daily with a scheduled GitHub workflow

---

## 📁 Output Format

Each product is saved as a JSON object:

```json
{
  "product": "MetaPWR Mito2Max",
  "unit": "60 Caps",
  "pv": 28.35,
  "points": null,
  "retail": null,
  "wholesale": 36.05,
  "context": "Daily Nutrient Pack"
}

🚀 Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python3 pdf_to_json.py`

📅 GitHub Actions: Daily Sync
This project uses a GitHub Actions workflow that:

Runs every day at 00:00 UTC

Downloads and parses the latest PDF

Commits and pushes changes to products.json if any