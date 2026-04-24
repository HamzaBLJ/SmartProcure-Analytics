# ⚙️ Power Query M Code — SmartProcure Analytics

Paste each block into the corresponding table's **Advanced Editor** in Excel Power Query.

> **Load order matters:** dim tables first, fact table last.
> dim_date → dim_supplier → dim_category → dim_business_unit → dim_contract → fact_purchase_orders

---

## dim_date

```m
let
    Source = Csv.Document(File.Contents("data/raw/dim_date.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"date", type date},
        {"day", Int64.Type},
        {"month", Int64.Type},
        {"month_name", type text},
        {"quarter", Int64.Type},
        {"year", Int64.Type},
        {"week_number", Int64.Type},
        {"is_weekend", type logical},
        {"is_month_end", type logical},
        {"fiscal_quarter", type text},
        {"day_of_week_name", type text}
    }),
    AddedShortMonth = Table.AddColumn(ChangedTypes, "short_month",
        each Text.Start([month_name], 3), type text),
    SortedAscending = Table.Sort(AddedShortMonth, {{"date", Order.Ascending}})
in
    SortedAscending
```

---

## dim_supplier

```m
let
    Source = Csv.Document(File.Contents("data/raw/dim_supplier.csv"),
        [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"supplier_id", type text},
        {"supplier_name", type text},
        {"supplier_tier", type text},
        {"country", type text},
        {"city", type text},
        {"category_specialty", type text},
        {"contract_start_date", type date},
        {"contract_end_date", type date},
        {"payment_terms_days", Int64.Type},
        {"is_strategic", type logical},
        {"risk_score", Int64.Type}
    }),
    AddedContractStatus = Table.AddColumn(ChangedTypes, "contract_status",
        each if [contract_end_date] < Date.From(DateTime.LocalNow()) then "Expired"
             else if Duration.Days([contract_end_date] - Date.From(DateTime.LocalNow())) <= 90
             then "Expiring Soon"
             else "Active",
        type text),
    AddedSupplierLabel = Table.AddColumn(AddedContractStatus, "supplier_label",
        each [supplier_name] & " (" & [supplier_tier] & ")", type text)
in
    AddedSupplierLabel
```

---

## dim_category

```m
let
    Source = Csv.Document(File.Contents("data/raw/dim_category.csv"),
        [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"category_id", type text},
        {"category_name", type text},
        {"category_group", type text},
        {"budget_annual", type number},
        {"criticality_level", type text}
    })
in
    ChangedTypes
```

---

## dim_business_unit

```m
let
    Source = Csv.Document(File.Contents("data/raw/dim_business_unit.csv"),
        [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"business_unit_id", type text},
        {"business_unit_name", type text},
        {"region", type text},
        {"annual_budget", type number},
        {"budget_owner", type text}
    })
in
    ChangedTypes
```

---

## dim_contract

```m
let
    Source = Csv.Document(File.Contents("data/raw/dim_contract.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"contract_id", type text},
        {"contract_name", type text},
        {"supplier_id", type text},
        {"category_id", type text},
        {"contract_type", type text},
        {"start_date", type date},
        {"end_date", type date},
        {"contract_value", type number},
        {"currency", type text},
        {"is_active", type logical},
        {"auto_renewal", type logical},
        {"negotiated_savings_pct", type number}
    }),
    AddedDaysToExpiry = Table.AddColumn(ChangedTypes, "days_to_expiry",
        each Duration.Days([end_date] - Date.From(DateTime.LocalNow())), Int64.Type),
    AddedContractHealth = Table.AddColumn(AddedDaysToExpiry, "contract_health",
        each if [days_to_expiry] < 0 then "Expired"
             else if [days_to_expiry] <= 90 then "Expiring Soon"
             else "Healthy",
        type text),
    AddedDurationMonths = Table.AddColumn(AddedContractHealth, "contract_duration_months",
        each Duration.Days([end_date] - [start_date]) / 30.44, type number),
    RoundedDuration = Table.TransformColumns(AddedDurationMonths,
        {{"contract_duration_months", Number.RoundDown, Int64.Type}})
in
    RoundedDuration
```

---

## fact_purchase_orders

```m
let
    Source = Csv.Document(File.Contents("data/raw/fact_purchase_orders.csv"),
        [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"po_id", type text},
        {"po_date", type date},
        {"supplier_id", type text},
        {"category_id", type text},
        {"business_unit_id", type text},
        {"contract_id", type text},
        {"quantity_ordered", Int64.Type},
        {"unit_price", type number},
        {"total_amount", type number},
        {"po_cycle_time_days", Int64.Type},
        {"actual_delivery_date", type date},
        {"requested_delivery_date", type date},
        {"is_on_time", type logical},
        {"delivery_variance_days", Int64.Type},
        {"defect_rate_pct", type number},
        {"payment_terms_days", Int64.Type},
        {"po_status", type text}
    }),
    ReplacedNullContract = Table.ReplaceValue(ChangedTypes,
        null, "No Contract", Replacer.ReplaceValue, {"contract_id"}),
    AddedDeliveryStatus = Table.AddColumn(ReplacedNullContract, "delivery_status",
        each if [delivery_variance_days] < 0 then "Early"
             else if [delivery_variance_days] = 0 then "On Time"
             else if [delivery_variance_days] <= 7 then "Late 1-7 Days"
             else "Late 7+ Days",
        type text),
    AddedSpendBucket = Table.AddColumn(AddedDeliveryStatus, "spend_bucket",
        each if [total_amount] < 100000 then "< 100K MAD"
             else if [total_amount] < 500000 then "100K–500K MAD"
             else if [total_amount] < 1000000 then "500K–1M MAD"
             else "> 1M MAD",
        type text),
    Percentile95 = List.Percentile(
        Table.Column(AddedSpendBucket, "total_amount"), 0.95),
    AddedAnomalyFlag = Table.AddColumn(AddedSpendBucket, "is_anomaly",
        each [total_amount] > Percentile95, type logical),
    FilteredActive = Table.SelectRows(AddedAnomalyFlag,
        each [po_status] <> "Cancelled"),
    RenamedColumns = Table.RenameColumns(FilteredActive, {
        {"po_cycle_time_days", "PO Cycle Time (Days)"},
        {"defect_rate_pct", "Defect Rate (%)"},
        {"total_amount", "Total Amount (MAD)"},
        {"delivery_variance_days", "Delivery Variance (Days)"}
    })
in
    RenamedColumns
```

---

## fact_cancelled_orders (separate query)

```m
let
    Source = Csv.Document(File.Contents("data/raw/fact_purchase_orders.csv"),
        [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"po_date", type date},
        {"total_amount", type number},
        {"po_status", type text}
    }),
    FilteredCancelled = Table.SelectRows(ChangedTypes,
        each [po_status] = "Cancelled")
in
    FilteredCancelled
```

---

## Parameters Table

```m
let
    Source = #table(
        {"Parameter", "Value"},
        {
            {"ReportRefreshDate", Date.From(DateTime.LocalNow())},
            {"CompanyName", "SmartProcure Analytics"},
            {"BaseCurrency", "MAD"},
            {"AnomalyThresholdPct", "95th Percentile"},
            {"MaverickSpendLabel", "No Contract"}
        }
    )
in
    Source
```

---

*SmartProcure Analytics — Power Query M Documentation*
