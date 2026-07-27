# Analytics Tables

## Purpose

This document defines the analytical tables used by the Food Inventory Leakage Platform.

Analytics tables store calculated, summarized, and derived business information generated from operational transactions. They improve reporting performance, support executive dashboards, and enable leakage detection without modifying the original transactional records.

Operational transaction tables remain the single source of truth.

---

# Design Principles

Analytics tables should:

- Store derived business information.
- Never replace transactional records.
- Improve dashboard performance.
- Support executive reporting.
- Support leakage detection.
- Support historical trend analysis.
- Be reproducible from transactional data.
- Support multi-tenant architecture.
- Be refreshed through scheduled processing.

---

# Analytics Architecture

The platform separates operational processing from analytical processing.

```text
Operational Transactions
        │
        ▼
FastAPI Business Logic
        │
        ▼
Analytics Tables
        │
        ▼
Dashboards
        │
        ▼
Reports
```

Business calculations are performed exclusively by **FastAPI**.

Analytics tables store the calculated results.

---

# Analytics Processing

Analytics data is generated from:

- Inventory Transactions
- Stock Balances
- Production Orders
- Production Consumption
- Production Output
- Production Waste
- Stock Variance

Analytics tables must never be updated manually.

They are refreshed automatically using scheduled jobs.

---

# Scheduled Processing

Scheduled processing may be initiated by:

- Supabase pg_cron
- GitHub Actions
- External schedulers

These schedulers trigger FastAPI jobs.

FastAPI performs:

- Leakage detection
- Yield calculations
- KPI calculations
- Variance analysis
- Dashboard refresh

Business calculations must never execute directly inside PostgreSQL stored procedures.

---

# Leakage Event

Stores detected inventory leakage incidents.

Typical fields include:

- leakage_event_id
- warehouse_id
- product_id
- detection_date
- leakage_type
- variance_quantity
- estimated_loss
- severity
- status

Leakage Events are generated automatically by FastAPI.

---

# Variance Analysis

Stores calculated inventory reconciliation results.

Typical fields include:

- variance_analysis_id
- warehouse_id
- product_id
- system_quantity
- physical_quantity
- variance_quantity
- variance_percentage
- variance_value

Variance Analysis supports inventory investigations and leakage reporting.

---

# Production Yield Analysis

Stores production efficiency calculations.

Typical metrics include:

- expected_material_consumption
- actual_material_consumption
- expected_output
- actual_output
- yield_percentage
- waste_percentage
- efficiency_score

Expected values are derived from the Bill of Material (BOM).

Actual values are derived from Production Consumption and Production Output.

---

# Inventory KPI

Stores summarized inventory performance indicators.

Examples include:

- Current Inventory Value
- Stock Turnover
- Inventory Accuracy
- Low Stock Count
- Overstock Count
- Inventory Variance Rate

These KPIs support warehouse and inventory management.

---

# Operational KPI

Stores organization-wide operational performance indicators.

Examples include:

- Leakage Rate
- Waste Rate
- Production Efficiency
- Purchase Accuracy
- Inventory Accuracy
- Adjustment Frequency

Operational KPIs support executive decision-making.

---

# Dashboard Cache

Dashboard Cache stores pre-calculated summary data used to improve dashboard response time.

Typical dashboard summaries include:

- Inventory Overview
- Production Summary
- Leakage Summary
- KPI Dashboard
- Executive Dashboard

Dashboard Cache is derived entirely from Analytics Tables.

---

# Data Refresh Strategy

Analytics data should be refreshed according to business requirements.

Typical refresh intervals may include:

- Hourly
- Daily
- Weekly
- Monthly

Refresh frequency should balance reporting accuracy with system performance.

---

# Data Retention

Operational transaction tables remain the permanent business record.

Analytics tables may be:

- Rebuilt
- Refreshed
- Archived

At any time using operational transaction data.

Historical KPI snapshots may be retained for trend analysis.

---

# Common Columns

Every analytics table should include:

- organization_id
- calculation_date
- generated_at
- generated_by

Where appropriate:

- reporting_period
- refresh_status
- remarks

---

# Relationships

Analytics tables derive information from:

- Inventory Transaction
- Stock Balance
- Stock Variance
- Production Order
- Production Consumption
- Production Output
- Production Waste
- Bill of Material (BOM)

Analytics tables provide information to:

- Executive Dashboards
- Operational Dashboards
- Reports
- Alert Engine

---

# Business Rules

- Operational tables remain the authoritative source of truth.
- Analytics tables contain derived information only.
- Analytics tables must never be edited manually.
- Business calculations execute exclusively in FastAPI.
- Scheduled jobs trigger FastAPI processing.
- Analytics tables can always be regenerated from transactional data.
- Dashboard Cache improves reporting performance but is not authoritative.

---

# Future Analytics

Future analytical capabilities may include:

- Predictive Analytics
- Machine Learning
- AI-based Leakage Detection
- Demand Forecasting
- Inventory Optimization
- Production Forecasting
- Anomaly Detection
- Recommendation Engine

These capabilities will extend the existing analytics layer without changing the operational database.

---

# Guiding Principle

Analytics tables transform operational data into business intelligence.

They should remain:

- Accurate
- Reproducible
- High-performance
- Multi-tenant
- Scalable
- Easy to maintain

The operational database remains the single source of truth, while analytics tables provide fast, reliable, and meaningful insights for decision-makers.