# 40_Backend_Principles.md

# Backend Principles

**Version:** 1.2  
**Status:** Approved  
**Last Updated:** July 2026

---

# Purpose

This document defines the backend architecture and development principles for the Food Inventory Leakage Detection Platform.

It establishes the standards that every backend component must follow to ensure the system remains secure, maintainable, scalable, and consistent.

This document defines architectural principles only. Detailed security implementation is documented in **44_Backend_Security_Architecture.md**.

---

# Backend Objectives

The backend is responsible for:

- Business logic
- Inventory processing
- Leakage detection
- API services
- Authentication integration
- Authorization
- Multi-tenant data isolation
- Background processing
- Audit logging

---

# Backend Technology Stack

| Layer | Technology |
|---------|------------|
| Framework | FastAPI |
| Language | Python 3.12+ |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Validation | Pydantic |
| Database | Supabase PostgreSQL |
| Authentication | Supabase Auth |
| Storage | Supabase Storage |
| Background Jobs | Supabase pg_cron + GitHub Actions |
| Email | Brevo |
| Deployment | Render |

---

# Architecture Overview

The backend follows a layered architecture.

```
Client
    │
    ▼
FastAPI API Layer
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
SQLAlchemy
    │
    ▼
PostgreSQL
```

Each layer has a single responsibility.

---

# Layer Responsibilities

## API Layer

Responsible for:

- HTTP endpoints
- Request validation
- Authentication
- Authorization
- Response formatting
- HTTP status codes

The API layer must not contain business logic.

---

## Service Layer

Responsible for:

- Business rules
- Leakage detection
- Inventory calculations
- Production calculations
- Purchase validation
- Sales validation
- Report orchestration
- Workflow management

Business logic belongs only in this layer.

---

## Repository Layer

Responsible for:

- Database access
- CRUD operations
- Query optimization
- SQLAlchemy interaction

Repositories isolate persistence logic from business logic.

Repositories must never contain business rules.

---

## Database Layer

Responsible for:

- Data storage
- Constraints
- Transactions
- Indexes
- Row-Level Security (RLS)
- Data integrity

Business logic should not reside in PostgreSQL except for integrity constraints and RLS policies.

---

# Separation of Responsibilities

| Responsibility | Layer |
|---------------|-------|
| Authentication | Supabase Auth + API Layer |
| Authorization | Service Layer |
| Business Rules | Service Layer |
| Database Access | Repository Layer |
| Data Integrity | PostgreSQL |
| Tenant Isolation | PostgreSQL RLS |

---

# Multi-Tenant Architecture

The platform is designed as a multi-tenant SaaS application.

Every organization has complete logical isolation from every other organization.

Tenant isolation is enforced through PostgreSQL Row-Level Security (RLS).

The backend must preserve authenticated tenant context throughout every request.

The detailed implementation of tenant context propagation is defined in:

**44_Backend_Security_Architecture.md**

---

# SQLAlchemy Principles

SQLAlchemy is the official ORM.

Guidelines:

- Use ORM for normal CRUD operations.
- Use SQLAlchemy Core where performance requires it.
- Avoid unnecessary raw SQL.
- Keep models simple.
- Keep repositories focused on persistence.
- Optimize queries before increasing complexity.

The backend uses SQLAlchemy 2.0 with AsyncSession.

All database operations execute asynchronously using Python async/await.

The asyncpg driver is the standard PostgreSQL driver for the platform.

Synchronous database access must not be introduced into the backend architecture.

---

# Alembic Principles

Alembic is the official migration framework.

Rules:

- Every schema change must use Alembic.
- Never modify production schemas manually.
- Store migrations in version control.
- Prefer reversible migrations.
- Alembic migrations must connect using the direct Supabase connection string, not the pooled connection, to avoid transaction-mode pooling issues with DDL operations.

# Dependency Injection

FastAPI dependency injection should manage:

- Database sessions
- Services
- Repositories
- Authentication
- Configuration

Avoid global state whenever possible.

---

# Validation Principles

Use Pydantic for:

- Request validation
- Response validation
- Type safety
- Input sanitization

Never trust client input.

---

# Error Handling

The backend must:

- Return meaningful HTTP status codes.
- Use centralized exception handling.
- Log server-side failures.
- Avoid exposing internal implementation details.
- Return user-friendly error messages.

---

# Logging

The backend must log:

- Authentication events
- Authorization failures
- API failures
- Scheduled job execution
- Leakage detection results
- Administrative actions
- Critical business events

Sensitive information such as passwords, JWTs, refresh tokens, API keys, and database credentials must never be logged.

---

# Performance Principles

The backend should:

- Remain stateless.
- Use pagination.
- Query only required columns.
- Prevent N+1 queries.
- Use indexes appropriately.
- Optimize only after measurement.

Premature optimization should be avoided.

---

# Security Principles

The backend follows a defense-in-depth strategy.

Every request must:

- Be authenticated.
- Be authorized.
- Be validated.
- Execute within the authenticated tenant context.
- Be protected by PostgreSQL Row-Level Security.

The detailed security architecture is documented in:

**44_Backend_Security_Architecture.md**

---

# Coding Standards

Backend code must:

- Follow PEP 8.
- Use type hints.
- Prefer readability.
- Keep functions focused.
- Use descriptive names.
- Avoid duplication.
- Keep modules organized by feature.

---

# Scalability Principles

The architecture must support:

- Multiple organizations
- Multiple warehouses
- Millions of inventory transactions
- Large product catalogs
- Background processing
- Future AI modules
- Future integrations

Scalability should be achieved through clean architecture rather than unnecessary complexity.

---

# MVP Philosophy

The project follows an MVP-first approach.

Guidelines:

- Build only required functionality.
- Prefer simplicity.
- Avoid unnecessary abstraction.
- Avoid premature optimization.
- Deliver working software quickly.
- Refactor when justified by business needs.

---

# Summary

The backend architecture is based on the following principles:

- FastAPI for application services
- SQLAlchemy as the official ORM
- Alembic for database migrations
- Repository pattern for data access
- Service layer for business logic
- PostgreSQL as the system of record
- Row-Level Security for tenant isolation
- Defense-in-depth security
- Dependency injection
- Stateless application design
- Clean, maintainable, and scalable architecture

This document defines the architectural principles for backend development. Implementation details for authentication, tenant context propagation, Row-Level Security, and security controls are maintained in **44_Backend_Security_Architecture.md**.