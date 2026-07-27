# FastAPI Architecture

## Purpose

This document defines the overall FastAPI architecture for the Food Inventory Leakage Platform.

It explains how FastAPI components interact, how requests flow through the system, and how the backend coordinates business logic, security, database access, and external services.

This document establishes the architectural blueprint for all backend development.

---

# Objectives

The FastAPI application should:

- Provide secure REST APIs
- Execute business logic
- Validate requests
- Coordinate database operations
- Enforce authorization
- Support multi-tenancy
- Process scheduled jobs
- Integrate with external services
- Remain modular and maintainable
- Scale without major redesign

---

# Design Principles

The FastAPI architecture follows these principles:

- API First
- Stateless
- Layered Architecture
- Dependency Injection
- Separation of Concerns
- Secure by Default
- Multi-Tenant by Design
- Cloud Native
- MVP First

---

# High-Level Architecture

```text
                 React Frontend
                        │
                 HTTPS REST API
                        │
                  FastAPI Router
                        │
                Authentication
                        │
                 Authorization
                        │
                Dependency Injection
                        │
                  Service Layer
                        │
               Repository Layer
                        │
              SQLAlchemy ORM
                        │
            Supabase PostgreSQL
```

---

# Request Lifecycle

Every request follows the same lifecycle.

```text
Client Request
        │
        ▼
API Router
        │
        ▼
Authentication
        │
        ▼
Authorization
        │
        ▼
Request Validation
        │
        ▼
Dependency Injection
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
Database
        │
        ▼
Response
```

Each layer performs one clearly defined responsibility.

---

# Layer Responsibilities

## API Layer

Responsibilities:

- Receive HTTP requests
- Validate request structure
- Call dependencies
- Return standardized responses
- Invoke Service Layer

The API layer must remain lightweight.

---

## Dependency Layer

Responsibilities:

- Database session
- Current user
- Current organization
- Permission validation
- Shared dependencies

Implementation details for tenant context are defined in **44_Backend_Security_Architecture.md**.

---

## Service Layer

Responsibilities:

- Business rules
- Workflow orchestration
- Inventory calculations
- Leakage detection
- Production processing
- KPI generation
- Alert generation

Business logic belongs only in this layer.

---

## Repository Layer

Responsibilities:

- CRUD operations
- Database queries
- Data persistence
- Transaction participation

Repositories never contain business rules.

---

## Database Layer

Responsibilities:

- Data storage
- Constraints
- Foreign keys
- Indexes
- Row-Level Security
- Transaction integrity

The database should not implement application workflows.

---

# API Routing

Endpoints should be organized by business domain.

Examples:

- Authentication
- Organizations
- Users
- Products
- Warehouses
- Purchasing
- Inventory
- Production
- Analytics
- File Import
- Scheduled Jobs

Each router should expose only related endpoints.

---

# Dependency Injection

FastAPI dependencies should provide:

- Database session
- Authentication
- Authorization
- Configuration
- Shared services

Dependencies should remain reusable and independent.

---

# Validation

All incoming requests must be validated using Pydantic models.

Validation includes:

- Required fields
- Data types
- Length limits
- Numeric ranges
- Enumerations
- Date validation

Business validation belongs in the Service Layer.

---

# Authentication

Authentication is performed before business processing.

Responsibilities include:

- JWT validation
- User identification
- Organization identification
- Session establishment

Authentication implementation is defined in **32_Authentication_Authorization.md** and **44_Backend_Security_Architecture.md**.

---

# Authorization

Authorization determines whether an authenticated user may perform the requested operation.

Authorization includes:

- Role validation
- Permission validation
- Resource ownership validation

Authorization must be enforced before executing business logic.

---

# Database Access

The application accesses PostgreSQL only through the Repository Layer.

The API Layer and Service Layer must never execute raw SQL directly.

Database access standards are defined in **45_Database_Access.md**.

---

# Transaction Management

Business operations involving multiple database changes should execute within transactions.

Examples include:

- Purchase processing
- Production completion
- Stock adjustments
- Inventory transfers

Transactions must guarantee ACID properties.

---

# Exception Handling

All exceptions should be handled consistently.

Responses should include:

- HTTP status code
- Error code
- Human-readable message

Internal implementation details must never be exposed.

Complete standards are defined in **38_Error_Handling.md**.

---

# Logging

The application should log:

- API requests
- Authentication events
- Authorization failures
- Exceptions
- Scheduled jobs
- File imports

Sensitive information must never appear in logs.

Detailed logging standards are defined in **48_Logging_Monitoring.md**.

---

# Background Processing

Some operations execute asynchronously.

Examples include:

- Leakage detection
- KPI calculation
- Dashboard refresh
- Email processing
- Cleanup tasks

Background jobs should reuse Service Layer functionality.

Implementation details are defined in **47_Background_Jobs.md**.

---

# File Processing

File uploads follow this workflow:

```text
Upload
   │
Validation
   │
Storage
   │
Parsing
   │
Business Validation
   │
Database Processing
   │
Result
```

Implementation details are defined in **36_File_Import_API.md**.

---

# External Services

The backend integrates with:

- Supabase Auth
- Supabase PostgreSQL
- Supabase Storage
- Brevo Email
- Metabase
- GitHub Actions (where applicable)

External services communicate through well-defined interfaces.

---

# Scalability

The architecture should support:

- Thousands of organizations
- Millions of transactions
- Additional API modules
- Future ERP integrations
- AI services
- OCR
- Mobile applications

Scalability should be achieved through clean architecture rather than unnecessary complexity.

---

# Documentation

Every endpoint should automatically appear in the OpenAPI specification.

Documentation should include:

- Purpose
- Parameters
- Authentication requirements
- Responses
- Status codes
- Example requests
- Example responses

OpenAPI documentation must remain synchronized with implementation.

---

# Future Enhancements

Future architectural improvements may include:

- API versioning beyond v1
- Background worker queues
- Event-driven architecture
- Caching
- WebSockets
- GraphQL
- AI microservices

These enhancements should integrate without requiring major architectural redesign.

---

# Guiding Principle

FastAPI is the orchestration layer of the Food Inventory Leakage Platform.

It coordinates authentication, authorization, validation, business logic, database access, and external integrations while maintaining a clean separation of responsibilities.

Every request should follow a consistent, secure, and maintainable execution path that supports the platform's cloud-native, API-first, multi-tenant, and MVP-first architecture.

# Asynchronous Architecture

The backend follows a fully asynchronous architecture using FastAPI, SQLAlchemy, and PostgreSQL.

## Asynchronous Technology Stack

The platform uses:

- FastAPI asynchronous endpoints
- SQLAlchemy 2.0 AsyncSession
- asyncpg PostgreSQL driver
- Python async/await programming model

All database operations execute asynchronously.

---

## Request Processing

Each HTTP request follows this sequence:

```text
Client Request
        │
FastAPI Endpoint
        │
Service Layer
        │
Repository Layer
        │
SQLAlchemy AsyncSession
        │
Supabase PostgreSQL
```

Every layer communicates using asynchronous functions.

---

## Design Rules

The backend architecture follows these rules:

- All API endpoints use `async def`.
- Service Layer methods execute asynchronously.
- Repository methods execute asynchronously.
- Database operations use SQLAlchemy AsyncSession.
- PostgreSQL communication uses the asyncpg driver.
- Blocking database operations should be avoided.

---

## Benefits

A fully asynchronous architecture provides:

- Better request concurrency
- Improved scalability
- Efficient database connection utilization
- Reduced response latency
- Better cloud resource utilization

---

## Guiding Principle

The platform adopts asynchronous programming as the standard backend execution model to maximize scalability, responsiveness, and efficient resource utilization while maintaining a simple and consistent architecture.