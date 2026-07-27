# Master Tables

## Purpose

This document defines the master data entities used by the Food Inventory Leakage Platform.

Master tables store relatively stable business information that supports day-to-day operations. Unlike transaction tables, master data changes infrequently and serves as the foundation for purchasing, inventory management, production, reporting, and leakage detection.

---

# Design Principles

Master tables should:

- Store reusable business information.
- Avoid duplicate data.
- Support multi-tenant architecture.
- Maintain referential integrity.
- Support auditability.
- Remain independent of transaction history.
- Be reusable across multiple business modules.

Every master table belongs to a single Organization (Tenant).

---

# Organization & Security

## Organization

Represents a customer company using the platform.

Example fields:

- organization_id
- organization_name
- registration_number
- tax_number
- email
- phone
- address
- country
- city
- status

One Organization represents one Tenant.

---

## User

Stores application users.

Example fields:

- user_id
- organization_id
- role_id
- full_name
- email
- mobile
- status

Users authenticate through Supabase Auth.

---

## Role

Defines application roles.

Examples:

- Owner
- Factory Manager
- Production Manager
- Warehouse Manager
- Inventory Manager
- Store Officer
- Accounts Manager
- Auditor

---

## Permission

Defines permissions assigned to roles.

Examples:

- View Dashboard
- Manage Products
- Manage Inventory
- Create Purchase Orders
- Approve Stock Adjustments
- View Reports

---

# Product Management

## Category

Groups products into logical categories.

Examples:

- Raw Material
- Packaging Material
- Finished Goods
- Consumables

---

## Unit

Defines measurement units.

Examples:

- Kilogram
- Gram
- Liter
- Milliliter
- Piece
- Box
- Carton

---

## Product

Stores all inventory items.

Example fields:

- product_id
- category_id
- unit_id
- product_code
- product_name
- product_type
- minimum_stock
- maximum_stock
- reorder_level
- status

Products may represent:

- Raw Materials
- Packaging Materials
- Finished Goods
- Consumables

---

## Bill of Material (BOM)

Defines the standard recipe or formulation required to manufacture a finished product.

A BOM specifies:

- Finished Product
- Raw Material
- Standard Quantity
- Unit of Measure

The BOM provides the expected material consumption used for:

- Production planning
- Yield analysis
- Leakage detection
- Variance analysis

---

# Warehouse Management

## Warehouse

Represents a physical inventory location.

Example fields:

- warehouse_id
- warehouse_code
- warehouse_name
- warehouse_type
- location
- status

---

# Business Partners

## Supplier

Stores supplier information.

Example fields:

- supplier_id
- supplier_code
- supplier_name
- contact_person
- phone
- email
- address
- status

---

## Customer

Stores customer information.

Example fields:

- customer_id
- customer_code
- customer_name
- contact_person
- phone
- email
- address
- status

---

# Operational Configuration

## Reason

Defines standardized reasons used throughout the application.

Examples:

- Stock Damage
- Production Waste
- Inventory Leakage
- Adjustment
- Transfer
- Expired Stock
- Quality Rejection

Using standardized reasons improves reporting and root-cause analysis.

---

# Common Columns

Every master table should include:

- organization_id
- created_at
- updated_at
- created_by
- updated_by

Where applicable:

- deleted_at
- deleted_by
- status
- remarks

---

# Relationships

Organization owns:

- Users
- Roles
- Warehouses
- Products
- Suppliers
- Customers

Products reference:

- Category
- Unit

Bill of Material references:

- Finished Product
- Raw Material

Inventory references:

- Product
- Warehouse

Purchasing references:

- Supplier
- Product

Production references:

- Product
- Bill of Material

---

# Validation Rules

Master data should enforce:

- Mandatory fields
- Unique business codes
- Valid foreign keys
- Active/inactive status
- Standardized units of measure
- Consistent product categorization

Business validation is implemented in FastAPI.

---

# Future Master Tables

The following master tables may be introduced as the platform evolves:

- Brand
- Product Group
- Production Line
- Machine
- Shift
- Department
- Cost Center
- Currency
- Tax Category
- Quality Standard
- Warehouse Zone
- Shelf / Bin Location

These tables should be added only when justified by business requirements.

---

# Guiding Principle

Master tables define the core business entities of the Food Inventory Leakage Platform.

They should remain:

- Simple
- Accurate
- Reusable
- Consistent
- Multi-tenant
- Well-governed

Every transactional, analytical, and reporting process depends on the integrity and quality of the master data.