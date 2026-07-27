# Database Access

## Purpose

This document defines the database access architecture for the Food Inventory Leakage Platform.

It establishes how FastAPI, SQLAlchemy, and Supabase PostgreSQL interact to provide secure, maintainable, and efficient data access while preserving a clear separation of responsibilities.

Business logic must never reside in the database layer.

---

# Objectives

The Database Access layer should:

- Provide secure database access
- Encapsulate all SQLAlchemy operations
- Isolate persistence from business logic
- Support multi-tenant architecture
- Respect PostgreSQL Row-Level Security (RLS)
- Maintain transaction integrity
- Support scalability
- Enable automated testing
- Minimize database coupling

---

# Design Principles

The Database Access layer follows these principles:

- Repository Pattern
- Separation of Concerns
- Dependency Injection
- Transaction Safety
- Multi-Tenant by Design
- Secure by Default
- Readability over Complexity
- MVP First

---

# Position in the Architecture

```text
React Frontend
       │
REST API
       │
API Layer
       │
Service Layer
       │
──────────────────────
Repository Layer
──────────────────────
       │
SQLAlchemy ORM
       │
Supabase PostgreSQL
```

The Repository Layer is the only layer permitted to communicate directly with the database.

---

# Responsibilities

The Repository Layer is responsible for:

- CRUD operations
- Query construction
- Data retrieval
- Data persistence
- Transaction participation
- Pagination
- Filtering
- Sorting
- Entity loading

Repositories must not implement business rules.

---

# Responsibilities Outside This Layer

The Repository Layer must never perform:

- Business calculations
- Inventory reconciliation
- Leakage detection
- Authorization decisions
- HTTP request handling
- Response formatting
- JWT validation

These responsibilities belong to other architectural layers.

---

# SQLAlchemy

SQLAlchemy 2.0 is the official ORM for the platform.

The platform uses SQLAlchemy AsyncSession together with the asyncpg PostgreSQL driver.

All repository operations execute asynchronously using Python async/await.

SQLAlchemy is responsible for:

- ORM mapping
- Relationship management
- Query generation
- Session management
- Transaction management
- Connection pooling

All database access must use SQLAlchemy.

---

# Repository Pattern

Each business domain owns a dedicated repository responsible only for persistence.

Examples include:

- Organization Repository
- User Repository
- Product Repository
- Warehouse Repository
- Supplier Repository
- Purchase Repository
- Inventory Repository
- Production Repository
- Analytics Repository

Repositories are responsible only for data persistence.

Repositories must never:

- implement business rules,
- perform authentication,
- perform authorization,
- establish tenant context,
- execute business workflows,
- call external services.

Business orchestration always belongs to the Service Layer.

---

# Database Sessions

Each HTTP request receives its own SQLAlchemy database session.

The session lifecycle is fully managed through FastAPI dependency injection.

Typical request flow:

```text
Client Request
       │
JWT Validation
       │
User Authentication
       │
Organization Identification
       │
Create SQLAlchemy Session
       │
Establish Tenant Context
       │
Repository Operations
       │
Commit / Rollback
       │
Close Session
```

Database sessions must never be shared across concurrent requests.

Each request executes inside an isolated database transaction.

The Database Access layer is responsible for establishing tenant context before any repository executes database operations.
---

# Transaction Management

The Service Layer coordinates transactions.

Repositories participate in transactions but do not decide transaction boundaries.

Typical transaction workflow:

```text
Begin Transaction

        │

Repository Operations

        │

Commit

or

Rollback
```

If any operation fails, the transaction must be rolled back.

---

# Query Design

Queries should:

- Return only required columns
- Use appropriate filtering
- Support pagination
- Minimize unnecessary joins
- Avoid N+1 query problems
- Use indexes effectively

Database performance should be continuously monitored.

---

# ORM Relationships

SQLAlchemy relationships should be defined only where they improve readability and maintainability.

Relationships should:

- Match the approved ERD
- Avoid circular dependencies
- Use lazy loading appropriately
- Prevent unnecessary database queries

---

# Tenant Context and Row-Level Security

The platform uses PostgreSQL Row-Level Security (RLS) as the primary tenant isolation mechanism.

After successful JWT authentication, FastAPI identifies:

- user_id
- organization_id
- assigned roles and permissions

The Database Access layer establishes the tenant context for the current database transaction before executing any repository operation.

Tenant context is established automatically using:

```sql
SET LOCAL app.organization_id = '<organization_id>';
```

The tenant context remains valid only for the current transaction.

Repositories must never execute this command directly.

All business tables enforce tenant isolation through PostgreSQL Row-Level Security using:

```sql
current_setting('app.organization_id', true)
```

Repositories must never attempt to replace RLS by manually filtering tenant data.

Additional business filtering is permitted, but tenant isolation is always enforced by PostgreSQL.

If tenant context establishment fails:

- the transaction is cancelled,
- no SQL statements are executed,
- the request fails immediately,
- the security event is logged.

Complete implementation details are documented in:

- 25_RLS_Policies.md
- 44_Backend_Security_Architecture.md
---

# Raw SQL

Raw SQL should be avoided whenever practical.

Raw SQL is acceptable only when:

- SQLAlchemy cannot efficiently express the query.
- Performance has been measured.
- The query has been reviewed.
- Parameterized queries are used.

Business logic must never be embedded in SQL.

---

# Pagination

Large result sets should use pagination.

Supported pagination features include:

- Page number
- Page size
- Sorting
- Filtering

Pagination standards are defined in the API Design documents.

---

# Filtering

Filtering should be performed at the database level whenever possible.

Typical filters include:

- Organization
- Warehouse
- Product
- Supplier
- Date range
- Status
- Category

Filtering should leverage indexed columns.

---

# Performance Principles

Repositories should:

- Minimize database round trips
- Batch related operations
- Avoid duplicate queries
- Reuse common query patterns
- Return only necessary data

Optimization should be evidence-based rather than speculative.

---

# Connection Management

SQLAlchemy manages all database connections through a connection pool.

The application should:

- Reuse pooled database connections.
- Release connections immediately after request completion.
- Avoid long-running transactions.
- Monitor connection pool utilization.
- Follow Supabase connection management recommendations.

Alembic migrations are an exception and must always use the direct Supabase PostgreSQL connection rather than the pooled connection.
---

# Migrations

Alembic is the official migration framework.

Rules:

- Every schema change must use Alembic.
- Migrations must be version controlled.
- Prefer reversible migrations.
- Never modify production schemas manually.
- Alembic migrations must connect using the direct Supabase connection string, not the pooled connection, to avoid transaction-mode pooling issues with DDL operations.

---

# Error Handling

Repository methods should raise database-related exceptions only.

Business exceptions belong in the Service Layer.

The API Layer converts exceptions into standardized API responses.

---

# Testing

Repository testing should verify:

- CRUD operations
- Query correctness
- Relationships
- Transaction behavior
- Pagination
- Filtering
- Performance-sensitive queries

Business logic should not be tested in repository tests.

---

# Logging

Database access logging should include:

- Query failures
- Transaction failures
- Connection failures
- Migration execution
- Unexpected exceptions

Sensitive information must never appear in logs.

---

# Scalability

The Repository Layer should support:

- Millions of records
- Thousands of organizations
- Future database optimization
- Read-heavy analytics
- Additional business modules

Scalability should not require architectural redesign.

---

# Future Enhancements

Future improvements may include:

- Read replicas
- Query optimization
- Database caching
- Materialized views
- Advanced indexing
- Partitioning (if justified by production data)

These enhancements should remain transparent to the Service Layer.

---

# Documentation

Every repository should document:

- Purpose
- Managed entities
- Public methods
- Query behavior
- Transactions
- Dependencies

Documentation should remain synchronized with implementation.

---

# Guiding Principle

The Database Access Layer provides the secure bridge between FastAPI and PostgreSQL.

FastAPI authenticates every request.

The Database Access Layer establishes the tenant context.

SQLAlchemy performs all persistence operations.

PostgreSQL Row-Level Security automatically enforces tenant isolation.

Repositories remain focused exclusively on persistence, allowing business logic to remain inside the Service Layer while keeping the platform secure, maintainable, scalable, cloud-native, and fully aligned with the project's API-first and multi-tenant architecture.