# Project Structure

## Purpose

This document defines the standard backend project structure for the Food Inventory Leakage Platform.

A consistent project structure improves:

- Maintainability
- Scalability
- Readability
- Testability
- Security
- Separation of Concerns
- Team Collaboration
- AI-Assisted Development

Every backend component must follow this structure.

---

# Design Principles

The backend project structure follows these principles:

- Modular Design
- Layered Architecture
- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection
- API First
- Multi-Tenant by Design
- Secure by Default
- MVP First

Each folder and module must have one clearly defined responsibility.

---

# High-Level Architecture

```text
                 React Frontend
                        │
                REST API (FastAPI)
                        │
        ┌───────────────┴───────────────┐
        │                               │
 Authentication                 Request Validation
        │                               │
        └───────────────┬───────────────┘
                        │
                 Service Layer
                        │
                Repository Layer
                        │
            SQLAlchemy ORM + PostgreSQL
                        │
             Supabase PostgreSQL
```

Business logic belongs exclusively in the Service Layer.

---

# Request Processing Flow

Every authenticated request follows the standard processing pipeline shown below.

```text
HTTP Request
      │
auth.py
(JWT Validation)
      │
tenant.py
(Organization Context + AsyncSession)
      │
permissions.py
(Role Validation)
      │
database.py
(Session Management)
      │
Repository Layer
      │
PostgreSQL (RLS)
```

This processing sequence ensures that every database operation executes within an authenticated organization context before the Repository Layer communicates with PostgreSQL. As a result, PostgreSQL Row-Level Security (RLS) policies automatically enforce organization-level data isolation for every request.

---

# Standard Backend Structure

```text
backend/

├── app/
│
├── api/
│   └── v1/
│       ├── auth.py
│       ├── organizations.py
│       ├── users.py
│       ├── roles.py
│       ├── permissions.py
│       ├── categories.py
│       ├── units.py
│       ├── products.py
│       ├── bom.py
│       ├── warehouses.py
│       ├── suppliers.py
│       ├── customers.py
│       ├── reasons.py
│       ├── purchases.py
│       ├── inventory.py
│       ├── production.py
│       ├── sales.py
│       ├── dispatches.py
│       ├── analytics.py
│       ├── alerts.py
│       ├── imports.py
│       └── jobs.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── permissions.py
│   ├── logging.py
│   ├── constants.py
│   └── exceptions.py
│
├── database/
│   ├── connection.py
│   ├── session.py
│   ├── base.py
│   └── migrations/
│
├── middleware/
│
├── dependencies/
│   ├── auth.py
│   ├── tenant.py
│   ├── permissions.py
│   └── database.py
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── jobs/
│
├── utils/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── fixtures/
│
├── main.py
│
└── requirements.txt
```

This structure is the standard for all backend development.

---

# Folder Responsibilities

## app/

Root application package.

Contains the complete backend source code.

---

## api/

Contains all REST API endpoints.

Responsibilities include:

- Receive HTTP requests
- Validate request format
- Authenticate requests
- Perform endpoint-level authorization
- Call Service Layer
- Return standardized API responses

API endpoints must remain thin.

Business logic must never be implemented in API controllers.

---

## core/

Contains shared infrastructure.

Examples include:

- Configuration
- Security utilities
- Logging
- Constants
- Exception classes
- Shared helper functions

Business logic must not be placed here.

---

## database/

Contains database infrastructure.

Responsibilities include:

- SQLAlchemy configuration
- Database sessions
- Connection management
- Alembic migrations

Database migration standards are defined in **40_Backend_Principles.md**.

---

## middleware/

Contains reusable FastAPI middleware.

Examples include:

- Request logging
- Correlation IDs
- Exception handling
- Performance monitoring
- Security headers

Middleware should remain generic and reusable.

---

## dependencies/

Contains reusable FastAPI dependencies that are injected into API endpoints.

These dependencies provide shared request processing, authentication, authorization, database session management, and organization context establishment.

Examples include:

- Authentication
- Database session management
- Permission validation
- Organization context establishment

### auth.py

Responsibilities:

- Validate Supabase JWT access tokens.
- Identify the authenticated user.
- Reject unauthenticated requests.

### tenant.py

Responsible for establishing the authenticated organization context before any database operation is executed.

Responsibilities:

- Create an authenticated SQLAlchemy AsyncSession.
- Identify the authenticated user's organization.
- Establish the organization context for the current database session.
- Ensure PostgreSQL Row-Level Security (RLS) policies execute using the correct organization context.
- Provide the configured database session to the Repository Layer.

Implementation details are defined in:

- **44_Backend_Security_Architecture.md**
- **45_Database_Access.md**

### permissions.py

Responsibilities:

- Validate role-based permissions.
- Verify endpoint authorization.
- Prevent unauthorized access to protected resources.

### database.py

Responsibilities:

- Create SQLAlchemy database sessions.
- Manage session lifecycle.
- Handle session cleanup.
- Support transaction commit and rollback.



---

## models/

Contains SQLAlchemy ORM models.

Each model represents one database table.

Models define:

- Columns
- Relationships
- Constraints
- Metadata

Models must never contain business workflows.

---

## schemas/

Contains Pydantic models.

Responsibilities include:

- Request validation
- Response serialization
- API documentation
- Data Transfer Objects (DTOs)

Typical schemas include:

- Create
- Update
- Response
- Summary

---

## repositories/

Repositories communicate directly with PostgreSQL.

Responsibilities include:

- CRUD operations
- Query execution
- Data persistence

Repositories must never implement business rules.

---

## services/

The Service Layer contains all business logic.

Examples include:

- Inventory calculations
- Leakage detection
- Production calculations
- Purchase processing
- Dashboard generation
- KPI calculation
- Alert generation

Services coordinate repositories and enforce business rules.

---

## jobs/

Contains scheduled job implementations.

Examples include:

- Leakage detection
- KPI refresh
- Dashboard refresh
- Analytics generation
- Email processing
- Cleanup jobs

Scheduled jobs must reuse the Service Layer instead of implementing business logic independently.

---

## utils/

Contains reusable helper functions.

Examples include:

- Date utilities
- Excel processing
- CSV processing
- File utilities
- Formatting helpers

Utilities should remain stateless.

---

## tests/

Contains automated tests.

Recommended structure:

```text
tests/

├── unit/
├── integration/
├── api/
└── fixtures/
```

Tests should mirror the application structure whenever practical.

---

# Module Organization

Business modules include:

- Authentication
- Organizations
- Users
- Roles
- Permissions
- Categories
- Units
- Products
- Bill of Material (BOM)
- Warehouses
- Suppliers
- Customers
- Reasons
- Purchasing
- Inventory
- Production
- Sales
- Dispatch
- Analytics
- Alerts
- File Import
- Scheduled Jobs

Each module should expose a clear public interface and remain independent from unrelated modules.

---

# API Module Guidelines

For MVP simplicity, related resources may be grouped into a single API module.

Examples:

- `purchases.py` manages Purchase Orders, Purchase Order Items, Goods Receipts, and Goods Receipt Items.
- `inventory.py` manages Inventory Transactions, Stock Balances, Stock Adjustments, Stock Transfers, Physical Stock Counts, and Stock Variances.
- `production.py` manages Production Orders, Consumption, Output, and Waste.
- `analytics.py` manages KPI, Dashboard, Leakage, Yield, and Variance endpoints.
- `alerts.py` manages alert notifications, acknowledgements, and alert history.

Modules may be split into smaller files in future releases if complexity increases.

---

# File Naming Standards

Use lowercase filenames.

Examples:

```text
inventory.py
products.py
analytics.py
security.py
```

Avoid:

- Spaces
- CamelCase filenames
- Ambiguous abbreviations

---

# Import Guidelines

Prefer absolute imports.

Example:

```python
from app.services.inventory_service import InventoryService
```

Avoid circular dependencies.

---

# Configuration Management

Application configuration must remain external.

Configuration includes:

- Database settings
- JWT settings
- Email configuration
- Storage configuration
- Environment variables

Sensitive information must never be stored in source code.

---

# File Storage

Uploaded files should be stored in Supabase Storage.

Temporary files should:

- Be validated
- Be processed securely
- Be deleted immediately after processing

---

# Documentation

Every module should include documentation describing:

- Purpose
- Responsibilities
- Dependencies
- Public interfaces

Documentation should remain synchronized with implementation.

---

# Scalability

The project structure should support future additions without major restructuring.

Examples include:

- ERP Integrations
- OCR Processing
- AI Services
- Mobile APIs
- Event-Driven Processing
- Background Workers
- Notification Services

Future modules should integrate naturally into the existing architecture.

---

# Guiding Principle

A clean project structure is the foundation of a maintainable backend.

Every folder must have a clearly defined responsibility, every layer must respect the separation of concerns, and all business logic must remain centralized in the Service Layer.

This structure supports the Food Inventory Leakage Platform's cloud-native, API-first, multi-tenant, secure-by-default, and MVP-first architecture while providing a scalable foundation for future growth.