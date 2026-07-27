# Analytics API

## Purpose

This document defines the REST API endpoints for accessing analytics, dashboards, key performance indicators (KPIs), and leakage detection results within the Food Inventory Leakage Platform.

Analytics APIs provide business intelligence generated from transactional data. They enable users to monitor inventory performance, detect leakage, measure production efficiency, and support operational decision-making.

Business calculations are performed by FastAPI scheduled jobs. Analytics APIs are primarily read-only.

---

# Design Principles

Analytics APIs should be:

- RESTful
- Stateless
- Secure
- Multi-tenant
- Read-optimized
- High performance
- Consistent
- Scalable

Analytics APIs should never modify transactional business data.

---

# API Base URL

All endpoints begin with:

```text
/api/v1/
```

---

# Authentication

All Analytics APIs require:

- Valid JWT Access Token
- Active User
- Active Organization
- Appropriate Role
- Required Permission

Unauthorized requests must be rejected.

---

# Analytics Architecture

Analytics data is generated from:

- Purchase Transactions
- Inventory Transactions
- Production Transactions
- Stock Adjustments
- Stock Transfers
- Physical Stock Counts
- Sales Transactions

FastAPI processes business rules and stores analytical results in dedicated Analytics tables.

The Analytics API exposes these results to the frontend.

---

# Leakage Events API

## Purpose

Retrieve detected inventory leakage events.

Endpoints

```text
GET /leakage-events

GET /leakage-events/{id}
```

Supported Filters

```text
?warehouse_id=

?product_id=

?severity=

?status=

?from_date=

?to_date=
```

Typical Information

- Leakage Date
- Product
- Warehouse
- Expected Quantity
- Actual Quantity
- Variance
- Estimated Financial Loss
- Severity
- Status

These records are generated automatically.

---

# Inventory Variance API

## Purpose

Retrieve inventory variance analysis.

Endpoints

```text
GET /inventory-variance

GET /inventory-variance/{id}
```

Supported Filters

```text
?warehouse_id=

?product_id=

?from_date=

?to_date=
```

Typical Information

- System Quantity
- Physical Quantity
- Variance Quantity
- Variance Percentage
- Estimated Loss

---

# Production Yield API

## Purpose

Retrieve production efficiency analysis.

Endpoints

```text
GET /production-yield

GET /production-yield/{id}
```

Supported Filters

```text
?product_id=

?production_order_id=

?from_date=

?to_date=
```

Typical Information

- Production Order
- Finished Product
- Planned Quantity
- Actual Output
- Expected Consumption
- Actual Consumption
- Yield Percentage
- Waste Percentage

Production Yield calculations use the Bill of Material (BOM) as the expected production baseline.

---

# Inventory KPI API

## Purpose

Retrieve inventory performance indicators.

Endpoints

```text
GET /inventory-kpis
```

Typical KPIs

- Inventory Accuracy
- Stock Variance
- Inventory Value
- Stock Turnover
- Waste Percentage
- Leakage Percentage
- Stock Availability

---

# Operational KPI API

## Purpose

Retrieve operational business metrics.

Endpoints

```text
GET /operational-kpis
```

Typical KPIs

- Purchase Performance
- Goods Receipt Performance
- Production Efficiency
- Warehouse Utilization
- Inventory Movement
- Stock Adjustment Trends

---

# Dashboard API

## Purpose

Retrieve dashboard summary information.

Endpoints

```text
GET /dashboard

GET /dashboard/summary

GET /dashboard/charts
```

Dashboard may include

- Total Products
- Total Warehouses
- Current Inventory Value
- Today's Transactions
- Leakage Alerts
- Production Summary
- Inventory Trends
- KPI Summary

Dashboard responses should use cached analytical data whenever appropriate.

---

# Alert API

## Purpose

Retrieve operational alerts.

Endpoints

```text
GET /alerts

GET /alerts/{id}
```

Examples

- High Leakage
- Negative Inventory
- Low Stock
- Overstock
- Production Exception
- Inventory Variance
- Failed Import

Alerts are generated automatically by scheduled processing.

---

# Trend Analysis API

## Purpose

Retrieve historical trends.

Endpoints

```text
GET /analytics/trends
```

Supported Filters

```text
?metric=

?period=daily

?period=weekly

?period=monthly

?from_date=

?to_date=
```

Example Metrics

- Leakage
- Inventory Value
- Production Output
- Waste
- Stock Variance

---

# Dashboard Cache

Analytics APIs should retrieve cached dashboard data whenever available.

Dashboard cache reduces:

- Database load
- API response time
- Dashboard rendering time

Cached data is refreshed through scheduled jobs.

---

# Filtering

Analytics APIs should support filtering.

Examples

```text
?warehouse_id=5

?product_id=20

?severity=High

?status=Open

?from_date=2026-07-01

?to_date=2026-07-31
```

---

# Pagination

Large analytical datasets should support pagination.

Example

```text
?page=1

?page_size=50
```

---

# Sorting

Analytics endpoints should support sorting.

Examples

```text
?sort=event_date

?sort=-estimated_loss

?sort=-variance_percentage
```

---

# Security

Every request must:

- Validate JWT
- Verify Organization
- Verify User Role
- Verify Permissions
- Enforce Row Level Security

Analytics must never expose another organization's information.

---

# Performance Guidelines

Analytics APIs should:

- Read only from Analytics tables
- Use indexed columns
- Support pagination
- Use cached dashboard data where possible
- Minimize expensive calculations during requests

Business calculations must not execute during API requests.

---

# Error Handling

Analytics APIs should return standardized responses for:

- Invalid Request
- Unauthorized
- Forbidden
- Validation Failure
- Resource Not Found
- Internal Server Error

Sensitive implementation details must never be exposed.

---

# Future Enhancements

Future analytics capabilities may include:

- AI-based anomaly detection
- Predictive inventory forecasting
- Demand forecasting
- Interactive dashboards
- Drill-down analytics
- Benchmarking
- Custom KPI Builder
- Executive Scorecards
- Export to Excel
- Export to PDF

These enhancements should extend the existing API structure without affecting backward compatibility.

---

# Guiding Principle

Analytics APIs transform operational data into actionable business intelligence.

Every endpoint should be:

- Secure
- Read-optimized
- Fast
- Consistent
- Multi-tenant
- Scalable
- Easy to consume
- Easy to maintain

Analytics APIs provide decision-makers with accurate, timely, and reliable operational insights while preserving the platform's API-first, cloud-native, and MVP-first architecture.