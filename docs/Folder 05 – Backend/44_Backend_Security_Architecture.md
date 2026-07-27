# 44_Backend_Security_Architecture.md

# Backend Security Architecture

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** July 2026

---

# Purpose

This document defines the backend security architecture for the Food Inventory Leakage Detection Platform.

Its objectives are to:

- Protect customer data
- Enforce tenant isolation
- Prevent unauthorized access
- Support secure API communication
- Provide defense in depth
- Maintain a clear separation between authentication, authorization, and business logic

This document is the authoritative implementation guide for backend security and complements:

- 20_Database_Principles.md
- 25_RLS_Policies.md
- 32_Authentication_Authorization.md
- 40_Backend_Principles.md

---

# Security Principles

The platform follows these principles:

- Zero Trust
- Least Privilege
- Defense in Depth
- Secure by Default
- Fail Securely
- Principle of Separation of Responsibilities

Every request must be authenticated, authorized, validated, and isolated before business logic is executed.

---

# Security Layers

```
Client

↓

HTTPS

↓

FastAPI API

↓

JWT Validation

↓

Tenant Context Initialization

↓

Authorization

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy Session

↓

PostgreSQL Row-Level Security (RLS)

↓

Database
```

Every layer contributes to security.

No single layer is trusted on its own.

---

# Authentication

Authentication is provided by **Supabase Auth**.

Responsibilities:

- User login
- Password management
- Password reset
- Session management
- JWT generation
- Token expiration
- Identity verification

FastAPI never authenticates users directly.

It validates JWTs issued by Supabase Auth.

---

# Authorization

After authentication:

1. Validate the JWT.
2. Identify the authenticated user.
3. Determine the user's organization and tenant.
4. Verify required permissions.
5. Establish the tenant context.
6. Execute business logic.

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

---

# Tenant Isolation

The platform is a multi-tenant SaaS application.

Every organization owns only its own data.

Tenant isolation is enforced using PostgreSQL Row-Level Security (RLS).

No request may access another tenant's records.

---

## Tenant Context Establishment

Every authenticated request follows the same security workflow to guarantee complete tenant isolation.

### Authentication

1. The client sends a valid Supabase JWT access token.
2. FastAPI validates the JWT.
3. FastAPI identifies:
   - user_id
   - organization_id
   - assigned roles and permissions

The organization_id is the tenant identifier used throughout the platform.

### Database Session

Before executing any business query, the database session establishes the tenant context by executing:

```sql
SET LOCAL app.organization_id = '<organization_id>';

# Tenant Context Propagation

## Principle

Because FastAPI communicates directly with PostgreSQL through SQLAlchemy, requests do not pass through Supabase PostgREST.

Therefore, the backend must explicitly establish the authenticated tenant context for each database session.

## Standard

After successful JWT validation:

1. FastAPI identifies the authenticated tenant.
2. A new SQLAlchemy session is created.
3. The tenant context is established for that session.
4. Repository operations execute within that tenant-aware session.
5. PostgreSQL RLS policies evaluate the tenant context before returning any data.

Tenant context is established **per request** and **per database session**.

No tenant context may be shared between requests.

---

# Row-Level Security (RLS)

RLS is mandatory for every business table.

RLS provides database-level tenant isolation.

Application code must never rely solely on service-layer filtering.

Even if a repository query accidentally omits a tenant filter, RLS remains the final protection against cross-tenant access.

The detailed RLS policy definitions are maintained in:

current_setting('app.organization_id', true)

**25_RLS_Policies.md**

---

# SQLAlchemy Security

Database sessions must:

- Be created per request.
- Be automatically closed after request completion.
- Never be shared across users.
- Execute only within the authenticated tenant context.

Repository classes must never disable or bypass tenant isolation.

---

# Repository Security

Repositories are responsible only for:

- Reading data
- Writing data
- Updating data
- Deleting data

Repositories are **not** responsible for:

- Authentication
- Authorization
- Business rules
- Permission checks

Security decisions belong to higher layers.

---

# Service Layer Security

The Service Layer is responsible for:

- Business authorization
- Permission validation
- Workflow validation
- Business rule enforcement

Examples:

- Can approve stock adjustment
- Can edit purchase
- Can delete production batch
- Can view reports

The Service Layer never bypasses database security.

---

# API Security

Every protected endpoint must:

- Require authentication.
- Validate JWTs.
- Validate request data.
- Authorize user permissions.
- Create a tenant-aware database session.
- Return standardized responses.

Public endpoints must be explicitly documented.

---

# HTTPS

All environments outside local development must use HTTPS.

HTTP is never permitted in production.

---

# Secrets Management

Sensitive values must never be stored in source code.

Examples:

- JWT secrets
- API keys
- Database credentials
- SMTP credentials
- Encryption keys

Secrets must be stored using environment variables.

---

# Password Security

Passwords are managed entirely by Supabase Auth.

The application:

- Never stores passwords.
- Never hashes passwords.
- Never validates passwords directly.

---

# Logging Security

Log:

- Authentication failures
- Authorization failures
- Permission denials
- Suspicious activity
- Security exceptions
- Administrative actions

Never log:

- Passwords
- JWT tokens
- Refresh tokens
- API keys
- Database credentials
- Personal secrets

---

# Background Jobs

Background jobs execute using service credentials.

They do not execute under an end-user JWT.

Background jobs must:

- Authenticate securely.
- Operate with the minimum required permissions.
- Respect tenant isolation where applicable.
- Produce audit logs.

---

# Administrative Access

Administrative users are authenticated like all other users.

Administrative capabilities are granted through application roles.

Administrative access must never bypass authentication.

Any elevated permissions must be explicitly authorized and audited.

---

# Error Handling

Security-related errors must:

- Return appropriate HTTP status codes.
- Avoid exposing internal implementation details.
- Log sufficient diagnostic information for administrators.

Examples:

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found (where appropriate)
- 422 Validation Error

---

# Audit Principles

The platform records critical security events, including:

- User login
- Logout
- Password reset
- Failed authentication
- Permission changes
- Administrative actions
- Sensitive data modifications

Audit records must be immutable.

---

# Security Testing

The backend must be tested for:

- Authentication
- Authorization
- Tenant isolation
- RLS enforcement
- SQL injection protection
- Input validation
- Broken access control
- Session handling

Security testing is required before every production release.

---

# Security Responsibilities

| Layer | Responsibility |
|---------|---------------|
| Supabase Auth | User authentication |
| FastAPI API | JWT validation |
| Service Layer | Authorization and business permissions |
| Repository Layer | Secure database access |
| SQLAlchemy | Session management |
| PostgreSQL RLS | Tenant isolation |
| Database | Data integrity |

---

# Summary

The backend security architecture is based on:

- Supabase Auth for authentication
- FastAPI for JWT validation
- Per-request tenant context initialization
- SQLAlchemy session isolation
- PostgreSQL Row-Level Security (RLS)
- Defense in depth
- Least privilege
- Secure API design
- Comprehensive audit logging
- Strong multi-tenant isolation

This document serves as the authoritative reference for backend security implementation across the platform.