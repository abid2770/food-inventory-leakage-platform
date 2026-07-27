# 25_RLS_Policies.md

## Tenant Context Mechanism

The platform enforces tenant isolation through a combination of FastAPI authentication, SQLAlchemy session management, and PostgreSQL Row Level Security (RLS).

### Authentication

Every authenticated request must include a valid Supabase JWT access token.

FastAPI validates the JWT before any business operation is performed.

After successful authentication, FastAPI identifies:

- user_id
- organization_id
- assigned roles and permissions

The **organization_id** represents the tenant identifier throughout the platform.

---

### Establishing Tenant Context

After authentication and before executing any database query, FastAPI establishes the tenant context for the current database transaction.

The tenant context is created by executing:

```sql
SET LOCAL app.organization_id = '<organization_id>';
```

This operation is performed automatically by the database session layer.

Application developers must never execute this command manually inside business services or repositories.

---

### Row Level Security Enforcement

All business tables use PostgreSQL Row Level Security (RLS).

Every RLS policy retrieves the active tenant using:

```sql
current_setting('app.organization_id', true)
```

Database policies automatically restrict data access to the authenticated organization.

Repositories and business services must never manually filter records by organization_id as a replacement for RLS.

Additional business filtering may be applied, but tenant isolation is always enforced by PostgreSQL.

---

### Failure Handling

If the tenant context cannot be established for any reason:

- Database access must be denied.
- The request must fail immediately.
- No SQL statement may execute without an active tenant context.
- The error must be logged for security auditing.

Failing securely is mandatory.

---

### Administrative Access

Administrative operations requiring cross-tenant access must use dedicated service accounts with explicitly approved permissions.

Normal application database connections must never possess the PostgreSQL `BYPASSRLS` privilege.

Cross-tenant access is permitted only for approved administrative or maintenance operations.

---

### Guiding Principle

Tenant isolation is enforced automatically through PostgreSQL Row Level Security.

FastAPI establishes the authenticated organization context, PostgreSQL enforces tenant isolation, and SQLAlchemy transparently operates within that secured context.

Business code must never bypass or replace this security model.



# Row-Level Security (RLS) Policies

**Version:** 1.1  
**Status:** Approved  
**Last Updated:** July 2026

---

# Purpose

This document defines the Row-Level Security (RLS) strategy for the Food Inventory Leakage Detection Platform.

RLS is the primary database-level security mechanism that guarantees tenant isolation in the multi-tenant SaaS platform.

This document is the authoritative reference for all PostgreSQL Row-Level Security (RLS) policies.

---

# Objectives

The RLS implementation must:

- Prevent cross-tenant data access.
- Protect all business data.
- Provide database-level security.
- Complement application-layer authorization.
- Support secure multi-tenant architecture.
- Provide defense in depth.

---

# Security Model

The platform uses multiple security layers.

```
Client
    │
    ▼
HTTPS
    │
    ▼
FastAPI
    │
    ▼
JWT Validation
    │
    ▼
Authorization
    │
    ▼
Tenant Context Initialization
    │
    ▼
SQLAlchemy
    │
    ▼
PostgreSQL Row-Level Security
    │
    ▼
Business Tables
```

Application authorization and PostgreSQL RLS work together.

Neither replaces the other.

---

# Tenant Isolation Strategy

The platform is a multi-tenant SaaS application.

Every organization owns only its own data.

Every business table contains:

```text
organization_id
```

The database must never return rows belonging to another tenant.

---

# Tenant Context Standard

## Principle

FastAPI communicates directly with PostgreSQL using SQLAlchemy.

Application requests do **not** pass through Supabase PostgREST.

Therefore, PostgreSQL does not automatically receive authentication claims from Supabase Auth.

The backend is responsible for establishing the authenticated tenant context for every database session.

---

## Standard Implementation

For every authenticated request:

1. Supabase Auth authenticates the user.
2. FastAPI validates the JWT.
3. FastAPI determines the authenticated tenant.
4. SQLAlchemy creates a new database session.
5. The backend stores the tenant identifier as a **session-local database setting**.
6. PostgreSQL RLS policies evaluate that session-local tenant value.

A tenant context exists only for the lifetime of the current request.

Tenant context must never be shared between sessions.

---

# RLS Policy Standard

Every business table must have Row-Level Security enabled.

Every RLS policy must evaluate the authenticated tenant context established by the backend.

RLS policies must **not** depend on:

- `auth.uid()`
- `auth.jwt()`

for application requests processed through FastAPI.

Instead, policies evaluate the tenant identifier supplied through the authenticated SQLAlchemy session.

This architecture keeps RLS independent of Supabase PostgREST while preserving database-level tenant isolation.

---

# Tables Protected by RLS

RLS is mandatory for all business tables, including:

## Master Tables

- Organization
- Warehouse
- Product
- Supplier
- Customer
- Recipe
- User

## Transaction Tables

- Purchase
- PurchaseItem
- ProductionBatch
- ProductionConsumption
- ProductionOutput
- InventoryTransaction
- Sales
- SalesItem
- StockAdjustment
- WasteEntry

## Analytics Tables

- LeakageAlert
- KPIHistory
- DashboardSnapshot

Future business tables must also implement RLS.

---

# Operations Protected by RLS

Every policy must protect:

- SELECT
- INSERT
- UPDATE
- DELETE

No operation may bypass tenant isolation.

---

# Application Responsibilities

FastAPI is responsible for:

- JWT validation
- User authentication
- Permission validation
- Establishing the tenant context
- Creating tenant-aware SQLAlchemy sessions

FastAPI does not replace database security.

---

# Database Responsibilities

PostgreSQL is responsible for:

- Row filtering
- Tenant isolation
- Preventing cross-tenant access
- Enforcing RLS policies

The database remains the final security boundary.

---

# Administrative Access

Administrative users must still authenticate.

Administrative privileges are granted through application roles.

Administrative access must be explicitly authorized.

Bypassing RLS is prohibited except for controlled administrative or maintenance operations that are documented, audited, and executed using dedicated service credentials.

---

# Background Jobs

Background jobs execute using dedicated service credentials.

Where tenant-specific processing is required:

- Each job must establish the appropriate tenant context.
- Jobs must process one tenant at a time.
- Audit logs must be generated.

Examples:

- Leakage detection
- Dashboard refresh
- KPI calculation
- Email notifications

---

# Security Principles

Always:

- Enable RLS on business tables.
- Validate authentication.
- Validate permissions.
- Establish tenant context before database access.
- Audit security events.

Never:

- Disable RLS.
- Share database sessions.
- Bypass tenant isolation.
- Trust client-supplied tenant identifiers.
- Expose data across organizations.

---

# Testing Requirements

The RLS implementation must be tested for:

- Cross-tenant isolation
- Unauthorized access
- Tenant switching
- Background jobs
- Administrative operations
- Permission boundaries

Security testing is mandatory before production deployment.

---

# Summary

The platform uses PostgreSQL Row-Level Security as the database-level enforcement mechanism for tenant isolation.

The security flow is:

1. User authenticates with Supabase Auth.
2. FastAPI validates the JWT.
3. FastAPI determines the authenticated tenant.
4. A tenant-aware SQLAlchemy session is created.
5. The tenant identifier is established as a session-local database context.
6. PostgreSQL RLS evaluates that tenant context.
7. Only rows belonging to the authenticated tenant are returned.

This layered approach provides secure, scalable, and maintainable multi-tenant isolation while keeping authentication, authorization, and database security clearly separated.

Physical deletion of business data should normally be avoided. Soft deletes are the default approach for business entities unless a documented exception has been approved.