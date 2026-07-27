# File Import API

## Purpose

This document defines the REST API endpoints, validation rules, processing workflow, and security requirements for importing Excel and CSV files into the Food Inventory Leakage Platform.

The MVP follows an **Excel-First** approach, enabling customers to upload existing business data without requiring ERP integration.

The File Import API provides secure, reliable, and auditable data import capabilities while ensuring data quality and tenant isolation.

---

# Design Principles

The File Import API should be:

- Secure
- Reliable
- User-friendly
- Multi-tenant
- Scalable
- Auditable
- Resumable where appropriate
- Easy to maintain

All imports must be validated before data is committed to the database.

---

# API Base URL

All endpoints begin with:

```text
/api/v1/
```

---

# Authentication

All File Import APIs require:

- Valid JWT Access Token
- Active User
- Active Organization
- Required Permission

Only authorized users may upload files.

---

# Supported File Formats

The MVP supports:

- Microsoft Excel (.xlsx)
- Comma Separated Values (.csv)

Unsupported formats must be rejected.

Examples:

```text
✔ inventory.xlsx

✔ products.csv

✘ products.xls

✘ products.pdf

✘ products.zip
```

---

# Supported Import Modules

The MVP supports importing:

- Products
- Categories
- Units
- Warehouses
- Suppliers
- Customers
- Bill of Materials (BOM)
- Opening Stock
- Purchase Orders
- Goods Receipts
- Inventory Transactions
- Physical Stock Counts

Additional import modules may be introduced in future releases.

---

# API Endpoints

## Upload File

```text
POST /imports/upload
```

Uploads an Excel or CSV file for validation.

---

## Validate File

```text
POST /imports/{import_id}/validate
```

Performs structural and business validation without saving data.

---

## Preview Import

```text
GET /imports/{import_id}/preview
```

Returns a preview of validated records before import.

---

## Execute Import

```text
POST /imports/{import_id}/execute
```

Commits validated records to the database.

---

## Import Status

```text
GET /imports/{import_id}
```

Returns:

- Status
- Progress
- Record Counts
- Errors
- Warnings
- Processing Time

---

## Import History

```text
GET /imports
```

Returns previous imports for the authenticated Organization.

---

## Download Error Report

```text
GET /imports/{import_id}/errors
```

Downloads validation errors for correction.

---

# File Validation

Every uploaded file must be validated before import.

Validation includes:

- File format
- File size
- Required columns
- Column names
- Duplicate columns
- Empty files
- Invalid data types
- Invalid dates
- Invalid numeric values
- Invalid foreign keys
- Duplicate business codes
- Missing required fields

Files failing validation must not be imported.

---

# Business Validation

Business validation includes:

- Organization ownership
- Existing master data
- Product existence
- Warehouse existence
- Supplier existence
- Unit existence
- Category existence
- Duplicate products
- Duplicate purchase orders
- BOM consistency
- Inventory availability (where applicable)

Business validation occurs after structural validation.

---

# Import Workflow

```text
User Uploads File
        │
        ▼
File Stored Securely
        │
        ▼
Structure Validation
        │
        ▼
Business Validation
        │
        ▼
Preview Generated
        │
        ▼
User Confirms Import
        │
        ▼
Database Transaction
        │
        ▼
Commit or Rollback
        │
        ▼
Import History Updated
```

---

# Import Modes

The platform supports:

## Insert Only

Creates new records only.

Existing records are ignored or reported.

---

## Update Existing

Updates matching records based on business keys.

---

## Upsert

Creates new records and updates existing records.

The selected mode should be specified by the client where supported.

---

# Database Transactions

Imports should execute inside database transactions.

If an unrecoverable error occurs:

- Roll back the transaction
- Preserve existing data
- Record the failure

Partial imports should be avoided unless explicitly supported.

---

# Import History

Every import should record:

- Import ID
- Organization ID
- Module
- File Name
- File Type
- Uploaded By
- Upload Time
- Import Time
- Status
- Total Records
- Successful Records
- Failed Records
- Warning Count
- Error Count
- Processing Duration

Import history supports auditing and troubleshooting.

---

# Error Reporting

Validation errors should include:

- Row Number
- Column Name
- Invalid Value
- Error Description
- Suggested Correction

Example:

```text
Row 15

Column: Product Code

Value: P-100

Error:

Duplicate Product Code
```

Errors should help users correct data quickly.

---

# Security

Every upload must:

- Validate JWT
- Verify Organization
- Verify Permissions
- Scan file metadata
- Restrict supported formats
- Restrict file size
- Reject executable content

Uploaded files must remain isolated between Organizations.

---

# Performance Guidelines

The File Import API should:

- Process large files efficiently
- Stream files where appropriate
- Minimize memory usage
- Batch database operations
- Return progress for long-running imports

Very large imports may be processed asynchronously in future releases.

---

# Error Handling

Standard responses include:

- Invalid File
- Unsupported Format
- Validation Failure
- Duplicate Data
- Permission Denied
- Import Failed
- Internal Server Error

Internal implementation details must never be exposed.

---

# Future Enhancements

Future improvements may include:

- Drag-and-Drop Upload
- Background Processing
- Import Templates
- Import Scheduling
- Import Rollback
- Duplicate Detection
- Intelligent Column Mapping
- OCR-Based Import
- ERP Data Import
- API-Based Bulk Import

These enhancements should preserve compatibility with the MVP import architecture.

---

# Guiding Principle

The File Import API is the primary onboarding mechanism for customer data in the MVP.

Every import should be:

- Secure
- Accurate
- Auditable
- Predictable
- Multi-tenant
- Easy to use
- Easy to troubleshoot

Reliable file imports enable organizations to adopt the platform quickly while preserving data quality and supporting the platform's Excel-first, cloud-native, and MVP-first philosophy.