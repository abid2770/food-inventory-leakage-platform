# Project Instructions

This project serves as the single source of truth for designing, developing, reviewing, and maintaining the Food Inventory Leakage Platform.

All future conversations, recommendations, architecture decisions, documentation, and code generation must remain consistent with these instructions.

---

# Primary Objective

Build a production-ready, multi-tenant SaaS platform that helps food manufacturers detect inventory leakage, production wastage, shrinkage, and operational losses while keeping development, deployment, and operational costs low.

---

# Development Philosophy

Always prioritize:

* MVP First
* Business Value First
* Simplicity Before Complexity
* Excel First
* Low Cost
* Maintainability
* Security
* Scalability
* Performance
* Production Readiness

Avoid unnecessary complexity and overengineering.

---

# Locked Technology Stack

Unless explicitly changed, treat the following decisions as final.

Database:

* Supabase PostgreSQL

Authentication:

* Supabase Auth

Storage:

* Supabase Storage

Backend:

* FastAPI

Frontend:

* React
* TypeScript

UI:

* Tailwind CSS
* shadcn/ui

Charts:

* Recharts

Scheduling:

* Supabase pg_cron

Email:

* Brevo

Frontend Hosting:

* Vercel

Backend Hosting:

* Render

Version Control:

* GitHub

---

# Architecture Principles

The system must always be:

* Multi-Tenant
* API First
* Cloud Native
* Modular
* Stateless
* Secure by Default
* AI Ready

Business logic should reside in FastAPI.

Supabase should manage:

* PostgreSQL
* Authentication
* Storage
* Row-Level Security
* Database Functions
* Scheduling

---

# Coding Standards

Generate production-quality code.

Code should be:

* Clean
* Readable
* Modular
* Well Documented
* Secure
* Efficient
* Testable
* Easy to Maintain

---

# Database Standards

Every database design should include:

* Proper normalization
* Foreign keys
* Indexes
* Audit columns
* Soft deletes where appropriate
* Row-Level Security
* Tenant isolation
* Performance optimization

---

# Documentation Standards

Documentation should:

* Use Markdown
* Explain architectural decisions
* State assumptions
* Maintain consistency
* Reference previous approved decisions

If contradictions are found, identify them before generating new content.

---

# Review Process

When reviewing documents or code:

1. Verify technical correctness.
2. Check consistency with approved architecture.
3. Identify unnecessary complexity.
4. Recommend simplifications.
5. Highlight security risks.
6. Highlight scalability concerns.
7. Explain trade-offs.
8. Recommend one of:

   * Approved
   * Approved with Changes
   * Needs Revision

---

# Communication Style

Provide honest, practical, and evidence-based recommendations.

Challenge poor architectural decisions respectfully.

Always explain trade-offs.

Recommend the simplest solution that satisfies the business requirement.

---

# Workflow

Work sequentially through these phases:

1. Business Requirements
2. Technology Decisions
3. Architecture
4. Database Design
5. API Design
6. Backend Development
7. Frontend Development
8. Testing
9. Deployment
10. Documentation

Do not skip phases without a valid reason.
