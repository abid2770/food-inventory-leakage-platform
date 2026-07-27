# Entity Relationship Diagram (ERD)

## Purpose

This document defines the logical Entity Relationship Diagram (ERD) for the Food Inventory Leakage Platform.

The ERD provides the conceptual structure of the database and defines how business entities relate to one another.

It serves as the foundation for database schema design, API development, business logic implementation, reporting, and leakage detection.

---

# Design Principles

The database follows these principles:

- Multi-tenant architecture
- Shared database, shared schema
- Third Normal Form (3NF)
- Master data separated from transactional data
- Transactional data separated from analytical data
- Business logic implemented in FastAPI
- PostgreSQL responsible for data integrity
- Support for auditability
- Support for future expansion
- MVP-first design philosophy

---

# High-Level Database Modules

The platform is divided into the following logical modules.

```text
Organization & Security
│
├── Organization
├── User
├── Role
└── Permission

Master Data
│
├── Category
├── Unit
├── Product
├── Warehouse
├── Supplier
├── Customer
├── Bill_of_Material (BOM)
└── Reason

Purchasing
│
├── Purchase_Order
├── Purchase_Order_Item
├── Goods_Receipt
└── Goods_Receipt_Item

Inventory
│
├── Inventory_Transaction
├── Stock_Balance
├── Stock_Adjustment
├── Stock_Transfer
├── Physical_Stock_Count
└── Stock_Variance

Production
│
├── Production_Order
├── Production_Consumption
├── Production_Output
└── Production_Waste

Analytics
│
├── Leakage_Event
├── Variance_Analysis
├── Production_Yield
├── Inventory_KPI
├── Operational_KPI
└── Dashboard_Cache

Alerts
│
├── Alert_Queue
└── Email_Queue
```

---

# Core Business Relationships

## Organization

Organization

↓

User

↓

Role

↓

Permission

Each Organization represents one Tenant.

Every business record belongs to exactly one Organization.

---

## Product Management

Category

↓

Product

↓

Unit

↓

Warehouse

Products belong to Categories.

Products are measured using Units.

Products are stored in Warehouses.

---

## Purchasing

Supplier

↓

Purchase_Order

↓

Purchase_Order_Item

↓

Goods_Receipt

↓

Goods_Receipt_Item

↓

Inventory_Transaction

Every approved Goods Receipt creates Inventory Transactions.

---

## Inventory

Warehouse

↓

Inventory_Transaction

↓

Stock_Balance

↓

Physical_Stock_Count

↓

Stock_Variance

Inventory Transactions are the official inventory ledger.

Stock Balance represents the current inventory position and is maintained from Inventory Transactions for reporting and dashboard performance.

Physical Stock Counts are compared against Stock Balance to produce Stock Variance records.

---

## Production

Bill_of_Material (BOM)

↓

Production_Order

↓

Production_Consumption

↓

Production_Output

↓

Production_Waste

The Bill of Material defines the expected raw material consumption for each finished product.

Production Orders consume raw materials and produce finished goods.

Yield calculations compare expected consumption (BOM) against actual consumption.

---

## Leakage Detection

Inventory_Transaction

↓

Stock_Variance

↓

Variance_Analysis

↓

Leakage_Event

↓

Alert_Queue

Leakage detection analyzes inventory movements and production results to identify unusual losses, excessive waste, shortages, or unexplained variances.

Alerts are generated for significant leakage events.

---

## Reporting

Inventory_Transaction

↓

Analytics Tables

↓

Dashboard_Cache

↓

Reports

↓

Executive Dashboards

Operational data remains the system of record.

Analytics tables contain derived calculations optimized for reporting.

---

# Master Data Relationships

Organization owns:

- Users
- Warehouses
- Products
- Suppliers
- Customers

Products reference:

- Category
- Unit
- Bill_of_Material

Inventory references:

- Product
- Warehouse

Purchasing references:

- Supplier
- Product
- Warehouse

Production references:

- Product
- Bill_of_Material
- Warehouse

Analytics references:

- Product
- Warehouse
- Organization

---

# Inventory Flow

```text
Purchase
      │
      ▼
Goods Receipt
      │
      ▼
Inventory Transaction
      │
      ▼
Stock Balance
      │
      ├─────────────► Production Consumption
      │
      ├─────────────► Sales
      │
      ├─────────────► Stock Transfer
      │
      ├─────────────► Stock Adjustment
      │
      └─────────────► Physical Count
                            │
                            ▼
                    Stock Variance
                            │
                            ▼
                    Leakage Detection
```

---

# Production Flow

```text
Bill of Material
        │
        ▼
Production Order
        │
        ▼
Production Consumption
        │
        ▼
Production Output
        │
        ▼
Production Waste
        │
        ▼
Yield Analysis
        │
        ▼
Leakage Detection
```

---

# Analytical Flow

```text
Operational Transactions
          │
          ▼
Analytics Processing
          │
          ▼
Leakage Events
          │
          ▼
KPIs
          │
          ▼
Dashboards
          │
          ▼
Executive Reports
```

---

# Future Expansion

The ERD supports future modules without requiring major redesign.

Future modules may include:

- ERP Integration
- Mobile Applications
- OCR Processing
- AI & Machine Learning
- Predictive Analytics
- Demand Forecasting
- IoT Integration
- Quality Control
- Maintenance Management
- Financial Integration

These modules will extend the existing architecture while preserving the current relational model.

---

# Guiding Principle

The ERD is the logical blueprint of the Food Inventory Leakage Platform.

It should remain:

- Simple
- Business-focused
- Secure
- Multi-tenant
- Normalized
- Scalable
- Maintainable

Every future database table, API, report, and business rule must align with this ERD.