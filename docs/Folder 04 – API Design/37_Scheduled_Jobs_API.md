# Scheduled Jobs API

## Purpose

This document defines the scheduled job architecture for the Food Inventory Leakage Platform.

Scheduled Jobs automate recurring business processes that do not require direct user interaction, including analytics generation, leakage detection, dashboard refresh, email notifications, and housekeeping.

Business logic is executed exclusively by FastAPI. Scheduling services are responsible only for triggering these jobs.

---

# Design Principles

Scheduled Jobs should be:

- Reliable
- Secure
- Idempotent
- Auditable
- Scalable
- Fault Tolerant
- Easy to Monitor
- Easy to Maintain

Every scheduled job must execute within a controlled and authenticated environment.

---

# Architecture

The platform uses the following architecture:

```text
Supabase pg_cron
        │
        │
GitHub Actions (Optional)
        │
        │
External Scheduler (Optional)
        │
        ▼
FastAPI Scheduled Job Endpoint
        │
        ▼
Business Logic
        │
        ▼
Supabase PostgreSQL
        │
        ▼
Analytics Tables
```

Business calculations must never execute directly inside PostgreSQL stored procedures.

---

# Scheduling Components

The MVP uses:

- Supabase pg_cron
- GitHub Actions (where appropriate)
- FastAPI
- Supabase PostgreSQL

Future versions may support additional scheduling platforms.

---

# Authentication

Scheduled Job APIs are internal APIs.

They must never be accessible by normal application users.

Authentication should use one of the following:

- Service Account
- Internal API Key
- Secure Bearer Token

Only trusted services may invoke scheduled endpoints.

---

# Base URL

All scheduled job endpoints begin with:

```text
/api/v1/jobs/
```

---

# Analytics Refresh Job

## Purpose

Refresh analytical tables using the latest transactional data.

Endpoint

```text
POST /jobs/refresh-analytics
```

Typical Tasks

- Inventory KPI Refresh
- Operational KPI Refresh
- Dashboard Cache Refresh
- Trend Calculation
- Summary Generation

---

# Leakage Detection Job

## Purpose

Detect inventory leakage using configured business rules.

Endpoint

```text
POST /jobs/detect-leakage
```

Typical Tasks

- Inventory Variance Analysis
- Leakage Event Creation
- Estimated Loss Calculation
- Severity Classification

Results are stored in Analytics tables.

---

# Production Yield Calculation Job

## Purpose

Calculate production efficiency using Bill of Material (BOM) data.

Endpoint

```text
POST /jobs/calculate-yield
```

Typical Tasks

- Expected Consumption
- Actual Consumption
- Yield Percentage
- Waste Percentage
- Production Variance

Results are stored for reporting and dashboards.

---

# Dashboard Refresh Job

## Purpose

Refresh dashboard cache.

Endpoint

```text
POST /jobs/refresh-dashboard
```

Typical Tasks

- KPI Cache
- Dashboard Summary
- Charts
- Operational Statistics

Refreshing cached data improves dashboard performance.

---

# Alert Generation Job

## Purpose

Generate operational alerts.

Endpoint

```text
POST /jobs/generate-alerts
```

Typical Alerts

- High Leakage
- Negative Inventory
- Low Stock
- Overstock
- Production Exception
- Inventory Variance

Alerts are stored for user notification.

---

# Email Notification Job

## Purpose

Send pending email notifications.

Endpoint

```text
POST /jobs/send-emails
```

Typical Emails

- Leakage Alerts
- Import Results
- System Notifications
- Scheduled Reports

Email delivery uses the configured email provider.

---

# Cleanup Job

## Purpose

Perform housekeeping activities.

Endpoint

```text
POST /jobs/cleanup
```

Typical Tasks

- Remove Expired Files
- Archive Old Logs
- Remove Temporary Data
- Clean Dashboard Cache
- Update Job History

Cleanup jobs must never delete active business records.

---

# Import Processing Job

## Purpose

Process large asynchronous file imports.

Endpoint

```text
POST /jobs/process-imports
```

Typical Tasks

- Validate Files
- Execute Imports
- Update Import Status
- Generate Error Reports

This endpoint is primarily intended for future asynchronous imports.

---

# Job Execution Flow

```text
Scheduler
      │
      ▼
Authenticate Request
      │
      ▼
FastAPI Endpoint
      │
      ▼
Validate Request
      │
      ▼
Execute Business Logic
      │
      ▼
Update Database
      │
      ▼
Write Job Log
      │
      ▼
Return Result
```

---

# Job Status

Each execution should record:

- Job Name
- Job ID
- Start Time
- End Time
- Duration
- Status
- Records Processed
- Warnings
- Errors

Possible Status Values

- Pending
- Running
- Completed
- Failed
- Cancelled

---

# Idempotency

Scheduled jobs should be safe to retry.

Re-running the same job should not:

- Duplicate Analytics
- Duplicate Alerts
- Duplicate Emails
- Corrupt Business Data

Idempotent design improves reliability and recovery.

---

# Logging

Every scheduled job should log:

- Job ID
- Execution Time
- Organization (if applicable)
- Duration
- Success Count
- Failure Count
- Error Details
- Processing Statistics

Logs support monitoring and troubleshooting.

---

# Monitoring

The platform should monitor:

- Job Success Rate
- Failed Jobs
- Average Runtime
- Processing Volume
- Retry Count
- Queue Length (future)
- Scheduler Availability

Monitoring helps identify operational issues early.

---

# Error Handling

If a scheduled job fails:

- Log the error
- Preserve processing history
- Mark the job as Failed
- Return a standardized error response
- Allow safe retry where appropriate

Business data should remain consistent even if a job fails.

---

# Security

Scheduled job endpoints must:

- Require service authentication
- Validate requests
- Restrict public access
- Log execution
- Protect sensitive operations

Normal application users must never invoke internal scheduled job APIs.

---

# Future Enhancements

Future releases may support:

- Job Queue Management
- Background Workers
- Distributed Processing
- Priority Scheduling
- Retry Policies
- Job Dependencies
- Real-Time Notifications
- Workflow Automation
- AI-Based Scheduling Optimization

These enhancements should integrate with the existing scheduling architecture without requiring major redesign.

---

# Guiding Principle

Scheduled Jobs automate repetitive operational tasks while keeping business logic centralized in FastAPI.

Every scheduled job should be:

- Secure
- Reliable
- Idempotent
- Auditable
- Scalable
- Easy to Monitor
- Easy to Maintain

A standardized scheduled job architecture ensures consistent background processing, timely analytics generation, reliable alerting, and efficient system maintenance while preserving the platform's cloud-native, API-first, multi-tenant, and MVP-first design philosophy.