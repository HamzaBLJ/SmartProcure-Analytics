# 📖 Data Dictionary — SmartProcure Analytics

All amounts are in **MAD (Moroccan Dirham)** unless otherwise noted.

---

## fact_purchase_orders

Core transactional table. Each row represents one purchase order line.

| Column | Type | Description | Example |
|---|---|---|---|
| po_id | Text | Unique PO identifier | PO-00001 |
| po_date | Date | Date PO was issued | 2022-03-15 |
| supplier_id | Text | FK → dim_supplier | SUP-001 |
| category_id | Text | FK → dim_category | CAT-03 |
| business_unit_id | Text | FK → dim_business_unit | BU-02 |
| contract_id | Text | FK → dim_contract (nullable) | CON-045 / "No Contract" |
| quantity_ordered | Integer | Units ordered | 150 |
| unit_price | Decimal | Price per unit (MAD) | 4,200.00 |
| total_amount | Decimal | quantity × unit_price (MAD) | 630,000.00 |
| po_cycle_time_days | Integer | Days from PO issue to delivery | 12 |
| actual_delivery_date | Date | Date goods were received | 2022-03-27 |
| requested_delivery_date | Date | Originally requested delivery date | 2022-03-25 |
| is_on_time | Boolean | actual_delivery_date ≤ requested_delivery_date | TRUE |
| delivery_variance_days | Integer | actual - requested (negative = early) | 2 |
| defect_rate_pct | Decimal | % of received units with defects | 3.5 |
| payment_terms_days | Integer | Net payment terms (30 / 60 / 90) | 60 |
| po_status | Text | Completed / Pending / Cancelled | Completed |
| delivery_status* | Text | Derived: Early / On Time / Late 1-7d / Late 7d+ | Late 1-7 days |
| is_anomaly* | Boolean | Derived: TRUE if amount > 95th percentile | FALSE |
| spend_bucket* | Text | Derived: spend range bucket | 500K–1M MAD |

*Calculated columns added during Power Query ETL*

---

## dim_supplier

| Column | Type | Description | Example |
|---|---|---|---|
| supplier_id | Text | Unique supplier identifier | SUP-001 |
| supplier_name | Text | Full company name | BASF Chemical Solutions |
| supplier_tier | Text | Performance tier: A / B / C | A |
| country | Text | Country of registration | Germany |
| city | Text | City of headquarters | Frankfurt |
| category_specialty | Text | Primary spend category served | Chemical Products |
| contract_start_date | Date | Current contract start | 2021-01-01 |
| contract_end_date | Date | Current contract end | 2025-12-31 |
| payment_terms_days | Integer | Standard payment terms | 30 |
| is_strategic | Boolean | Top 20 strategic suppliers | TRUE |
| risk_score | Integer | Risk assessment score (1=low, 10=high) | 3 |
| contract_status* | Text | Derived: Active / Expiring Soon / Expired | Active |
| supplier_label* | Text | Derived: name + tier | BASF Chemical Solutions (A) |

### Supplier Tier Performance Benchmarks

| Tier | On-Time Delivery | Avg Defect Rate | Avg Cycle Time |
|---|---|---|---|
| A | 90.9% | 1.48% | 8.4 days |
| B | 78.5% | 4.39% | 18.8 days |
| C | 60.9% | 9.05% | 30.1 days |

---

## dim_category

| Column | Type | Description | Example |
|---|---|---|---|
| category_id | Text | Unique category identifier | CAT-01 |
| category_name | Text | Category label | Raw Materials |
| category_group | Text | Direct (production-linked) or Indirect | Direct |
| budget_annual | Decimal | Annual budget allocation (MAD) | 500,000,000 |
| criticality_level | Text | High / Medium / Low | High |

### Category List

| Category | Group | Criticality |
|---|---|---|
| Raw Materials | Direct | High |
| Chemical Products | Direct | High |
| Energy | Direct | High |
| Construction | Direct | High |
| Industrial Supplies | Direct | Medium |
| Spare Parts | Direct | Medium |
| Lab Equipment | Direct | Medium |
| Packaging | Direct | Low |
| Logistics | Indirect | High |
| Transportation | Indirect | Medium |
| Maintenance | Indirect | Medium |
| IT Equipment | Indirect | Medium |
| Consulting Services | Indirect | Low |
| Safety Equipment | Indirect | Low |
| Office Supplies | Indirect | Low |

---

## dim_business_unit

| Column | Type | Description | Example |
|---|---|---|---|
| business_unit_id | Text | Unique BU identifier | BU-01 |
| business_unit_name | Text | Business unit name | Mining Operations |
| region | Text | Moroccan region | Khouribga |
| annual_budget | Decimal | Annual procurement budget (MAD) | 800,000,000 |
| budget_owner | Text | Budget responsible name | — |

### Business Units

| Unit | Region |
|---|---|
| Mining Operations | Khouribga |
| Processing Plant | Khouribga |
| Logistics | Casablanca |
| R&D | Benguerir |
| Corporate | Casablanca |
| HSE | Jorf Lasfar |
| Finance | Casablanca |
| IT | Laayoune |

---

## dim_contract

| Column | Type | Description | Example |
|---|---|---|---|
| contract_id | Text | Unique contract identifier | CON-001 |
| contract_name | Text | Contract description | Raw Materials Framework 2022 |
| supplier_id | Text | FK → dim_supplier | SUP-012 |
| category_id | Text | FK → dim_category | CAT-01 |
| contract_type | Text | Framework / Spot / Long-term | Framework |
| start_date | Date | Contract effective date | 2022-01-01 |
| end_date | Date | Contract expiry date | 2024-12-31 |
| contract_value | Decimal | Total contract ceiling (MAD) | 50,000,000 |
| currency | Text | MAD / EUR / USD | MAD |
| is_active | Boolean | Currently active | TRUE |
| auto_renewal | Boolean | Renews automatically | FALSE |
| negotiated_savings_pct | Decimal | % savings vs. market rate | 8.5 |
| days_to_expiry* | Integer | Derived: days until end_date | 245 |
| contract_health* | Text | Derived: Healthy / Expiring Soon / Expired | Healthy |
| contract_duration_months* | Integer | Derived: months between start and end | 36 |

---

## dim_date

| Column | Type | Description | Example |
|---|---|---|---|
| date | Date | Calendar date | 2022-06-15 |
| day | Integer | Day of month (1–31) | 15 |
| month | Integer | Month number (1–12) | 6 |
| month_name | Text | Full month name | June |
| short_month* | Text | Abbreviated month | Jun |
| quarter | Integer | Quarter number (1–4) | 2 |
| year | Integer | Calendar year | 2022 |
| week_number | Integer | ISO week number | 24 |
| is_weekend | Boolean | Saturday or Sunday | FALSE |
| is_month_end | Boolean | Last day of month | FALSE |
| fiscal_quarter | Text | OCP fiscal quarter (starts April) | FQ1 |
| day_of_week_name | Text | Full day name | Wednesday |

---

*Generated: April 2026 | SmartProcure Analytics Project*
