"""
SmartProcure Analytics -- Mock Procurement Dataset Generator
Generates realistic procurement data for a Power BI portfolio project.
"""

import os
import random
from datetime import date, timedelta, datetime

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. DIM_CATEGORY  (15 rows)
# ---------------------------------------------------------------------------
dim_category = pd.DataFrame([
    ("CAT-01", "Raw Materials",       "Direct",   45_000_000, "High"),
    ("CAT-02", "Logistics",           "Indirect",  18_000_000, "High"),
    ("CAT-03", "IT Equipment",        "Indirect",  12_000_000, "Medium"),
    ("CAT-04", "Industrial Supplies", "Direct",    30_000_000, "High"),
    ("CAT-05", "Safety Equipment",    "Indirect",   8_000_000, "High"),
    ("CAT-06", "Energy",              "Direct",    35_000_000, "High"),
    ("CAT-07", "Consulting Services", "Indirect",  15_000_000, "Medium"),
    ("CAT-08", "Lab Equipment",       "Direct",    10_000_000, "Medium"),
    ("CAT-09", "Packaging",           "Direct",    20_000_000, "Medium"),
    ("CAT-10", "Maintenance",         "Indirect",  25_000_000, "High"),
    ("CAT-11", "Office Supplies",     "Indirect",   4_000_000, "Low"),
    ("CAT-12", "Transportation",      "Indirect",  22_000_000, "Medium"),
    ("CAT-13", "Construction",        "Direct",    50_000_000, "High"),
    ("CAT-14", "Chemical Products",   "Direct",    40_000_000, "High"),
    ("CAT-15", "Spare Parts",         "Direct",    28_000_000, "Medium"),
], columns=["category_id", "category_name", "category_group",
            "budget_annual", "criticality_level"])

CAT_IDS    = dim_category["category_id"].tolist()
CAT_NAMES  = dim_category["category_name"].tolist()
CAT_BUDGET = dim_category["budget_annual"].values.astype(float)
CAT_W      = CAT_BUDGET / CAT_BUDGET.sum()   # category sampling weights

# ---------------------------------------------------------------------------
# 2. DIM_BUSINESS_UNIT  (8 rows)
# ---------------------------------------------------------------------------
dim_business_unit = pd.DataFrame([
    ("BU-01", "Mining Operations", "Khouribga",   120_000_000, "Ahmed Benali"),
    ("BU-02", "Processing Plant",  "Jorf Lasfar",  95_000_000, "Mohammed Ezzine"),
    ("BU-03", "Logistics",         "Casablanca",   45_000_000, "Fatima Chraibi"),
    ("BU-04", "R&D",               "Benguerir",    30_000_000, "Youssef Alami"),
    ("BU-05", "Corporate",         "Casablanca",   25_000_000, "Nadia Fassi"),
    ("BU-06", "HSE",               "Khouribga",    20_000_000, "Rachid Ouali"),
    ("BU-07", "Finance",           "Casablanca",   15_000_000, "Laila Bennani"),
    ("BU-08", "IT",                "Casablanca",   18_000_000, "Karim Tahiri"),
], columns=["business_unit_id", "business_unit_name", "region",
            "annual_budget", "budget_owner"])

BU_IDS = dim_business_unit["business_unit_id"].tolist()

# ---------------------------------------------------------------------------
# 3. DIM_SUPPLIER  (80 rows)
# ---------------------------------------------------------------------------
MOROCCAN_SUPPLIERS = [
    "Maghreb Industrial Solutions", "Atlas Mining Supplies",
    "Casablanca Tech Partners", "Maroc Chimie Industries",
    "Rif Industrial Group", "Souss-Massa Equipment",
    "Tensift Logistics SA", "Draa-Tafilalet Resources",
    "Beni Mellal Supplies", "Khouribga Industrial Co.",
    "Laayoune Mining Services", "Dakhla Resources Ltd",
    "Agadir Trade Solutions", "Fes-Meknes Industries",
    "Oriental Mining Group", "Marrakech Logistics SA",
    "Rabat Industrial Partners", "Tanger Med Supplies",
    "Oujda Industrial Services", "Safi Chemical Industries",
    "Nador Steel & Metal", "Kenitra Packaging Co.",
    "Settat Agro Industries", "Khemisset Resources",
    "Berrechid Industrial Park", "Benslimane Equipment",
    "El Jadida Maritime Supplies", "Essaouira Trading Co.",
    "Tiznit Mining Services", "Taroudant Industrial Ltd",
]

EUROPEAN_SUPPLIERS = [
    "Schneider Industrial SAS", "Siemens Procurement GmbH",
    "Veolia Environmental Services", "Air Liquide Industrial",
    "TotalEnergies Supply Chain", "Lafarge Holcim Materials",
    "Thales Group Systems", "Bureau Veritas Inspection",
    "SGS Quality Services", "Alstom Rail & Transport",
    "Saint-Gobain Construction", "Vallourec Tubes SA",
    "Eiffage Construction", "Vinci Industrial Services",
    "Legrand Electrical", "SKF Bearings & Parts",
    "ABB Automation Systems", "BASF Chemical Solutions",
    "Henkel Industrial Adhesives", "Linde Gas Solutions",
    "Bayer MaterialScience", "Evonik Specialty Chemicals",
    "Arkema Chemical Group", "Solvay Advanced Materials",
    "Nyrstar Metal Processing", "Trelleborg Industrial",
    "Sandvik Mining Tools", "Metso Outotec GmbH",
]

ASIAN_SUPPLIERS = [
    "Sinopec Trading Co.", "CITIC Industrial Group",
    "China Molybdenum Ltd", "Minmetals Resources",
    "CNMC Mining Equipment", "Shandong Heavy Industry",
    "Zhejiang Industrial Parts", "Jiangsu Packaging Corp",
    "Shanghai Tech Solutions", "Guangzhou Chemical Corp",
    "Wuhan Steel & Materials", "Chengdu Equipment Co.",
    "Mitsubishi Industrial", "Sumitomo Heavy Industries",
    "Mitsui Mining Corp", "Komatsu Equipment Asia",
    "Hitachi Industrial Systems", "Yokogawa Instruments",
    "Samsung Engineering MENA", "Hyundai Heavy Industries",
    "POSCO Steel & Metal", "Gulf Mining International",
]

# 30 + 28 + 22 = 80
ALL_SUPPLIER_NAMES = MOROCCAN_SUPPLIERS + EUROPEAN_SUPPLIERS + ASIAN_SUPPLIERS

COUNTRY_CITIES = {
    "Morocco": ["Casablanca", "Rabat", "Khouribga", "Jorf Lasfar",
                "Agadir", "Fes", "Marrakech", "Tanger", "Safi"],
    "France":  ["Paris", "Lyon", "Marseille", "Bordeaux", "Toulouse"],
    "Spain":   ["Madrid", "Barcelona", "Bilbao", "Valencia", "Seville"],
    "China":   ["Shanghai", "Beijing", "Guangzhou", "Shenzhen", "Wuhan"],
    "Germany": ["Munich", "Hamburg", "Frankfurt", "Berlin", "Cologne"],
    "USA":     ["Houston", "New York", "Chicago", "Los Angeles", "Dallas"],
}


def _supplier_country(name: str) -> str:
    if name in MOROCCAN_SUPPLIERS:
        return "Morocco"
    if name in EUROPEAN_SUPPLIERS:
        return random.choice(["France", "Spain", "Germany"])
    return random.choice(["China", "Germany", "USA"])


supplier_rows = []
for idx, name in enumerate(ALL_SUPPLIER_NAMES):
    sid     = f"SUP-{idx + 1:03d}"
    country = _supplier_country(name)
    city    = random.choice(COUNTRY_CITIES[country])
    tier    = random.choices(["A", "B", "C"], weights=[25, 45, 30])[0]
    cat_idx = random.randint(0, 14)

    c_start = date(random.randint(2018, 2021), random.randint(1, 12), 1)
    c_end   = c_start + timedelta(days=random.choice([365, 730, 1095]))

    risk_score = (
        random.randint(1, 4) if tier == "A"
        else random.randint(3, 7) if tier == "B"
        else random.randint(5, 10)
    )

    supplier_rows.append({
        "supplier_id":         sid,
        "supplier_name":       name,
        "supplier_tier":       tier,
        "country":             country,
        "city":                city,
        "category_specialty":  CAT_NAMES[cat_idx],
        "contract_start_date": c_start,
        "contract_end_date":   c_end,
        "payment_terms_days":  random.choice([30, 60, 90]),
        "is_strategic":        int(idx < 20),
        "risk_score":          risk_score,
    })

dim_supplier = pd.DataFrame(supplier_rows)
SUP_IDS   = dim_supplier["supplier_id"].tolist()
SUP_TIERS = dim_supplier.set_index("supplier_id")["supplier_tier"].to_dict()
SUP_TERMS = dim_supplier.set_index("supplier_id")["payment_terms_days"].to_dict()

# ---------------------------------------------------------------------------
# 4. DIM_CONTRACT  (120 rows)
# ---------------------------------------------------------------------------
CONTRACT_TYPES = ["Framework", "Spot", "Long-term"]
CURRENCIES     = ["MAD", "EUR", "USD"]
CURRENCY_W     = [0.60, 0.25, 0.15]

contract_rows = []
for i in range(120):
    cid     = f"CON-{i + 1:04d}"
    sup_row = dim_supplier.iloc[random.randint(0, len(dim_supplier) - 1)]
    cat_idx = random.randint(0, 14)
    ctype   = random.choice(CONTRACT_TYPES)

    c_start  = date(random.randint(2019, 2023), random.randint(1, 12), 1)
    duration = {"Framework": random.choice([365, 730]),
                "Long-term": random.choice([730, 1095, 1460]),
                "Spot":      random.choice([90, 180, 365])}[ctype]
    c_end = c_start + timedelta(days=duration)

    contract_rows.append({
        "contract_id":            f"CON-{i + 1:04d}",
        "contract_name":          f"{sup_row['supplier_name']} - {CAT_NAMES[cat_idx]}",
        "supplier_id":            sup_row["supplier_id"],
        "category_id":            CAT_IDS[cat_idx],
        "contract_type":          ctype,
        "start_date":             c_start,
        "end_date":               c_end,
        "contract_value":         random.randint(500_000, 50_000_000),
        "currency":               random.choices(CURRENCIES, weights=CURRENCY_W)[0],
        "is_active":              int(c_end >= date(2024, 1, 1)),
        "auto_renewal":           random.choice([0, 1]),
        "negotiated_savings_pct": round(random.uniform(1.0, 15.0), 2),
    })

dim_contract = pd.DataFrame(contract_rows)

# Pre-build contract lookup: category_id -> [(contract_id, start, end), ...]
cat_contract_lookup: dict = {cid: [] for cid in CAT_IDS}
for _, row in dim_contract.iterrows():
    cat_contract_lookup[row["category_id"]].append(
        (row["contract_id"], row["start_date"], row["end_date"])
    )

# ---------------------------------------------------------------------------
# 5. DIM_DATE  (2021-01-01 to 2024-12-31)
# ---------------------------------------------------------------------------
def _fiscal_quarter(month: int) -> str:
    """OCP fiscal year starts April 1."""
    if month in (4, 5, 6):    return "FQ1"
    if month in (7, 8, 9):    return "FQ2"
    if month in (10, 11, 12): return "FQ3"
    return "FQ4"              # Jan, Feb, Mar


date_rows = []
cur = date(2021, 1, 1)
end = date(2024, 12, 31)
while cur <= end:
    m   = cur.month
    nxt = cur + timedelta(days=1)
    date_rows.append({
        "date":             cur,
        "day":              cur.day,
        "month":            m,
        "month_name":       cur.strftime("%B"),
        "quarter":          (m - 1) // 3 + 1,
        "year":             cur.year,
        "week_number":      cur.isocalendar()[1],
        "is_weekend":       int(cur.weekday() >= 5),
        "is_month_end":     int(nxt.month != m),
        "fiscal_quarter":   _fiscal_quarter(m),
        "day_of_week_name": cur.strftime("%A"),
    })
    cur = nxt

dim_date = pd.DataFrame(date_rows)

# ---------------------------------------------------------------------------
# 6. FACT_PURCHASE_ORDERS  (~5000 rows, 2021-2024)
# ---------------------------------------------------------------------------
N_TOTAL     = 5000
YEAR_COUNTS = {2021: 1100, 2022: 1200, 2023: 1300, 2024: 1400}
GROWTH_RATE = 0.12

# Seasonal weights per month (Q1 Jan-Mar and Q3 Jul-Sep are peaks)
MONTHLY_W = np.array([1.3, 1.2, 1.1, 0.9, 0.8, 0.7,
                       1.3, 1.2, 1.1, 0.9, 0.8, 0.7])
MONTHLY_W = MONTHLY_W / MONTHLY_W.sum()

# Base spend ranges per category (MAD)
CAT_SPEND = {
    "CAT-01": (50_000,  2_000_000),
    "CAT-02": (20_000,    500_000),
    "CAT-03": (10_000,    300_000),
    "CAT-04": (30_000,    800_000),
    "CAT-05":  (5_000,    150_000),
    "CAT-06": (100_000, 3_000_000),
    "CAT-07": (15_000,    400_000),
    "CAT-08": (20_000,    600_000),
    "CAT-09": (10_000,    250_000),
    "CAT-10": (15_000,    450_000),
    "CAT-11":  (1_000,     50_000),
    "CAT-12": (10_000,    300_000),
    "CAT-13": (200_000, 5_000_000),
    "CAT-14": (50_000,  1_500_000),
    "CAT-15":  (5_000,    200_000),
}

# Categories with elevated maverick (no-contract) spend
MAVERICK_CATS = {"CAT-07", "CAT-11", "CAT-03", "CAT-12", "CAT-02"}

# Tier delivery / quality parameters
TIER_PARAMS = {
    "A": dict(cycle_lo=2,  cycle_hi=15,  on_time_p=0.92, defect_lo=0.0, defect_hi=3.0),
    "B": dict(cycle_lo=7,  cycle_hi=30,  on_time_p=0.78, defect_lo=1.0, defect_hi=8.0),
    "C": dict(cycle_lo=15, cycle_hi=45,  on_time_p=0.60, defect_lo=3.0, defect_hi=15.0),
}

# ── Row generation ──────────────────────────────────────────────────────────
po_rows = []

for year, n in YEAR_COUNTS.items():
    for _ in range(n):
        # Date (seasonally weighted)
        month   = int(np.random.choice(np.arange(1, 13), p=MONTHLY_W))
        day     = random.randint(1, 28)
        po_date = date(year, month, day)

        # Supplier
        supplier_id = random.choice(SUP_IDS)
        tier        = SUP_TIERS[supplier_id]
        tp          = TIER_PARAMS[tier]

        # Category — weighted by budget so high-spend categories dominate
        cat_id = str(np.random.choice(CAT_IDS, p=CAT_W))

        # Business unit
        bu_id = random.choice(BU_IDS)

        # Contract (maverick logic)
        maverick_rate = 0.50 if cat_id in MAVERICK_CATS else 0.30
        if random.random() > maverick_rate:
            valid = [
                c_id for c_id, c_s, c_e in cat_contract_lookup.get(cat_id, [])
                if c_s <= po_date <= c_e
            ]
            contract_id = random.choice(valid) if valid else None
        else:
            contract_id = None

        # Base amount (no YoY multiplier yet — applied in normalization step)
        lo, hi       = CAT_SPEND[cat_id]
        base_amount  = random.uniform(lo, hi)

        # Anomaly flag: 8 % of orders (unusually high — fraud / error)
        is_anomaly = random.random() < 0.08
        if is_anomaly:
            base_amount *= random.uniform(5.0, 15.0)

        total_amount = round(base_amount, 2)
        quantity     = random.randint(1, 500)
        unit_price   = round(total_amount / quantity, 2)

        # Delivery
        cycle_time = random.randint(tp["cycle_lo"], tp["cycle_hi"])
        req_del    = po_date + timedelta(days=cycle_time)
        is_on_time = random.random() < tp["on_time_p"]
        variance   = random.randint(-3, 0) if is_on_time else random.randint(1, 20)
        act_del    = req_del + timedelta(days=variance)

        # Defect rate
        defect_rate = round(random.uniform(tp["defect_lo"], tp["defect_hi"]), 2)

        # PO status
        r_status  = random.random()
        po_status = "Cancelled" if r_status < 0.05 else ("Pending" if r_status < 0.15 else "Completed")

        po_rows.append({
            "po_id":                   f"PO-{len(po_rows) + 1:05d}",
            "po_date":                 po_date,
            "supplier_id":             supplier_id,
            "category_id":             cat_id,
            "business_unit_id":        bu_id,
            "contract_id":             contract_id,
            "quantity_ordered":        quantity,
            "unit_price":              unit_price,
            "total_amount":            total_amount,
            "po_cycle_time_days":      cycle_time,
            "actual_delivery_date":    act_del,
            "requested_delivery_date": req_del,
            "is_on_time":              int(is_on_time),
            "delivery_variance_days":  variance,
            "defect_rate_pct":         defect_rate,
            "payment_terms_days":      SUP_TERMS[supplier_id],
            "po_status":               po_status,
            "_is_anomaly":             int(is_anomaly),   # temp column, dropped before save
        })

fact_po = pd.DataFrame(po_rows)

# ── Post-normalization: enforce ~12 % YoY growth ────────────────────────────
# Scale ALL non-cancelled orders proportionally so every year hits the target.
# Anomaly orders are scaled the same way — they stay proportionally larger.
fact_po["_year"] = pd.to_datetime(fact_po["po_date"]).dt.year
active_mask = fact_po["po_status"] != "Cancelled"

base_spend = fact_po.loc[active_mask & (fact_po["_year"] == 2021), "total_amount"].sum()

for yr in [2022, 2023, 2024]:
    target   = base_spend * ((1 + GROWTH_RATE) ** (yr - 2021))
    mask_yr  = active_mask & (fact_po["_year"] == yr)
    actual   = fact_po.loc[mask_yr, "total_amount"].sum()
    if actual > 0:
        scale = target / actual
        fact_po.loc[mask_yr, "total_amount"] = (fact_po.loc[mask_yr, "total_amount"] * scale).round(2)
        fact_po.loc[mask_yr, "unit_price"]   = (
            fact_po.loc[mask_yr, "total_amount"] / fact_po.loc[mask_yr, "quantity_ordered"]
        ).round(2)

# Capture anomaly count before dropping temp columns
anomaly_count    = int(fact_po["_is_anomaly"].sum())
maverick_count   = int(fact_po["contract_id"].isna().sum())
cancelled_count  = int((fact_po["po_status"] == "Cancelled").sum())

fact_po.drop(columns=["_is_anomaly", "_year"], inplace=True)

# ---------------------------------------------------------------------------
# 7. Save all CSVs
# ---------------------------------------------------------------------------
def save(df: pd.DataFrame, name: str) -> None:
    path = os.path.join(OUTPUT_DIR, name)
    df.to_csv(path, index=False)
    print(f"  [OK] {name:<35s} {len(df):>6,} rows  ->  {path}")


print("\n-- Saving files ------------------------------------------------------")
save(fact_po,           "fact_purchase_orders.csv")
save(dim_supplier,      "dim_supplier.csv")
save(dim_category,      "dim_category.csv")
save(dim_business_unit, "dim_business_unit.csv")
save(dim_contract,      "dim_contract.csv")
save(dim_date,          "dim_date.csv")

# ---------------------------------------------------------------------------
# 8. Year-over-year spend validation
# ---------------------------------------------------------------------------
print("\n-- Total Spend per Year (MAD) -- excl. Cancelled --------------------")
print(f"{'Year':<6} {'Total Spend (MAD)':>22}  {'YoY Growth':>12}")
print("-" * 44)

active = fact_po[fact_po["po_status"] != "Cancelled"].copy()
active["year"] = pd.to_datetime(active["po_date"]).dt.year
spend_by_year  = active.groupby("year")["total_amount"].sum()

prev_spend = None
for yr, spend in spend_by_year.items():
    if prev_spend is not None:
        growth = (spend - prev_spend) / prev_spend * 100
        print(f"{yr:<6} {spend:>22,.0f}  {'+' + f'{growth:.1f}%':>12}")
    else:
        print(f"{yr:<6} {spend:>22,.0f}  {'(baseline)':>12}")
    prev_spend = spend

# ---------------------------------------------------------------------------
# 9. Data Quality Report
# ---------------------------------------------------------------------------
report_path = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
null_counts  = fact_po.isnull().sum()

with open(report_path, "w", encoding="utf-8") as f:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write("=" * 62 + "\n")
    f.write("  SmartProcure Analytics -- Data Quality Report\n")
    f.write(f"  Generated : {now}\n")
    f.write("=" * 62 + "\n\n")

    # Row counts
    f.write("ROW COUNTS\n" + "-" * 40 + "\n")
    for tbl, cnt in {
        "fact_purchase_orders": len(fact_po),
        "dim_supplier":         len(dim_supplier),
        "dim_category":         len(dim_category),
        "dim_business_unit":    len(dim_business_unit),
        "dim_contract":         len(dim_contract),
        "dim_date":             len(dim_date),
    }.items():
        f.write(f"  {tbl:<28} {cnt:>6,}\n")

    # Null counts
    f.write("\nNULL COUNTS -- fact_purchase_orders\n" + "-" * 40 + "\n")
    for col, cnt in null_counts.items():
        f.write(f"  {col:<32} {cnt:>6,}\n")

    # Value ranges
    f.write("\nVALUE RANGES -- fact_purchase_orders\n" + "-" * 40 + "\n")
    ranges = {
        "total_amount (MAD)":     (fact_po["total_amount"].min(),         fact_po["total_amount"].max()),
        "unit_price (MAD)":       (fact_po["unit_price"].min(),           fact_po["unit_price"].max()),
        "quantity_ordered":       (fact_po["quantity_ordered"].min(),      fact_po["quantity_ordered"].max()),
        "po_cycle_time_days":     (fact_po["po_cycle_time_days"].min(),    fact_po["po_cycle_time_days"].max()),
        "defect_rate_pct":        (fact_po["defect_rate_pct"].min(),       fact_po["defect_rate_pct"].max()),
        "delivery_variance_days": (fact_po["delivery_variance_days"].min(),fact_po["delivery_variance_days"].max()),
    }
    for label, (lo, hi) in ranges.items():
        f.write(f"  {label:<28}  min={lo:>12,.2f}  max={hi:>14,.2f}\n")

    # Anomaly & business rule summary
    f.write("\nANOMALY & BUSINESS-RULE SUMMARY\n" + "-" * 40 + "\n")
    f.write(f"  Anomalous orders (8% target)   : {anomaly_count:>5,}  ({anomaly_count / N_TOTAL * 100:.1f}%)\n")
    f.write(f"  Maverick spend (no contract)   : {maverick_count:>5,}  ({maverick_count / N_TOTAL * 100:.1f}%)\n")
    f.write(f"  Cancelled orders (5% target)   : {cancelled_count:>5,}  ({cancelled_count / N_TOTAL * 100:.1f}%)\n")

    # Status breakdown
    f.write("\nSPEND BY PO STATUS\n" + "-" * 40 + "\n")
    for status, grp in fact_po.groupby("po_status"):
        f.write(f"  {status:<12} {len(grp):>5,} orders  {grp['total_amount'].sum():>18,.0f} MAD\n")

    # Supplier tier performance
    f.write("\nDELIVERY PERFORMANCE BY SUPPLIER TIER\n" + "-" * 40 + "\n")
    merged = fact_po.merge(dim_supplier[["supplier_id", "supplier_tier"]], on="supplier_id")
    tier_stats = merged.groupby("supplier_tier").agg(
        orders         =("po_id",             "count"),
        on_time_pct    =("is_on_time",         "mean"),
        avg_defect_pct =("defect_rate_pct",    "mean"),
        avg_cycle_days =("po_cycle_time_days", "mean"),
    ).reset_index()
    for _, row in tier_stats.iterrows():
        f.write(
            f"  Tier {row['supplier_tier']}  orders={int(row['orders']):>4,}"
            f"  on-time={row['on_time_pct']*100:.1f}%"
            f"  avg_defect={row['avg_defect_pct']:.2f}%"
            f"  avg_cycle={row['avg_cycle_days']:.1f}d\n"
        )

    # YoY spend table
    f.write("\nYEAR-OVER-YEAR SPEND (excl. Cancelled)\n" + "-" * 40 + "\n")
    prev_s = None
    for yr, s in spend_by_year.items():
        if prev_s:
            g = (s - prev_s) / prev_s * 100
            f.write(f"  {yr}  {s:>20,.0f} MAD  YoY +{g:.1f}%\n")
        else:
            f.write(f"  {yr}  {s:>20,.0f} MAD  (baseline)\n")
        prev_s = s

print(f"\n  [OK] {'data_quality_report.txt':<35s}   ->  {report_path}")

# ---------------------------------------------------------------------------
# 10. Final summary
# ---------------------------------------------------------------------------
print("\n-- Generation Summary ------------------------------------------------")
print(f"  Total POs generated     : {len(fact_po):,}")
print(f"  Anomalous orders (~8%)  : {anomaly_count:,}  ({anomaly_count / N_TOTAL * 100:.1f}%)")
print(f"  Maverick spend          : {maverick_count:,}  ({maverick_count / N_TOTAL * 100:.1f}%)")
print(f"  Cancelled (~5%)         : {cancelled_count:,}  ({cancelled_count / N_TOTAL * 100:.1f}%)")
print(f"  Date range              : {dim_date['date'].min()}  ->  {dim_date['date'].max()}")
print(f"\n  All files written to: {os.path.abspath(OUTPUT_DIR)}")
print("-" * 62)
