# 10_Technology_Stack.md

# Technology Stack

**Version:** 1.1  
**Status:** Approved  
**Last Updated:** July 2026

---

# Purpose

This document defines the official technology stack for the Food Inventory Leakage Detection Platform.

All future architectural decisions and development work must follow this stack unless an approved architecture change is made.

The guiding principles for technology selection are:

- Simplicity
- Reliability
- Scalability
- Low operational cost
- Open-source preference
- MVP-first development

---

# Frontend

| Component | Technology |
|-----------|------------|
| Framework | React |
| Language | TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Forms | React Hook Form |
| Validation | Zod |
| Routing | React Router |
| State Management | TanStack Query + React Context |
| Charts | Recharts |

---

# Backend

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.12+ |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Validation | Pydantic |
| API Documentation | OpenAPI (Swagger UI) |
| Authentication | Supabase Auth |

The platform uses SQLAlchemy 2.0 with AsyncSession and the asyncpg PostgreSQL driver.

All backend database operations use Python async/await.

Alembic is used for all database schema migrations.

---

# Database

| Component | Technology |
|-----------|------------|
| Database | Supabase PostgreSQL |
| Row-Level Security | PostgreSQL RLS |
| Extensions | pgcrypto, pg_trgm (as required) |
| Connection Pooling | Supabase Pooler |

---

# Storage

| Component | Technology |
|-----------|------------|
| File Storage | Supabase Storage |

---

# Dashboard & Analytics

| Component | Technology |
|-----------|------------|
| BI Dashboard | Metabase |

---

# Background Processing

| Component | Technology |
|-----------|------------|
| Scheduled Jobs | Supabase pg_cron |
| External Automation | GitHub Actions |

---

# Notifications

| Component | Technology |
|-----------|------------|
| Email Service | Brevo |

---

# Version Control

| Component | Technology |
|-----------|------------|
| Source Control | Git |
| Repository Hosting | GitHub |

---

# Hosting & Deployment

| Component | Technology |
|-----------|------------|
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Database Hosting | Supabase |

---

# Development Tools

| Component | Technology |
|-----------|------------|
| API Testing | Postman / Bruno |
| Database Management | Supabase Dashboard |
| SQL IDE | DBeaver |
| Code Editor | Visual Studio Code |
| Python Environment | uv or venv |

---

# Security

| Component | Technology |
|-----------|------------|
| Authentication | Supabase Auth |
| Authorization | PostgreSQL Row-Level Security (RLS) |
| Password Security | Managed by Supabase Auth |
| Secrets Management | Environment Variables |
| HTTPS | Enabled on all production services |

---

# Architecture Principles

The platform follows these architectural principles:

- React frontend communicates only with FastAPI APIs.
- FastAPI contains all business logic.
- SQLAlchemy is the official ORM for database access.
- Alembic is the official database migration framework.
- PostgreSQL is the single source of truth.
- Row-Level Security (RLS) is mandatory for tenant isolation.
- Business logic does not reside in the database.
- Background jobs run through Supabase pg_cron and GitHub Actions.
- The application is stateless and horizontally scalable.
- The project follows an MVP-first development philosophy.

---

# Future Technologies (Not Part of MVP)

The following technologies may be introduced in future versions after business validation:

- Redis (caching)
- Celery (distributed background jobs)
- Apache Kafka (event streaming)
- Elasticsearch (advanced search)
- AI/LLM services
- Mobile application (React Native)

These technologies are **not part of the approved MVP stack** and require formal architectural approval before adoption.

---

# Approved Technology Stack Summary

| Layer | Technology |
|--------|------------|
| Frontend | React + TypeScript |
| UI | Tailwind CSS + shadcn/ui |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Database | Supabase PostgreSQL |
| Authentication | Supabase Auth |
| Storage | Supabase Storage |
| Dashboard | Metabase |
| Scheduling | Supabase pg_cron + GitHub Actions |
| Email | Brevo |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Version Control | GitHub |

---

# Change Management

No technology in this document may be replaced or supplemented without a documented architecture review and formal approval.

This ensures consistency across all project documentation and prevents technology drift during development.