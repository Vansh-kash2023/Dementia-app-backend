# Dementia App Backend

Backend service for the Dementia App, built with Flask, SQLAlchemy, JWT authentication, PostgreSQL (Supabase), Cloudinary media storage, and Gemini-powered assistant features.

## What This Backend Provides

- User authentication with signup, login, and JWT-based protected access
- User profile support (name, email, emergency contact)
- Memory management (save memories with image upload to Cloudinary)
- Familiar faces management (store known people with image upload to Cloudinary)
- Reminder management (title, date, time, repeat, status)
- Assessment answer storage and report generation
- AI helper endpoint that uses user context (memories, reminders, familiar faces) with Gemini
- CORS configuration for development and production
- Database schema versioning through Flask-Migrate (Alembic)

Note: Full endpoint documentation is maintained in API_SUMMARY.md.

## Tech Stack

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate (Alembic)
- PostgreSQL (Supabase)
- Cloudinary
- Google GenAI SDK

## Repository Setup

### 1) Clone repository

- git clone https://github.com/Vansh-kash2023/Dementia-app-backend.git
- cd Dementia-app-backend

### 2) Create and activate virtual environment

Windows PowerShell:
- python -m venv venv
- .\venv\Scripts\Activate.ps1

macOS/Linux:
- python3 -m venv venv
- source venv/bin/activate

### 3) Install dependencies

- pip install -r requirements.txt

### 4) Configure environment variables

Create a .env file in the project root and copy values from .env.example.

Required variables:
- JWT_SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS
- GEMINI_API_KEY
- HOST
- PORT
- FLASK_DEBUG
- FLASK_ENV
- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET
- CLOUDINARY_FOLDER
- CORS_ALLOWED_ORIGINS

Environment notes:
- SQLALCHEMY_DATABASE_URI should point to your Supabase/PostgreSQL connection string.
- In production, CORS_ALLOWED_ORIGINS must be explicitly set (comma-separated origins).
- Keep .env private and never commit secrets.

## Run the Backend (Development)

Windows PowerShell:
- .\venv\Scripts\Activate.ps1
- python run.py

macOS/Linux:
- source venv/bin/activate
- python run.py

Expected behavior:
- App reads HOST, PORT, and FLASK_DEBUG from .env.
- Health route should respond at / with a server-up message.

## Run the Backend (Production)

Recommended (Linux container/VM):
- python -m gunicorn --bind 0.0.0.0:8000 wsgi:app

Typical production environment settings:
- FLASK_ENV=production
- FLASK_DEBUG=false
- HOST=0.0.0.0
- PORT=8000
- CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

## Database Migrations (Important)

This project uses Flask-Migrate for all schema changes.
Do not use runtime table auto-creation for production workflows.

### Core commands

Before migration commands, set FLASK_APP.

Windows PowerShell:
- $env:FLASK_APP = "run.py"

macOS/Linux:
- export FLASK_APP=run.py

Then use:
- flask db init        (one-time, if migrations folder does not exist)
- flask db migrate -m "describe change"
- flask db upgrade
- flask db downgrade -1
- flask db current
- flask db history

### Standard workflow after model changes

1. Update models in app/models/models.py.
2. Generate migration:
   - flask db migrate -m "add <feature>"
3. Review generated migration file in migrations/versions.
4. Apply migration:
   - flask db upgrade
5. Verify revision:
   - flask db current

### Existing database already has tables

If your database already has schema and you want to start tracking with migrations without dropping data:

1. Ensure models match current DB schema.
2. Generate baseline migration:
   - flask db migrate -m "baseline existing schema"
3. Mark DB as already at latest revision:
   - flask db stamp head

Use this path when you want to preserve existing data.

### Full reset path (destructive)

Use this only when existing data/tables are not needed.

1. Drop all tables (project script or SQL).
2. Generate migration from models:
   - flask db migrate -m "initial schema"
3. Recreate schema using migrations:
   - flask db upgrade

This path was used in this repository setup when Supabase data was considered disposable.

## Troubleshooting

- Error: Missing required environment variable
  - Add missing key to .env and restart.

- Error: flask db commands fail
  - Ensure virtual environment is active and FLASK_APP is set to run.py.

- Error: DB connection/authentication issues
  - Re-check SQLALCHEMY_DATABASE_URI, password encoding, network access, and Supabase allowlist.

- Error: CORS blocked in production
  - Set CORS_ALLOWED_ORIGINS to exact frontend origins (comma-separated).

## Project Conventions

- Keep secrets only in .env.
- Use migration files for every schema change.
- Keep API-specific request/response details in API_SUMMARY.md.
