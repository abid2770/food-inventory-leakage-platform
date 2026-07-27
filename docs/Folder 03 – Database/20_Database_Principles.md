# 20_Database_Principles.md

# Database Principles

## Purpose

This document defines the database architecture principles for the Food Inventory Leakage Platform.

It establishes the standards, conventions, and design decisions that govern the PostgreSQL database used throughout the platform.

These principles ensure the database remains secure, scalable, maintainable, and aligned with the overall system architecture.

The database serves as the authoritative source of truth for all business data while keeping business logic within the FastAPI application.

---

# Database Platform

The platform uses:

- PostgreSQL (Supabase)
- Row Level Security (RLS)
- SQLAlchemy ORM
- Alembic Migrations

PostgreSQL is responsible for secure data storage, transactional consistency, constraints, indexing, and query execution.

Business rules must never be implemented inside PostgreSQL stored procedures.

---

# Database Design Objectives

The database must provide:

- Multi-tenant architecture
- Strong data integrity
- High performance
- Scalability
- Security by default
- Auditability
- Extensibility
- Reliable reporting
- AI-ready data structures

---

# Multi-Tenant Architecture

The platform uses a:

**Shared Database**
**Shared Schema**
**Row Level Security (RLS)**

architecture.

Every business table contains:

- organization_id
- created_at
- created_by
- updated_at
- updated_by

The term **organization** represents the tenant throughout the system. Therefore, `organization_id` is the tenant identifier used consistently across the application, database, API, and backend.

Every database query must automatically respect tenant isolation through PostgreSQL Row Level Security policies.

---

# Separation of Responsibilities

## FastAPI Responsibilities

FastAPI is responsible for:

- Business rules
- Inventory calculations
- Leakage detection
- Production calculations
- Production yield calculations
- Expected vs Actual Consumption calculations
- Workflow orchestration
- Validation
- Authorization
- Scheduled jobs
- Email notifications

---

## PostgreSQL Responsibilities

PostgreSQL is responsible for:

- Data persistence
- Transactions
- Constraints
- Foreign keys
- Indexes
- Views
- Row Level Security
- Query execution
- ACID compliance

Business calculations must never execute inside PostgreSQL stored procedures.

---

# Database Design Principles

## Normalize Operational Data

Operational tables should remain normalized to reduce redundancy and maintain data integrity.

---

## Separate Analytics from Transactions

Analytics tables are derived from transactional data.

They never become the authoritative source of truth.

---

## Bill of Material (BOM)

The Bill of Material (BOM) is a core master data entity included in the MVP.

Every finished product may define one or more raw materials together with their standard consumption quantities.

Production Yield Analysis, Expected vs Actual Consumption, Variance Analysis, and Inventory Leakage Detection use the active BOM as the baseline for business calculations.

The BOM is maintained as master data, while all calculations execute within the FastAPI Service Layer.

---

## Inventory Balance Strategy

Inventory Transactions are the authoritative source of truth.

The Stock Balance table stores the latest calculated inventory quantity for each product and warehouse to improve reporting and dashboard performance.

If inconsistencies occur, Stock Balance can always be rebuilt from Inventory Transactions.

---

# Naming Standards

The project follows consistent singular table names.

Examples:

- Organization
- Product
- Warehouse
- Supplier
- PurchaseOrder
- InventoryTransaction
- ProductionOrder
- LeakageEvent

Primary keys use:

```
table_name_id
```

Examples:

```
organization_id
product_id
warehouse_id
purchase_order_id
```

Foreign keys always reference the parent primary key.

---

# Primary Keys

Every table uses a surrogate primary key.

Identity or UUID selection follows the project standards defined in the architecture documents.

Primary keys never contain business meaning.

---

# Foreign Keys

All relationships must be enforced using foreign keys.

Orphan records are not permitted.

---

# Audit Columns

Business tables must include:

- created_at
- created_by
- updated_at
- updated_by

Soft delete columns should be included where business requirements require logical deletion:

- deleted_at
- deleted_by

Physical deletion of business data should normally be avoided.

---

# Data Integrity

The database must enforce:

- Primary Keys
- Foreign Keys
- NOT NULL
- CHECK Constraints
- UNIQUE Constraints
- Referential Integrity

Business validation remains inside FastAPI.

---

# Performance Principles

Performance improvements must be based on measured workload.

Avoid premature optimization.

Use:

- Proper indexes
- Query optimization
- Pagination
- Efficient joins
- Batch processing

---

# Indexing Principles

Indexes should prioritize:

- organization_id
- Foreign Keys
- Frequently filtered columns
- Frequently joined columns
- Frequently sorted columns

Composite indexes should be created only when justified by actual query patterns.

---

# Security Principles

Security is enforced through:

- PostgreSQL Row Level Security
- JWT Authentication
- Organization isolation
- Least privilege
- Audit logging

Application database users must never bypass Row Level Security.

---

# Scalability Principles

The database must support:

- Thousands of organizations
- Millions of inventory transactions
- Large production histories
- Large analytical datasets

without structural redesign.

---

# Future Database Enhancements

Future releases may introduce:

- Table partitioning
- Read replicas
- Materialized views
- Advanced indexing
- Data archiving
- Performance tuning based on production workloads

These enhancements must not change the core database architecture.

---

# Documentation Standards

Every schema change must include:

- Alembic migration
- Documentation update
- Architecture review (if applicable)
- Version control

No manual production schema changes are permitted.

---

# Guiding Principle

The database is the secure, authoritative repository of business data.

PostgreSQL manages storage, integrity, security, and performance.

FastAPI owns all business logic, workflow orchestration, inventory calculations, production calculations, leakage detection, and analytical processing.

This separation of responsibilities ensures a maintainable, scalable, and secure architecture aligned with the overall platform design.