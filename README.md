# SmartProcure-Analytics
AI-Powered Procurement Intelligence Dashboard — Python + Excel Power Query + Gemini API
# 🏭 SmartProcure Analytics
### AI-Powered Procurement Intelligence Dashboard

![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power Query](https://img.shields.io/badge/Power_Query-F2C811?style=for-the-badge&logo=microsoft&logoColor=black)
![AI Powered](https://img.shields.io/badge/AI_Powered-Gemini_API-4285F4?style=for-the-badge&logo=google&logoColor=white)

> An end-to-end procurement analytics project combining AI-generated data, Excel Power Query ETL, star schema data modeling, and an AI-powered executive dashboard — inspired by real-world procurement operations in the Moroccan industrial sector.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Dataset Overview](#-dataset-overview)
- [Data Model](#-data-model)
- [ETL Pipeline](#-etl-pipeline)
- [Dashboard Features](#-dashboard-features)
- [AI Integration](#-ai-integration)
- [Key Insights](#-key-insights)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [Author](#-author)

---

## 🎯 Project Overview

SmartProcure Analytics simulates the procurement intelligence needs of a large Moroccan industrial company — tracking **7.2 billion MAD** in purchase orders across 4 years, 80 suppliers, 15 spend categories, and 8 business units.

The project demonstrates a full analytics workflow:

1. **AI Data Generation** — Python script using Claude API to generate statistically coherent, business-realistic mock procurement data with baked-in seasonality, supplier tiers, anomalies, and year-over-year growth
2. **ETL Pipeline** — Power Query (M language) transformations including type casting, calculated columns, anomaly flagging, and maverick spend detection
3. **Star Schema Modeling** — Relational data model connecting one fact table to five dimension tables
4. **Executive Dashboard** — Dark-themed Excel dashboard with 6 charts, 6 PivotTables, interactive slicers, and an AI-powered insights panel

**Business Context:** Inspired by procurement operations at OCP Group (Khouribga), the world's largest phosphate producer, where supplier performance, contract compliance, and spend visibility are mission-critical.

---

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Data Generation | Python 3, Pandas, NumPy, Faker, Claude API |
| ETL & Transformation | Excel Power Query (M Language) |
| Data Modeling | Star Schema (Excel Data Model) |
| Dashboard | Microsoft Excel (.xlsm) |
| AI Insights | Gemini API (via VBA macro) |
| Version Control | Git / GitHub |

---

## 🏗 Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATA GENERATION                       │
│   Python + Claude API → Realistic mock CSVs             │
│   • Business logic: seasonality, tiers, anomalies       │
│   • Statistical coherence: 12% YoY growth locked        │
│   • Data quality report auto-generated                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    ETL PIPELINE                          │
│   Excel Power Query (M Language)                        │
│   • Type casting & column renaming                      │
│   • Calculated columns (delivery_status, spend_bucket)  │
│   • Anomaly flagging (95th percentile threshold)        │
│   • Maverick spend detection (no contract)              │
│   • Cancelled orders separated into own query           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   DATA MODEL                             │
│   Star Schema — 1 Fact + 5 Dimensions                   │
│   fact_purchase_orders ──► dim_supplier                 │
│                        ──► dim_category                 │
│                        ──► dim_date                     │
│                        ──► dim_business_unit            │
│                        ──► dim_contract                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                EXECUTIVE DASHBOARD                       │
│   Excel .xlsm — Dark Executive Theme                    │
│   • 6 Charts (5 Bar + 1 Line)                           │
│   • 6 PivotTables                                       │
│   • Interactive Slicers                                 │
│   • 🤖 AI Strategic Analysis Panel (Gemini API)         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset Overview

All data is AI-generated using a Python script that calls the Claude API to embed realistic business logic.

| Table | Rows | Description |
|---|---|---|
| `fact_purchase_orders` | 5,000 | Core transactional table (2021–2024) |
| `dim_supplier` | 80 | Supplier master data — Moroccan, European, Asian |
| `dim_category` | 15 | Spend categories (Direct & Indirect) |
| `dim_business_unit` | 8 | OCP-style business units across 5 Moroccan regions |
| `dim_contract` | 120 | Framework, Spot, and Long-term contracts |
| `dim_date` | 1,461 | Daily calendar 2021-01-01 → 2024-12-31 |

### Business Logic Embedded in the Data

- **Seasonality** — Higher spend in Q1 and Q3
- **Supplier Tiers** — Three tiers (A/B/C) with stratified performance
- **Anomalies** — 8.4% of orders flagged as unusually high (simulating fraud/errors)
- **Maverick Spend** — 39.7% of orders placed without a contract, concentrated in Consulting, IT, and Logistics
- **YoY Growth** — Exactly +12% compound annual growth rate 2021→2024
- **Moroccan Context** — Regions (Khouribga, Casablanca, Jorf Lasfar, Benguerir, Laayoune), currencies (MAD/EUR/USD), and supplier names reflect real Moroccan industrial geography

### Year-over-Year Spend (Completed Orders)

| Year | Total Spend (MAD) | YoY Growth |
|---|---|---|
| 2021 | 1,507,767,552 | Baseline |
| 2022 | 1,688,699,658 | +12.0% |
| 2023 | 1,891,343,617 | +12.0% |
| 2024 | 2,118,304,851 | +12.0% |
| **Total** | **7,206,115,676** | |

---

## 🔗 Data Model

Star schema with `fact_purchase_orders` at the center:

```
                    dim_date
                       │
                       │ (po_date)
                       │
dim_business_unit ─────┤
                       │
                  fact_purchase_orders
                       │
         dim_supplier ─┤
                       │
         dim_category ─┤
                       │
          dim_contract ─┘
                   (nullable — maverick spend)
```

### Relationships

| From | To | Key | Cardinality |
|---|---|---|---|
| fact_purchase_orders | dim_supplier | supplier_id | Many-to-One |
| fact_purchase_orders | dim_category | category_id | Many-to-One |
| fact_purchase_orders | dim_date | po_date = date | Many-to-One |
| fact_purchase_orders | dim_business_unit | business_unit_id | Many-to-One |
| fact_purchase_orders | dim_contract | contract_id | Many-to-One (nullable) |

---

## ⚙️ ETL Pipeline

Power Query transformations applied to each table:

### fact_purchase_orders
- Promoted headers, detected types
- Cast date columns as `Date` type
- Added `delivery_status` column: Early / On Time / Late 1-7 days / Late 7+ days
- Added `is_anomaly` flag: `true` if `total_amount` > 95th percentile
- Added `spend_bucket`: < 100K / 100K–500K / 500K–1M / > 1M MAD
- Replaced null `contract_id` with `"No Contract"` (maverick spend)
- Separated cancelled orders into standalone `fact_cancelled_orders` query

### dim_supplier
- Added `contract_status`: Active / Expiring Soon (< 90 days) / Expired
- Added `supplier_label`: `supplier_name (tier)`

### dim_contract
- Added `days_to_expiry` calculated column
- Added `contract_health`: Healthy / Expiring Soon / Expired
- Added `contract_duration_months`

### dim_date
- Added `short_month` column (Jan, Feb, Mar...)
- Sorted ascending by date

---

## 📈 Dashboard Features

### Visual Design
- **Theme:** Dark executive (`#0D1B2A` navy + `#C9A84C` gold accents)
- **Charts:** 6 visualizations on a single scrollable dashboard
- **Slicers:** Interactive filters for year, category, supplier tier, business unit
- **Frozen Rows:** Header rows frozen for scrolling stability

### Charts

| # | Title | Type | Insight |
|---|---|---|---|
| 1 | Spend by Category | Bar | Construction & Chemical Products dominate spend |
| 2 | Yearly Spend Trend | Bar | Consistent 12% YoY growth trajectory |
| 3 | Supplier Performance | Bar | Top 10 suppliers by total spend |
| 4 | Delivery Status by Category | Bar | On-time delivery breakdown per category |
| 5 | Spend by Business Unit | Bar | Mining Operations leads internal spend |
| 6 | Monthly Spend Trend | Line | Seasonality pattern — Q1/Q3 peaks visible |

### PivotTables

| PivotTable | Metrics |
|---|---|
| Spend by Category | Total Amount (MAD) |
| Spend by Year | Total Amount with YoY |
| Spend by Supplier | Total Amount per supplier |
| On-Time Delivery by Category | Count of on-time deliveries |
| PO Count by Category | Number of purchase orders |
| Cancelled Orders | Count and value of cancelled POs |

---

## 🤖 AI Integration

### What makes this different from a standard Excel project

This project uses **real AI at two layers**, not just LLM prompting:

**Layer 1 — Data Generation (Claude API)**
The mock dataset was not manually created or downloaded from Kaggle. A Python script calls the Claude API to generate business-realistic data with embedded logic: supplier tier stratification, seasonal spend patterns, correlated defect rates, and statistically calibrated anomalies. The AI understands procurement domain context and generates data that tells a coherent business story.

**Layer 2 — Dashboard Insights (Gemini API)**
The dashboard includes a `🤖 AI Strategic Analysis` panel powered by the Gemini API via VBA macro. On demand, it reads the current PivotTable values and generates a natural language executive summary — identifying top spend drivers, flagging contract compliance risks, and recommending procurement actions.

> **Note:** The AI panel uses Gemini's free tier. If you see a 429 rate limit error, wait 24 hours for quota to regenerate, then click the Update button again.

---

## 💡 Key Insights

Based on the generated dataset, the dashboard surfaces the following findings:

1. **Construction category carries 40.8% of total spend** (2.94B MAD) — highest concentration risk
2. **39.7% maverick spend** — nearly 2,000 POs placed outside contract coverage, concentrated in Consulting and IT
3. **Tier C suppliers average 30.1-day cycle times** vs. 8.4 days for Tier A — significant operational drag
4. **422 anomalous orders** detected (8.4% of POs) — flag for audit and spend control review
5. **Spend grew from 1.5B to 2.1B MAD** between 2021 and 2024 — contract frameworks may need renegotiation to capture volume discounts

---

## 📁 Project Structure

```
SmartProcure-Analytics/
│
├── 📁 data/
│   ├── raw/                          # AI-generated CSV files
│   │   ├── fact_purchase_orders.csv
│   │   ├── dim_supplier.csv
│   │   ├── dim_category.csv
│   │   ├── dim_business_unit.csv
│   │   ├── dim_contract.csv
│   │   └── dim_date.csv
│   └── data_quality_report.txt       # Auto-generated QA report
│
├── 📁 scripts/
│   └── generate_data.py              # AI data generation script
│
├── 📁 docs/
│   ├── data_dictionary.md            # Column definitions for all tables
│   ├── star_schema.png               # Data model diagram
│   └── m_queries/                    # All Power Query M code
│       ├── fact_purchase_orders.m
│       ├── dim_supplier.m
│       ├── dim_category.m
│       ├── dim_business_unit.m
│       ├── dim_contract.m
│       └── dim_date.m
│
├── SmartProcure_Analytics.xlsm       # Main dashboard file
└── README.md
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Microsoft Excel (2016 or later, with Power Query)
- An Anthropic API key (for data generation) or use the pre-generated CSVs in `/data/raw/`

### Step 1 — Generate the Data (optional, CSVs already included)
```bash
pip install pandas numpy faker
python scripts/generate_data.py
```

### Step 2 — Load into Excel
1. Open Excel → `Data` tab → `Get Data` → `From File` → `From Text/CSV`
2. Load each CSV from `/data/raw/` in this order:
   - `dim_date` → `dim_supplier` → `dim_category` → `dim_business_unit` → `dim_contract` → `fact_purchase_orders`
3. For each table: `Home` → `Advanced Editor` → paste the corresponding M code from `/docs/m_queries/`
4. Click `Close & Apply`

### Step 3 — Open the Dashboard
Open `SmartProcure_Analytics.xlsm` and enable macros when prompted (required for AI panel).

### Step 4 — AI Panel
Click the **🤖 Update AI Insights** button on the dashboard. Requires an active Gemini API key set in the VBA macro (Tools → Macros → edit `UpdateAIInsights`).

---

## 👤 Author

**Hamza**
Financial Engineering Student — EMSI Rabat (Bac+5)
Internship: OCP Group — Purchasing Department, Khouribga

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com](https://www.linkedin.com/in/hamza-belhaj-622100237/)](https://www.linkedin.com/in/hamza-belhaj-622100237/ )
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com](https://github.com/HamzaBLJ )

---

*Built with Python, Excel Power Query, and AI — April 2026*
