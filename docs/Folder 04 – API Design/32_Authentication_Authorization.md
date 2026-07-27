# Authentication & Authorization

## Purpose

This document defines the authentication and authorization architecture for the Food Inventory Leakage Platform.

The platform uses Supabase Authentication for user identity management and FastAPI for business authorization.

The objective is to ensure that every authenticated user can access only the resources they are permitted to use within their own organization.

---

# Security Architecture

The platform follows a layered security model.

```text
User
   │
   ▼
Supabase Authentication
   │
   ▼
JWT Access Token
   │
   ▼
FastAPI Authentication
   │
   ▼
Role & Permission Validation
   │
   ▼
Organization Validation
   │
   ▼
Supabase PostgreSQL (Row Level Security)
```

Each layer provides an additional level of protection.

---

# Authentication Principles

Authentication answers the question:

**"Who is the user?"**

Authentication is handled exclusively by Supabase Auth.

The application does not manage passwords directly.

---

# Authorization Principles

Authorization answers the question:

**"What is the user allowed to do?"**

Authorization is handled by FastAPI using:

- Organization membership
- User role
- Assigned permissions
- Business rules

Authentication alone does not grant access to business operations.

---

# Identity Provider

Supabase Auth is the official identity provider.

Supported authentication methods for the MVP:

- Email and Password
- Password Reset
- Email Verification
- Session Management

Future authentication methods may include:

- Google Sign-In
- Microsoft Sign-In
- SSO
- Multi-Factor Authentication (MFA)

---

# JWT Authentication

After successful login, Supabase issues a JWT Access Token.

Every protected API request must include:

```text
Authorization: Bearer <JWT Token>
```

FastAPI validates the JWT before processing any request.

Requests without a valid token must be rejected.

---

# User Identity

Each authenticated user has a unique identity.

Typical identity information includes:

- User ID
- Email Address
- Organization ID
- Role
- Account Status

This identity is available to FastAPI after JWT validation.

---

# Organization (Tenant) Context

The platform is multi-tenant.

Each user belongs to exactly one Organization.

The Organization represents the Tenant.

Every request is executed within the authenticated Organization context.

A user must never access data belonging to another Organization.

---

# Tenant Isolation

Tenant isolation is enforced through multiple layers.

FastAPI validates:

- User identity
- Organization membership
- Requested resource ownership

Supabase PostgreSQL enforces Row Level Security (RLS).

Both layers work together to protect tenant data.

---

# Role-Based Access Control (RBAC)

Authorization is based on Roles.

Typical roles include:

- Owner
- Factory Manager
- Production Manager
- Warehouse Manager
- Inventory Manager
- Store Officer
- Accounts Manager
- Internal Auditor

Each role is assigned a predefined set of permissions.

---

# Permissions

Permissions define specific business capabilities.

Examples include:

- View Dashboard
- Manage Products
- Manage Warehouses
- Create Purchase Orders
- Receive Goods
- Manage Inventory
- Perform Stock Count
- Approve Stock Adjustment
- Manage Production
- View Reports
- Export Reports
- Manage Users

FastAPI validates permissions before executing business operations.

---

# Authorization Flow

Every protected request follows this sequence:

```text
Receive Request
        │
        ▼
Validate JWT
        │
        ▼
Identify User
        │
        ▼
Load Organization
        │
        ▼
Load Role
        │
        ▼
Validate Permission
        │
        ▼
Validate Resource Ownership
        │
        ▼
Execute Business Logic
        │
        ▼
Return Response
```

If any validation fails, access is denied.

---

# Row Level Security (RLS)

Supabase PostgreSQL enforces Row Level Security.

Every business table contains:

- organization_id

RLS ensures that queries automatically return data only for the authenticated Organization.

FastAPI must never bypass RLS for normal business operations.

---

# Administrative Access

Administrative operations should follow the principle of least privilege.

Administrative capabilities may include:

- Organization Management
- User Management
- Role Management
- Permission Management
- System Configuration

Only authorized administrators should perform these actions.

---

# Public Endpoints

Only a small number of endpoints should be publicly accessible.

Examples include:

- Login
- Password Reset
- Email Verification
- Health Check

All business APIs require authentication.

---

# Session Management

Supabase manages user sessions.

FastAPI remains stateless.

The backend does not maintain server-side user sessions.

Expired or invalid tokens must be rejected.

---

# Account Status

Only active users may access the system.

Possible account states include:

- Active
- Inactive
- Locked
- Suspended

FastAPI should validate account status before allowing business operations.

---

# Password Management

Passwords are managed entirely by Supabase Auth.

The application should never:

- Store passwords
- Encrypt passwords manually
- Reset passwords directly

Password policies are managed through Supabase configuration.

---

# Audit Requirements

Authentication and authorization events should be auditable.

Important events include:

- Login
- Logout
- Password Reset
- Failed Login
- Permission Denied
- Role Changes
- User Creation
- User Deactivation

Audit information supports security monitoring and troubleshooting.

---

# Security Best Practices

The platform should follow these practices:

- HTTPS in production
- JWT authentication
- Role-based authorization
- Least privilege access
- Row Level Security
- Input validation
- Secure error messages
- Audit logging

Sensitive information must never be exposed to unauthorized users.

---

# Future Enhancements

Future security enhancements may include:

- Multi-Factor Authentication (MFA)
- Single Sign-On (SSO)
- Google Authentication
- Microsoft Authentication
- API Keys
- Device Management
- Login Notifications
- Security Dashboard
- Conditional Access Policies

These features should integrate with the existing authentication architecture without requiring major redesign.

---

# Guiding Principle

Authentication verifies identity.

Authorization verifies permissions.

FastAPI is responsible for business authorization.

Supabase Auth is responsible for identity management.

Supabase PostgreSQL is responsible for Row Level Security.

Together, these components provide a secure, scalable, and maintainable security architecture that protects every organization's data while supporting the platform's multi-tenant, API-first, and MVP-first design philosophy.