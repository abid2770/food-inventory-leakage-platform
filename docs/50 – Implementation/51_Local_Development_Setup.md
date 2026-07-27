# Local Development Setup

## Purpose

This document defines the standard local development environment for the Food Inventory Leakage Platform.

A consistent development environment ensures all developers, AI coding assistants, and future contributors work with the same tools, configurations, and project structure.

This document serves as the official guide for setting up a new development machine.

---

# Objectives

The local development environment should:

- Be easy to install
- Be reproducible
- Match the production architecture
- Support rapid development
- Support automated testing
- Minimize configuration issues
- Follow cloud-native development practices

---

# Development Environment

The platform is developed using the following technology stack.

| Component | Technology |
|-----------|------------|
| Operating System | Windows 11 (Primary), Linux/macOS Supported |
| IDE | Visual Studio Code |
| Version Control | Git |
| Source Repository | GitHub |
| Backend Language | Python 3.13+ |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | Supabase PostgreSQL |
| Database Migration | Alembic |
| Database Driver | asyncpg |
| Frontend | React + TypeScript |
| Build Tool | Vite |
| UI Framework | Tailwind CSS |
| UI Components | shadcn/ui |
| Authentication | Supabase Auth |
| Storage | Supabase Storage |
| Dashboard | Metabase |
| Email | Brevo |
| API Testing | Postman |
| Backend Hosting | Railway |
| Frontend Hosting | Vercel |

---

# Required Software

Install the following software before starting development.

## Git

Required for source control.

Recommended version:

- Latest Stable Release

---

## Visual Studio Code

Required for development.

Recommended extensions:

- Python
- Pylance
- Ruff
- Black Formatter
- GitHub Copilot (Optional)
- GitLens
- Docker (Optional)
- PostgreSQL
- Tailwind CSS IntelliSense
- ESLint
- Prettier

---

## Python

Install:

```text
Python 3.13 or later
```

Verify installation:

```bash
python --version
```

---

## Node.js

Install:

```text
Latest LTS Version
```

Verify:

```bash
node --version
npm --version
```

---

## Git

Verify installation:

```bash
git --version
```

---

# Clone Repository

Clone the project.

```bash
git clone https://github.com/<organization>/<repository>.git
```

Open the project.

```bash
cd repository
```

---

# Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

Windows:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
python3 -m venv .venv
```

---

# Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

# Install Backend Dependencies

```bash
pip install -r requirements.txt
```

Verify:

```bash
pip list
```

---

# Frontend Setup

Navigate to frontend.

```bash
cd frontend
```

Install packages.

```bash
npm install
```

Start development server.

```bash
npm run dev
```

---

# Environment Variables

Create a local environment file.

```text
backend/.env
```

Typical variables include:

```text
SUPABASE_URL=
SUPABASE_DB_HOST=
SUPABASE_DB_PORT=
SUPABASE_DB_NAME=
SUPABASE_DB_USER=
SUPABASE_DB_PASSWORD=

SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

JWT_SECRET_KEY=

BREVO_API_KEY=

METABASE_URL=

APP_ENV=development
```

Environment files must never be committed to Git.

---

# Database Connection

The application connects to:

- Supabase PostgreSQL

Development uses:

- SQLAlchemy AsyncSession
- asyncpg
- Alembic migrations

Schema changes must always use Alembic.

---

# Alembic Setup

Initialize migrations if required.

```bash
alembic init migrations
```

Create a migration.

```bash
alembic revision --autogenerate -m "Initial schema"
```

Apply migrations.

```bash
alembic upgrade head
```

Alembic migrations must connect using the direct Supabase connection string, not the pooled connection, to avoid transaction-mode pooling issues with DDL operations.

---

# Project Structure

The backend project structure follows the standard defined in:

**41_Project_Structure.md**

Developers must not introduce new folders without architectural approval.

---

# Running the Backend

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

Default URL:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

OpenAPI Schema:

```text
http://localhost:8000/openapi.json
```

---

# Running the Frontend

Start the frontend.

```bash
npm run dev
```

Default URL:

```text
http://localhost:5173
```

---

# Running Tests

Backend tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

Frontend tests:

```bash
npm test
```

Testing standards are defined in:

**48_Testing_Strategy.md**

---

# Code Formatting

Python formatting:

```bash
black .
```

Linting:

```bash
ruff check .
```

Type checking:

```bash
mypy app
```

Frontend formatting:

```bash
npm run lint
```

---

# Git Workflow

Typical workflow:

```text
Clone Repository
       │
Create Feature Branch
       │
Implement Feature
       │
Run Tests
       │
Commit Changes
       │
Push Branch
       │
Create Pull Request
       │
Code Review
       │
Merge
```

Git workflow standards are defined in:

**52_Git_Workflow.md**

---

# Local Development Rules

Developers should:

- Pull the latest changes before starting work.
- Keep dependencies up to date.
- Run tests before committing.
- Follow coding standards.
- Keep commits small and focused.
- Resolve merge conflicts promptly.

---

# Security During Development

Developers must never:

- Commit `.env` files.
- Commit API keys.
- Commit database passwords.
- Commit JWT secrets.
- Disable authentication.
- Disable Row-Level Security.

Use environment variables for all sensitive configuration.

---

# Troubleshooting

Common issues include:

- Missing environment variables
- Python virtual environment not activated
- Missing Node.js packages
- Alembic migration conflicts
- Incorrect database connection strings
- Supabase authentication failures

Resolve issues before implementing new features.

---

# Documentation

When local setup changes:

- Update this document.
- Update installation instructions.
- Keep dependency versions current.
- Remove obsolete steps.

Documentation must always reflect the approved development environment.

---

# Guiding Principle

Every developer should be able to clone the repository, configure the environment, connect to Supabase, and run both the FastAPI backend and React frontend with minimal effort.

A consistent local development environment reduces onboarding time, improves collaboration, minimizes configuration errors, and ensures reliable implementation of the Food Inventory Leakage Platform.