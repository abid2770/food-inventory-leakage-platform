# Transaction API

## Purpose

This document defines the REST API endpoints for managing transactional business operations within the Food Inventory Leakage Platform.

Transaction APIs capture and process day-to-day business activities including purchasing, inventory movement, production, sales, and stock reconciliation.

These APIs implement business rules through FastAPI while ensuring data integrity, auditability, and multi-tenant security.

---

# Design Principles

Transaction APIs should be:

- RESTful
- Stateless
- Secure
- Multi-tenant
- Auditable
- Scalable
- Consistent
- Business-rule driven

Every transaction must execute within the authenticated Organization.

---

# API Base URL

All endpoints begin with:

```text
/api/v1/
```

---

# Authentication

All Transaction APIs require:

- Valid JWT Access Token
- Active User
- Active Organization
- Required Role
- Required Permission

Unauthorized requests must be rejected.

---

# Purchasing APIs

## Purchase Order

Purpose

Create and manage supplier purchase orders.

Endpoints

```text
GET    /purchase-orders

GET    /purchase-orders/{id}

POST   /purchase-orders

PUT    /purchase-orders/{id}

PATCH  /purchase-orders/{id}

DELETE /purchase-orders/{id}
```

Typical Operations

- Create Purchase Order
- Update Purchase Order
- Submit Purchase Order
- Cancel Purchase Order
- View Purchase Orders

---

## Purchase Order Items

Purpose

Manage products within a purchase order.

Endpoints

```text
GET    /purchase-orders/{id}/items

POST   /purchase-orders/{id}/items

PUT    /purchase-orders/{id}/items/{item_id}

DELETE /purchase-orders/{id}/items/{item_id}
```

---

## Goods Receipt

Purpose

Receive inventory from suppliers.

Endpoints

```text
GET    /goods-receipts

GET    /goods-receipts/{id}

POST   /goods-receipts

PUT    /goods-receipts/{id}

PATCH  /goods-receipts/{id}
```

Business Rules

- Goods Receipt must reference an approved Purchase Order.
- Approved Goods Receipt automatically creates Inventory Transactions.
- Duplicate Goods Receipts are not allowed.

---

# Inventory APIs

## Inventory Transactions

Purpose

Retrieve inventory movement history.

Endpoints

```text
GET /inventory-transactions

GET /inventory-transactions/{id}
```

Inventory Transactions are system-generated and cannot be edited after posting.

---

## Stock Balance

Purpose

Retrieve current inventory balances.

Endpoints

```text
GET /stock-balances

GET /stock-balances/{product_id}

GET /stock-balances/{warehouse_id}
```

Stock Balance is derived from Inventory Transactions.

---

## Stock Adjustment

Purpose

Record inventory corrections.

Endpoints

```text
GET    /stock-adjustments

GET    /stock-adjustments/{id}

POST   /stock-adjustments

PUT    /stock-adjustments/{id}

PATCH  /stock-adjustments/{id}
```

Business Rules

- Adjustment reason is mandatory.
- Approval may be required based on business policy.
- Approved adjustments generate Inventory Transactions.

---

## Stock Transfer

Purpose

Transfer inventory between warehouses.

Endpoints

```text
GET    /stock-transfers

GET    /stock-transfers/{id}

POST   /stock-transfers

PUT    /stock-transfers/{id}

PATCH  /stock-transfers/{id}
```

Business Rules

- Source and destination warehouses must differ.
- Stock availability must be validated.
- Completed transfers generate Inventory Transactions.

---

## Physical Stock Count

Purpose

Record physical inventory counts.

Endpoints

```text
GET    /stock-counts

GET    /stock-counts/{id}

POST   /stock-counts

PUT    /stock-counts/{id}
```

Business Rules

- Counts are compared with Stock Balance.
- Variances generate Stock Variance records.

---

## Stock Variance

Purpose

Review inventory variances.

Endpoints

```text
GET /stock-variances

GET /stock-variances/{id}
```

Stock Variance records are system-generated.

---

# Production APIs

## Production Order

Purpose

Manage manufacturing batches.

Endpoints

```text
GET    /production-orders

GET    /production-orders/{id}

POST   /production-orders

PUT    /production-orders/{id}

PATCH  /production-orders/{id}
```

Business Rules

- Production Orders must reference a valid Bill of Material (BOM).
- Planned quantities must be greater than zero.

---

## Production Consumption

Purpose

Record raw material consumption.

Endpoints

```text
GET    /production-consumption

GET    /production-consumption/{id}

POST   /production-consumption
```

Business Rules

- Consumption is validated against available stock.
- Inventory Transactions are generated automatically.

---

## Production Output

Purpose

Record finished goods produced.

Endpoints

```text
GET    /production-output

GET    /production-output/{id}

POST   /production-output
```

Business Rules

- Output increases finished goods inventory.
- Inventory Transactions are generated automatically.

---

## Production Waste

Purpose

Record production losses.

Endpoints

```text
GET    /production-waste

GET    /production-waste/{id}

POST   /production-waste
```

Business Rules

- Waste reason is mandatory.
- Waste contributes to yield and leakage analysis.

---

# Sales APIs

## Sales Order

Purpose

Manage customer sales.

Endpoints

```text
GET    /sales-orders

GET    /sales-orders/{id}

POST   /sales-orders

PUT    /sales-orders/{id}

PATCH  /sales-orders/{id}
```

---

## Dispatch

Purpose

Dispatch finished goods to customers.

Endpoints

```text
GET    /dispatches

GET    /dispatches/{id}

POST   /dispatches
```

Business Rules

- Dispatch validates stock availability.
- Completed dispatch generates Inventory Transactions.

---

# Transaction Workflow

Purchasing

```text
Purchase Order
      │
      ▼
Goods Receipt
      │
      ▼
Inventory Transaction
      │
      ▼
Stock Balance
```

Inventory

```text
Inventory Transaction
      │
      ▼
Stock Balance
      │
      ▼
Physical Stock Count
      │
      ▼
Stock Variance
```

Production

```text
Bill of Material
      │
      ▼
Production Order
      │
      ▼
Production Consumption
      │
      ▼
Production Output
      │
      ▼
Production Waste
      │
      ▼
Inventory Transaction
```

Sales

```text
Sales Order
      │
      ▼
Dispatch
      │
      ▼
Inventory Transaction
```

---

# Validation Rules

Transaction APIs must validate:

- Authentication
- Organization ownership
- User permissions
- Required fields
- Business rules
- Product availability
- Warehouse validity
- Duplicate transactions
- Reference documents
- Inventory availability

Validation failures return HTTP 422.

---

# Audit Requirements

Every transaction should record:

- Organization ID
- User ID
- Transaction Date
- Created At
- Updated At
- Reference Number
- Operation Type

Completed transactions remain fully auditable.

---

# Security

Every transaction request must:

- Validate JWT
- Verify Organization
- Verify Role
- Verify Permission
- Enforce Row Level Security
- Validate ownership of referenced records

Cross-organization access is prohibited.

---

# Error Handling

Transaction APIs should return standardized errors for:

- Invalid Request
- Validation Failure
- Unauthorized
- Forbidden
- Resource Not Found
- Duplicate Transaction
- Insufficient Stock
- Invalid Business Rule
- Internal Server Error

Internal implementation details must never be exposed.

---

# Future Enhancements

Future transaction APIs may support:

- Bulk Transactions
- Batch Processing
- Workflow Approvals
- Barcode Scanning
- QR Code Operations
- Offline Mobile Synchronization
- ERP Integration
- IoT Device Integration

These enhancements should extend the existing API structure while preserving backward compatibility.

---

# Guiding Principle

Transaction APIs represent the operational backbone of the Food Inventory Leakage Platform.

Every endpoint should be:

- Secure
- Reliable
- Auditable
- Multi-tenant
- Business-rule driven
- Easy to test
- Easy to maintain
- Scalable

Transaction APIs ensure that every inventory movement, production activity, purchasing event, and sales operation is processed consistently while preserving data integrity, tenant isolation, and complete business traceability.