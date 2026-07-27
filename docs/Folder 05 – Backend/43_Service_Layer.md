# Service Layer

## Purpose

This document defines the Service Layer architecture for the Food Inventory Leakage Platform.

The Service Layer is the core business engine of the application. It contains all business rules, coordinates workflows, validates business operations, and orchestrates interactions between repositories, external services, and scheduled jobs.

Business logic must exist only within the Service Layer.

---

# Objectives

The Service Layer should:

- Centralize all business logic
- Coordinate business workflows
- Enforce business rules
- Maintain data consistency
- Support multi-tenant operations
- Remain independent of API implementation
- Remain independent of database implementation
- Support automated testing
- Enable future scalability

---

# Design Principles

The Service Layer follows these principles:

- Single Responsibility Principle
- Separation of Concerns
- Dependency Injection
- Business Logic First
- Stateless Services
- Reusable Components
- Transaction Safety
- MVP First

---

# Position in the Architecture

```text
React Frontend
       │
REST API (FastAPI)
       │
API Router
       │
Dependency Injection
       │
──────────────
Service Layer
──────────────
       │
Repository Layer
       │
SQLAlchemy ORM
       │
Supabase PostgreSQL
```

The Service Layer sits between the API Layer and the Repository Layer.

---

# Responsibilities

The Service Layer is responsible for:

- Business rule enforcement
- Workflow orchestration
- Inventory calculations
- Leakage detection
- Production processing
- Purchase processing
- Stock validation
- KPI generation
- Analytics generation
- Alert generation
- File processing coordination
- Transaction coordination
- Integration with external services

---

# Responsibilities That Do NOT Belong Here

The Service Layer must not perform:

- HTTP request handling
- Response formatting
- JWT validation
- SQL query construction
- Database connection management
- ORM model definitions
- UI logic

These responsibilities belong to other layers.

---

# Service Workflow

Every business operation follows a consistent flow.

```text
API Request

      │

Validation

      │

Service Method

      │

Business Rules

      │

Repository Operations

      │

Database Transaction

      │

Business Result

      │

API Response
```

---

# Service Organization

Business services should be organized by domain.

Examples:

- Organization Service
- User Service
- Product Service
- Warehouse Service
- Supplier Service
- Customer Service
- Purchase Service
- Inventory Service
- Production Service
- Analytics Service
- Alert Service
- Import Service

Each service owns its business domain.

---

# Business Rule Ownership

Business rules belong exclusively in the Service Layer.

Examples include:

- Stock cannot become negative.
- Product must belong to the current organization.
- Warehouse must be active.
- Production cannot consume unavailable inventory.
- Leakage thresholds determine alert severity.
- Physical count variances require approval.
- Duplicate imports should be prevented.

These rules must never be duplicated in controllers or repositories.

---

# Repository Coordination

Services coordinate one or more repositories.

Example:

```text
Purchase Service

      │

      ├── Purchase Repository

      ├── Inventory Repository

      ├── Supplier Repository

      └── Alert Repository
```

Repositories never communicate directly with each other.

---

# Transaction Management

Services are responsible for coordinating database transactions.

Typical transactional operations include:

- Purchase completion
- Inventory adjustment
- Production completion
- Stock transfer
- Physical stock reconciliation

If any step fails, the entire transaction should be rolled back.

---

# Validation Responsibilities

Validation occurs at multiple layers.

## API Layer

Responsible for:

- Required fields
- Data types
- Basic request validation

---

## Service Layer

Responsible for:

- Business validation
- Workflow validation
- Inventory validation
- Cross-entity validation
- Authorization-related business rules

---

## Database Layer

Responsible for:

- Foreign keys
- Constraints
- Unique indexes
- Row-Level Security

Each layer validates only what belongs to it.

---

# Service Communication

Services may call other services when appropriate.

Example:

```text
Production Service

        │

Inventory Service

        │

Analytics Service

        │

Alert Service
```

Circular dependencies between services should be avoided.

---

# Dependency Injection

Services should receive dependencies through constructor or FastAPI dependency injection.

Typical dependencies include:

- Repository instances
- Configuration
- Email service
- File storage service
- Logger

Services should never create their own dependencies.

---

# Error Handling

Services should raise business exceptions rather than HTTP exceptions.

Examples:

- InsufficientInventoryError
- DuplicateImportError
- ProductInactiveError
- WarehouseClosedError
- InvalidProductionError

The API Layer converts business exceptions into standardized HTTP responses.

---

# Logging

Services should log important business events.

Examples:

- Purchase completed
- Inventory adjusted
- Leakage detected
- Production completed
- File imported
- Alert generated

Sensitive information must never be logged.

---

# Scheduled Jobs

Scheduled jobs should reuse Service Layer methods.

Examples:

- Leakage detection
- KPI refresh
- Dashboard refresh
- Email processing
- Cleanup operations

Business logic must never be duplicated inside scheduled jobs.

---

# External Integrations

The Service Layer coordinates integrations with:

- Supabase Storage
- Brevo Email
- Metabase
- Scheduled Jobs

Integration logic should remain isolated from business rules whenever possible.

---

# Testing

The Service Layer should be independently testable.

Recommended tests include:

- Unit tests
- Business rule tests
- Workflow tests
- Transaction tests
- Error handling tests

Repositories and external services should be mocked during unit testing.

---

# Performance Principles

Services should:

- Minimize unnecessary repository calls
- Avoid duplicate queries
- Batch operations where appropriate
- Return only required data
- Reuse shared business logic

Performance optimization should be guided by real measurements rather than assumptions.

---

# Scalability

The Service Layer should support future enhancements without architectural redesign.

Future additions may include:

- AI-assisted leakage detection
- OCR processing
- ERP integrations
- Mobile services
- Workflow automation
- Event-driven processing

New services should integrate naturally into the existing architecture.

---

# Documentation

Every service should document:

- Purpose
- Responsibilities
- Public methods
- Dependencies
- Business rules
- Exceptions raised

Documentation should remain synchronized with implementation.

---

# Guiding Principle

The Service Layer is the business heart of the Food Inventory Leakage Platform.

It centralizes business rules, coordinates workflows, protects data integrity, and ensures that every business operation behaves consistently regardless of how it is triggered—through REST APIs, scheduled jobs, or future integrations.

A clean, well-designed Service Layer enables a secure, maintainable, scalable, and testable backend while keeping business logic independent from the API, database, and infrastructure layers.