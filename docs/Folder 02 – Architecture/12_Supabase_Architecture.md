# Supabase Architecture

## Purpose

Supabase serves as the managed backend platform providing PostgreSQL, authentication, storage, scheduling, and security services for the Food Inventory Leakage Platform.

Business logic remains in FastAPI, while Supabase provides managed infrastructure and database services.

---

# Core Components

## Supabase PostgreSQL

Responsibilities:

* Relational database
* Transaction processing
* Data integrity
* Foreign keys
* Indexes
* Views
* Stored procedures
* Reporting queries

---

## Supabase Auth

Responsibilities:

* User registration
* Login
* Password reset
* Session management
* JWT authentication

---

## Supabase Storage

Responsibilities:

* Excel uploads
* CSV uploads
* Report exports
* Documents
* Images (future)

---

## Row-Level Security (RLS)

All business data must be isolated by tenant.

Every business table should include:

* tenant_id
* created_at
* updated_at
* created_by
* updated_by

Row-Level Security policies must ensure users can access only data belonging to their own organization.

---

## Scheduled Jobs

Supabase pg_cron will execute recurring tasks including:

* Leakage detection
* Scheduled reports
* Email notifications
* Data cleanup
* Health checks

---

# Responsibilities

Supabase is responsible for:

* Database management
* Authentication
* File storage
* Row-Level Security
* Database functions
* Scheduled tasks

FastAPI is responsible for:

* Business rules
* Inventory calculations
* Leakage detection logic
* Validation
* API endpoints
* Reporting logic
* External integrations

---

# Security Model

Security principles include:

* JWT authentication
* Row-Level Security
* Tenant isolation
* Encrypted communication (HTTPS)
* Principle of least privilege
* Secure credential management

---

# Benefits

Using Supabase provides:

* Managed PostgreSQL
* Reduced operational overhead
* Faster MVP development
* Built-in authentication
* Built-in storage
* Strong security capabilities
* Straightforward scalability

---

# Future Enhancements

As the platform grows, Supabase can support:

* Read replicas
* Database scaling
* Additional storage
* Advanced monitoring
* Enhanced backup strategies
* Enterprise authentication options

The goal is to maximize managed services while keeping application-specific business logic within FastAPI, resulting in a clean separation of responsibilities and easier long-term maintenance.
