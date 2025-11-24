# Assetrack

Assetrack is a Django 5 application for tracking the full lifecycle of laboratory and field assets—hardware, software, maintenance schedules, and the documents that support them. It ships with HTMX-enhanced views, generic attachment handling, and request logging so teams can keep critical equipment compliant and audit-ready.

## Feature Highlights
- Equipment registry with manufacturer, calibration, warranty, and replacement metadata (`asset.models.equipment`).
- Software inventory plus license/record tracking (`asset/urls.py` → `software_*` views).
- Preventive maintenance scheduler and status dashboards powered by the home panels in `templates/home.html`.
- Generic attachment subsystem (`attachment` app) for equipment, software, and maintenance records.
- Custom user model plus authentication views in `user`.
- Request logging middleware (`requestlog`) for basic auditing of incoming traffic.

## Project Layout
- `core/` – Django project settings, URLs, WSGI/ASGI entrypoints.
- `asset/` – Equipment, software, schedule, and maintenance domain logic.
- `attachment/` – Generic file upload models and CRUD.
- `user/` – Custom user model and auth views.
- `requestlog/` – Middleware and models for request auditing.
- `templates/`, `static/`, `staticfiles/`, `media/` – Front-end assets and uploads.
- `fixtures/` – Optional seed data for statuses, calibration types, and record types.

## Requirements
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- SQLite (bundled in `data/assetrack.sqlite3` for local development)
- Optional: Docker + Docker Compose for containerized runs

## Local Development

> **Migration Note:** This project has migrated from `requirements.txt` to `pyproject.toml` with `uv` for dependency management. The old `requirements.txt` and `requirements.dev.txt` files are kept for backward compatibility but are no longer the primary source of dependencies.

### 1. Install uv (if not already installed)
```pwsh
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create a virtual environment and install dependencies
```pwsh
# Install production dependencies only
uv sync

# Install with development dependencies (recommended for local development)
uv sync --extra dev
```

**Note:** The virtual environment will be automatically created at `.venv/` and dependencies are managed via `pyproject.toml` and locked in `uv.lock`.

### 3. Configure environment variables
Create a `.env` file (or export variables in your shell) with at least:
```dotenv
DJANGO_SETTINGS_MODULE=core.settings.development
```
The development settings already include a non-production `SECRET_KEY` and point to `data/assetrack.sqlite3`.

### 4. Apply migrations and seed data
```pwsh
# Activate the virtual environment first
# Windows
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

# Or use uv run to run commands without activating
uv run python manage.py migrate
uv run python manage.py loaddata fixtures/assset_status.json fixtures/assset_calibration.json
uv run python manage.py createsuperuser
```
Add or remove fixtures as needed; they provide reference data for dropdowns.

### 5. Run the development server
```pwsh
# Using activated virtual environment
python manage.py runserver

# Or using uv run
uv run python manage.py runserver
```
Visit `http://127.0.0.1:8000/` and log in with the superuser you created to access dashboards and CRUD screens.

## Docker Workflow
Use the provided images (Gunicorn + Nginx TLS termination) for local parity or deployment testing:
```pwsh
docker compose up --build
```
Make sure your `.env` file also contains production-only settings such as `SECRET_KEY`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` when running against `core.settings.production`.

## Quality Checks
- Run Django tests: `python manage.py test`
- Lint Python: `ruff check .`
- Lint templates: `djlint templates --check`
- Collect static files before packaging: `python manage.py collectstatic --noinput`

## Deployment Notes
- Set `DJANGO_SETTINGS_MODULE=core.settings.production`.
- Provide `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and database credentials via environment variables.
- Point `MEDIA_ROOT` and `STATIC_ROOT` to persistent storage and run `collectstatic`.
- `docker-compose.yml` mounts volumes for `staticfiles`, `media`, and `data`—map them to durable storage in production.

## License
This project is licensed under the [MIT License](LICENSE).
