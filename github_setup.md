# 🗂 GitHub Repository Setup Guide

## Recommended Folder Structure

When pushing to GitHub, organize your repo exactly like this:

```
SmartProcure-Analytics/
│
├── 📄 README.md                          ← Main project page
│
├── 📁 data/
│   ├── raw/
│   │   ├── fact_purchase_orders.csv
│   │   ├── dim_supplier.csv
│   │   ├── dim_category.csv
│   │   ├── dim_business_unit.csv
│   │   ├── dim_contract.csv
│   │   └── dim_date.csv
│   └── data_quality_report.txt
│
├── 📁 scripts/
│   └── generate_data.py                  ← AI data generation script
│
├── 📁 docs/
│   ├── data_dictionary.md                ← Column definitions
│   ├── m_queries.md                      ← All Power Query M code
│   └── star_schema.png                   ← ERD diagram (screenshot from Excel)
│
├── 📄 SmartProcure_Analytics.xlsm        ← Main dashboard
└── 📄 .gitignore
```

---

## .gitignore

Create a `.gitignore` file with:

```
# Python
__pycache__/
*.pyc
*.pyo
.env
venv/

# Excel temp files
~$*.xlsm
~$*.xlsx

# OS files
.DS_Store
Thumbs.db

# API keys (never commit these)
*.env
config.py
```

---

## Commit Message Convention

Use clear, descriptive commits:

```bash
git init
git add .
git commit -m "Initial commit: AI data generation + ETL pipeline"

git add SmartProcure_Analytics.xlsm
git commit -m "feat: Add dark executive dashboard with 6 charts and AI panel"

git add docs/
git commit -m "docs: Add data dictionary, M queries, and star schema diagram"

git add README.md
git commit -m "docs: Complete README with architecture and insights"
```

---

## How to Get the Star Schema Screenshot

1. Open `SmartProcure_Analytics.xlsm`
2. Go to **Data** tab → **Queries & Connections**
3. Click **Data Model** or open **Power Pivot** → **Diagram View**
4. Screenshot the diagram
5. Save as `docs/star_schema.png`
6. Commit it: `git add docs/star_schema.png && git commit -m "docs: Add star schema ERD"`

---

## LinkedIn Post Template

When you publish this project, use this post structure:

```
🏭 Just published: SmartProcure Analytics

An end-to-end procurement intelligence project built with:
✅ AI-generated data (Python + Claude API)
✅ ETL pipeline with Excel Power Query
✅ Star schema data model (5 dimensions)
✅ Executive dashboard — 6 charts, PivotTables, slicers
✅ AI insights panel (Gemini API)

7.2 billion MAD in procurement data across 80 suppliers,
15 categories, and 4 years — with seasonality, anomaly
detection, and maverick spend analysis built in.

Inspired by my internship experience at OCP Group's
Purchasing Department in Khouribga.

GitHub: [link]

#DataAnalytics #Excel #PowerQuery #Python #AI #Procurement
#SupplyChain #Morocco #Portfolio
```

---

*SmartProcure Analytics — GitHub Setup Guide*
