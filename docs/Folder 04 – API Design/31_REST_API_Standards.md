# REST API Standards

## Purpose

This document defines the REST API standards for the Food Inventory Leakage Platform.

These standards ensure that every API endpoint follows a consistent structure, naming convention, request format, response format, and security model.

All APIs developed for the platform must comply with these standards.

---

# REST Design Principles

The platform follows REST (Representational State Transfer) principles.

Every API should be:

- Resource-oriented
- Stateless
- Predictable
- Consistent
- Secure
- Versioned
- Easy to consume
- Easy to maintain

---

# Base URL

All API endpoints should begin with a version identifier.

Example:

```text
/api/v1/
```

Examples:

```text
/api/v1/products
/api/v1/warehouses
/api/v1/purchase-orders
/api/v1/leakage-events
```

---

# Resource Naming

Resources should represent business entities.

Use plural nouns.

Examples:

```text
/products
/categories
/warehouses
/suppliers
/customers
/purchase-orders
/inventory-transactions
/stock-adjustments
/production-orders
/leakage-events
```

Avoid verbs in endpoint names.

Incorrect:

```text
/createProduct
/getProducts
/updateWarehouse
```

Correct:

```text
POST /products
GET /products
PUT /warehouses/{id}
```

---

# HTTP Methods

Use standard HTTP methods consistently.

| Method | Purpose |
|----------|----------|
| GET | Retrieve data |
| POST | Create a resource |
| PUT | Replace an existing resource |
| PATCH | Partially update a resource |
| DELETE | Soft delete a resource |

DELETE should perform a soft delete unless explicitly approved for system administration.

---

# Standard CRUD Pattern

Example:

```text
GET    /products
GET    /products/{id}

POST   /products

PUT    /products/{id}

PATCH  /products/{id}

DELETE /products/{id}
```

---

# URL Structure

URLs should be simple and hierarchical.

Example:

```text
/products

/products/{product_id}

/warehouses/{warehouse_id}

/purchase-orders/{purchase_order_id}

/production-orders/{production_order_id}
```

Nested resources should be used only when they clearly represent ownership.

Example:

```text
/purchase-orders/{id}/items
```

Avoid excessive nesting.

---

# Query Parameters

Filtering should use query parameters.

Examples:

```text
/products?category=RawMaterial

/products?status=Active

/products?warehouse=Main

/products?search=Sugar
```

Multiple filters may be combined.

Example:

```text
/products?category=RawMaterial&status=Active
```

---

# Pagination

Large result sets should always support pagination.

Standard parameters:

```text
?page=1

?page_size=25
```

Example:

```text
/products?page=2&page_size=50
```

Responses should include pagination metadata.

---

# Sorting

Sorting should use a standard parameter.

Example:

```text
?sort=product_name

?sort=-created_at
```

"-" indicates descending order.

---

# Searching

Search should use a common parameter.

Example:

```text
?search=Milk
```

Search should be case-insensitive where practical.

---

# Request Headers

Typical headers include:

```text
Authorization: Bearer <JWT>

Content-Type: application/json

Accept: application/json
```

Protected endpoints require a valid JWT.

---

# Request Body

Requests should use JSON.

Example:

```json
{
  "product_name": "Sugar",
  "category_id": 10,
  "unit_id": 2
}
```

File upload endpoints may use `multipart/form-data`.

---

# Response Format

Every API should return a consistent response structure.

Successful response:

```json
{
  "success": true,
  "message": "Request completed successfully.",
  "data": {}
}
```

List response:

```json
{
  "success": true,
  "data": [],
  "pagination": {}
}
```

Error response:

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": []
}
```

---

# HTTP Status Codes

Use standard HTTP status codes.

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

Status codes should accurately reflect the outcome of the request.

---

# Validation

Every request should be validated before processing.

Validation includes:

- Required fields
- Data types
- Length limits
- Numeric ranges
- Date formats
- Business rules
- Organization ownership
- Foreign key references

Validation failures should return HTTP 422.

---

# Idempotency

GET operations must never modify data.

PUT operations should be idempotent.

POST operations create new resources.

PATCH updates only specified fields.

DELETE performs a soft delete.

---

# Date and Time Format

All timestamps should use UTC.

ISO 8601 format:

```text
2026-07-21T10:30:00Z
```

The frontend is responsible for displaying dates in the user's local timezone.

---

# API Security

Every protected request must:

- Authenticate the user
- Validate the JWT
- Verify Organization access
- Verify Role permissions
- Enforce Row Level Security (RLS)

The API must never expose data belonging to another Organization.

---

# Performance Standards

APIs should:

- Return only required fields
- Support pagination
- Avoid unnecessary joins
- Use indexed queries
- Minimize response size

Heavy analytical operations should use pre-calculated analytics tables where appropriate.

---

# Error Messages

Error messages should be:

- Clear
- Consistent
- Actionable

Avoid exposing:

- SQL statements
- Stack traces
- Internal implementation details
- Sensitive information

---

# API Documentation

Every endpoint should document:

- Purpose
- URL
- HTTP Method
- Authentication requirement
- Request parameters
- Request body
- Response format
- Status codes
- Validation rules
- Example requests
- Example responses

FastAPI OpenAPI documentation should remain synchronized with implementation.

---

# Backward Compatibility

Once an API version is released:

- Breaking changes should not be introduced.
- New functionality should be added without affecting existing clients.
- Major breaking changes require a new API version.

---

# Future Standards

Future enhancements may include:

- Rate limiting
- API keys for third-party integrations
- Webhooks
- GraphQL gateway
- Bulk operations
- Batch processing
- API usage analytics

These enhancements should preserve existing REST standards.

---

# Guiding Principle

REST APIs are the public contract of the Food Inventory Leakage Platform.

Every endpoint should be:

- Consistent
- Predictable
- Secure
- Stateless
- Versioned
- Well-documented
- Easy to consume
- Easy to maintain

A consistent REST API enables reliable frontend development, simplified testing, and future integration with external systems while preserving the platform's MVP-first and API-first philosophy.