# System Architecture

## Overview

The Food Inventory Leakage Platform follows a layered, cloud-native, multi-tenant architecture designed for rapid MVP delivery while supporting future growth into a production-scale SaaS platform.

The architecture separates presentation, business logic, data management, and infrastructure responsibilities to ensure maintainability, scalability, and security.

---

# High-Level Architecture

```text
Users
   │
   ▼
React + TypeScript Frontend
   │
   ▼
FastAPI REST API
   │
   ├──────────► Supabase Auth
   │
   ├──────────► Supabase Storage
   │
   ├──────────► Supabase PostgreSQL
   │
   └──────────► Brevo Email Service
                    │
                    ▼
             Email Notifications

Scheduled Tasks
      │
      ▼
Supabase pg_cron
      │
      ▼
Leakage Detection
Report Generation
Email Scheduling
```

---

# Architecture Layers

## Presentation Layer

Responsibilities:

* User interface
* Forms
* Dashboards
* Reports
* Data visualization
* User interaction

Technology:

* React
* TypeScript
* Tailwind CSS
* shadcn/ui
* Recharts

---

## Business Layer

Responsibilities:

* Business rules
* Leakage detection
* Validation
* Inventory calculations
* Risk scoring
* Reporting logic
* API endpoints

Technology:

* FastAPI

---

## Data Layer

Responsibilities:

* Persistent storage
* Transaction management
* Security
* Multi-tenancy
* Database functions

Technology:

* Supabase PostgreSQL

---

## Infrastructure Layer

Responsibilities:

* Authentication
* File storage
* Scheduling
* Email
* Hosting

Technologies:

* Supabase Auth
* Supabase Storage
* Supabase pg_cron
* Brevo
* Vercel
* Render

---

# Core Architectural Principles

* Separation of concerns
* Stateless backend
* REST API design
* Multi-tenant architecture
* Secure by default
* Modular development
* Cloud-native deployment
* Scalable design

---

# Data Flow Summary

1. Users upload Excel or CSV files.
2. The frontend sends data to FastAPI.
3. FastAPI validates and processes the data.
4. Data is stored in Supabase PostgreSQL.
5. Leakage detection rules analyze operational data.
6. Results are displayed through dashboards and reports.
7. Scheduled jobs generate alerts and email notifications.

---

# Future Expansion

The architecture supports future additions without major redesign, including:

* Mobile applications
* ERP integrations
* AI services
* OCR processing
* Public APIs
* Advanced analytics
* Third-party integrations
