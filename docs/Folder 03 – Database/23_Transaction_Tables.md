# Transaction Tables

## Purpose

This document defines the transactional tables used by the Food Inventory Leakage Platform.

Transaction tables capture day-to-day business activities performed by users and business processes. They provide the official operational record for purchasing, inventory movement, production, stock reconciliation, and leakage detection.

Unlike Master Tables, transaction tables grow continuously and preserve the complete business history.

---

# Design Principles

Transaction tables should:

- Record every business event.
- Preserve historical records.
- Maintain complete auditability.
- Support multi-tenant architecture.
- Maintain referential integrity.
- Support reporting and analytics.
- Never overwrite completed transactions.
- Support future scalability.

Inventory Transactions are the official source of truth for inventory movement.

---

# Purchasing Module

## Purchase Order

Represents a purchase order issued to a supplier.

Example fields:

- purchase_order_id
- supplier_id
- warehouse_id
- order_number
- order_date
- expected_delivery_date
- status

---

## Purchase Order Item

Stores individual products included in a Purchase Order.

Example fields:

- purchase_order_item_id
- purchase_order_id
- product_id
- ordered_quantity
- unit_price
- total_amount

---

## Goods Receipt

Represents inventory received from a supplier.

Example fields:

- goods_receipt_id
- purchase_order_id
- warehouse_id
- receipt_number
- receipt_date
- status

---

## Goods Receipt Item

Stores products received against a Goods Receipt.

Example fields:

- goods_receipt_item_id
- goods_receipt_id
- product_id
- received_quantity
- accepted_quantity
- rejected_quantity

Approved Goods Receipts automatically generate Inventory Transactions.

---

# Inventory Module

## Inventory Transaction

The Inventory Transaction table is the official inventory ledger.

Every stock movement creates an Inventory Transaction.

Transaction types include:

- Purchase Receipt
- Production Consumption
- Production Output
- Sales Dispatch
- Stock Transfer
- Stock Adjustment
- Customer Return
- Supplier Return
- Production Waste
- Inventory Leakage
- Physical Count Adjustment

Example fields:

- inventory_transaction_id
- warehouse_id
- product_id
- transaction_type
- quantity
- transaction_date
- reference_number

---

## Stock Balance

The Stock Balance table maintains the current inventory quantity for each product in each warehouse.

Typical fields include:

- stock_balance_id
- warehouse_id
- product_id
- current_quantity
- reserved_quantity
- available_quantity
- last_updated

Stock Balance is a derived table maintained from Inventory Transactions.

Inventory Transactions remain the authoritative source of truth.

If inconsistencies occur, Stock Balance can be rebuilt from Inventory Transactions.

---

## Stock Adjustment

Stores manual inventory corrections.

Examples:

- Inventory correction
- Damage adjustment
- Expired stock
- Missing stock
- Administrative adjustment

Every approved adjustment generates an Inventory Transaction.

---

## Stock Transfer

Represents movement of inventory between warehouses.

Example fields:

- stock_transfer_id
- source_warehouse_id
- destination_warehouse_id
- transfer_date
- status

Each completed transfer creates Inventory Transactions for both warehouses.

---

## Physical Stock Count

Stores results of physical inventory counting.

Physical counts are periodically performed to verify inventory accuracy.

---

## Stock Variance

Stores differences between:

- Physical Stock Count
- System Stock Balance

Typical fields include:

- stock_variance_id
- warehouse_id
- product_id
- system_quantity
- physical_quantity
- variance_quantity
- variance_value

Significant variances may generate Leakage Events.

---

# Production Module

## Production Order

Represents a manufacturing or production batch.

Example fields:

- production_order_id
- finished_product_id
- planned_quantity
- production_date
- status

Production Orders use the Bill of Material (BOM) to determine expected raw material consumption.

---

## Production Consumption

Records actual raw materials consumed during production.

Example fields:

- production_consumption_id
- production_order_id
- product_id
- consumed_quantity

Actual consumption is compared with the BOM for yield analysis.

---

## Production Output

Records finished goods produced.

Example fields:

- production_output_id
- production_order_id
- finished_product_id
- produced_quantity

Finished goods increase inventory through Inventory Transactions.

---

## Production Waste

Stores production losses.

Examples:

- Spoilage
- Scrap
- Rework
- Process Loss
- Quality Rejection

Production Waste contributes to leakage and efficiency analysis.

---

# Sales Module

## Sales Order

Represents customer sales.

Example fields:

- sales_order_id
- customer_id
- order_date
- status

---

## Sales Order Item

Stores products sold.

---

## Dispatch

Represents shipment of finished goods to customers.

Approved dispatches automatically create Inventory Transactions.

---

# Alerts & Notifications

## Alert Queue

Stores system-generated alerts.

Examples:

- Inventory Variance
- Negative Stock
- Excessive Waste
- Leakage Detected
- Low Stock
- Overstock

---

## Email Queue

Stores pending notification emails.

Email delivery is handled by the notification service.

---

# Common Columns

Every transaction table should include:

- organization_id
- created_at
- updated_at
- created_by
- updated_by

Where appropriate:

- deleted_at
- deleted_by
- status
- remarks
- reference_number

---

# Transaction Relationships

Purchasing Flow

Supplier

↓

Purchase Order

↓

Goods Receipt

↓

Inventory Transaction

↓

Stock Balance

---

Inventory Flow

Inventory Transaction

↓

Stock Balance

↓

Physical Stock Count

↓

Stock Variance

↓

Leakage Event

---

Production Flow

Bill of Material

↓

Production Order

↓

Production Consumption

↓

Production Output

↓

Production Waste

↓

Inventory Transaction

↓

Stock Balance

---

Sales Flow

Sales Order

↓

Dispatch

↓

Inventory Transaction

↓

Stock Balance

---

# Business Rules

- Every inventory movement must create an Inventory Transaction.
- Inventory Transactions are immutable after posting.
- Corrections must be performed using Stock Adjustments.
- Stock Balance must always reflect Inventory Transactions.
- Physical Stock Counts generate Stock Variance records.
- Production Orders use the Bill of Material to calculate expected material consumption.
- Production Consumption is compared against the Bill of Material for yield and leakage analysis.
- Significant inventory or production variances may generate Leakage Events and Alerts.

---

# Guiding Principle

Transaction tables represent the operational history of the Food Inventory Leakage Platform.

They must remain:

- Accurate
- Auditable
- Consistent
- Multi-tenant
- Scalable
- High-performance

All reporting, analytics, leakage detection, and dashboards ultimately derive from the transactional data stored in these tables.