# Master Data API

## Purpose

This document defines the REST API endpoints for managing master data within the Food Inventory Leakage Platform.

Master Data APIs provide Create, Read, Update, and Deactivate (CRUD) operations for business entities that are used throughout the platform.

These APIs support secure, multi-tenant access and follow the standards defined in:

- API Principles
- REST API Standards
- Authentication & Authorization
- Database Architecture

---

# Design Principles

Master Data APIs should be:

- RESTful
- Stateless
- Versioned
- Secure
- Multi-tenant
- Consistent
- Well documented
- Easy to maintain

Every request must execute within the authenticated Organization.

---

# API Base URL

All endpoints begin with:

```text
/api/v1/
```

---

# Authentication

All Master Data APIs require:

- Valid JWT Access Token
- Authenticated User
- Active Account
- Valid Organization
- Required Permission

Unauthorized requests must be rejected.

---

# Organization API

Purpose

Manage organization profile information.

Endpoints

```text
GET    /organizations/me

PUT    /organizations/me
```

Permissions

- Organization Owner
- System Administrator

---

# User API

Purpose

Manage application users.

Endpoints

```text
GET    /users

GET    /users/{id}

POST   /users

PUT    /users/{id}

PATCH  /users/{id}

DELETE /users/{id}
```

Typical Operations

- Create User
- Update User
- Activate User
- Deactivate User
- View Users

---

# Role API

Purpose

Manage application roles.

Endpoints

```text
GET    /roles

GET    /roles/{id}

POST   /roles

PUT    /roles/{id}

DELETE /roles/{id}
```

Roles define business responsibilities.

---

# Permission API

Purpose

Manage system permissions.

Endpoints

```text
GET /permissions
```

Permissions are generally managed by administrators and referenced by Roles.

---

# Category API

Purpose

Manage product categories.

Endpoints

```text
GET    /categories

GET    /categories/{id}

POST   /categories

PUT    /categories/{id}

DELETE /categories/{id}
```

Example Categories

- Raw Material
- Packaging Material
- Finished Goods
- Consumables

---

# Unit API

Purpose

Manage units of measure.

Endpoints

```text
GET    /units

GET    /units/{id}

POST   /units

PUT    /units/{id}

DELETE /units/{id}
```

Example Units

- Kilogram
- Gram
- Liter
- Piece
- Carton

---

# Product API

Purpose

Manage products.

Endpoints

```text
GET    /products

GET    /products/{id}

POST   /products

PUT    /products/{id}

PATCH  /products/{id}

DELETE /products/{id}
```

Products may represent:

- Raw Materials
- Finished Goods
- Packaging
- Consumables

---

# Bill of Material (BOM) API

Purpose

Manage product recipes and production formulations.

Endpoints

```text
GET    /bill-of-materials

GET    /bill-of-materials/{id}

POST   /bill-of-materials

PUT    /bill-of-materials/{id}

DELETE /bill-of-materials/{id}
```

The BOM defines:

- Finished Product
- Raw Materials
- Standard Quantities
- Units of Measure

BOM data is used for:

- Production Planning
- Yield Analysis
- Leakage Detection

---

# Warehouse API

Purpose

Manage warehouses.

Endpoints

```text
GET    /warehouses

GET    /warehouses/{id}

POST   /warehouses

PUT    /warehouses/{id}

DELETE /warehouses/{id}
```

---

# Supplier API

Purpose

Manage suppliers.

Endpoints

```text
GET    /suppliers

GET    /suppliers/{id}

POST   /suppliers

PUT    /suppliers/{id}

DELETE /suppliers/{id}
```

---

# Customer API

Purpose

Manage customers.

Endpoints

```text
GET    /customers

GET    /customers/{id}

POST   /customers

PUT    /customers/{id}

DELETE /customers/{id}
```

---

# Reason API

Purpose

Manage standardized operational reasons.

Endpoints

```text
GET    /reasons

GET    /reasons/{id}

POST   /reasons

PUT    /reasons/{id}

DELETE /reasons/{id}
```

Examples

- Damage
- Waste
- Leakage
- Transfer
- Adjustment
- Expired Stock

---

# Common API Behaviour

Every endpoint should support:

- Pagination
- Searching
- Sorting
- Filtering

Example

```text
GET /products?page=1&page_size=25

GET /products?search=Sugar

GET /products?status=Active

GET /products?sort=product_name
```

---

# Validation Rules

Every request should validate:

- Required fields
- Data types
- Business rules
- Duplicate business codes
- Organization ownership
- Foreign key references

Validation failures return HTTP 422.

---

# Security

Every request must:

- Validate JWT
- Verify Organization
- Verify User Status
- Verify Role
- Verify Permission
- Enforce Row Level Security

Master Data must never be shared across Organizations.

---

# Soft Delete Policy

Business master data should use soft deletes.

Deletion should:

- Mark records as inactive
- Preserve audit history
- Prevent accidental data loss

Physical deletion should be restricted to administrative maintenance operations.

---

# Audit Requirements

Master Data changes should record:

- Organization
- User
- Timestamp
- Operation
- Previous Value
- New Value

Audit logs support traceability and compliance.

---

# Error Handling

Errors should follow the standard API response format.

Examples include:

- Invalid Request
- Unauthorized
- Forbidden
- Validation Failed
- Duplicate Record
- Resource Not Found

Implementation details should never be exposed.

---

# Future Enhancements

Future APIs may include:

- Bulk Import
- Bulk Update
- Bulk Deactivate
- Product Images
- Barcode Management
- QR Code Support
- Product Variants
- Approval Workflow

These enhancements should extend the existing API structure without breaking backward compatibility.

---

# Guiding Principle

Master Data APIs provide the foundation for every operational process within the Food Inventory Leakage Platform.

Every endpoint should be:

- Secure
- Consistent
- RESTful
- Multi-tenant
- Well documented
- Easy to test
- Easy to maintain

Reliable Master Data APIs ensure high-quality business data that supports purchasing, inventory, production, analytics, and leakage detection across the platform.