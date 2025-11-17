# Repository Guidelines

## Project Structure & Module Organization
Assetrack is a Django 5 project. `core/` holds project settings, URL routing, and top-level views; treat it as the entry point for new global config. Feature work generally lives in app folders such as `asset/`, `attachment/`, and `user/`, each with Django-standard `models/`, `views/`, `forms/`, or `templatetags/` submodules. Front-end assets are in `static/` and `staticfiles/`, while templates are under `templates/`. Local SQLite data persists at `data/assetrack.sqlite3`; avoid committing regenerated copies.

## Build, Test, and Development Commands
Create or activate the virtual environment in `.venv/`, then install dependencies: `pip install -r requirements.dev.txt`. During iterative work run `python manage.py runserver` for the Django dev server and `python manage.py migrate` whenever model schema changes occur. Use `python manage.py createsuperuser` to seed admin access and `python manage.py collectstatic --noinput` before packaging static files for deployment.

## Coding Style & Naming Conventions
We follow standard Python with 4-space indentation and aim for modules under 120 characters per line (enforced by Ruff via `ruff check .`). Prefer descriptive, lowercase_with_underscores module and function names; Django models stay in `PascalCase`, and template blocks use hyphenated names (example: `{% block asset-header %}`). HTML templates may be linted with `djlint templates --check`. Keep view functions slim by delegating business logic to services or models when possible.

## Testing Guidelines
Store new tests alongside their respective apps (for example, `asset/tests.py` or `user/tests/`). Use Django’s TestCase subclasses and name methods with the pattern `test_<condition>`. Run the suite with `python manage.py test` and include any relevant `--tag` filters in PR notes when partial runs are necessary. Target high coverage on business-critical flows such as CSV exports and attachment uploads; add regression tests for reported bugs before patching them.

## Commit & Pull Request Guidelines
Commit summaries should be short, imperative, and lowercase, mirroring history entries like `fix csv export bug`. Group related changes into a single commit and avoid mixing formatting-only updates with feature work. For pull requests, provide a crisp problem statement, describe the solution, link related issues, and attach screenshots or terminal captures for UI or command changes. Note database migrations and manual steps so reviewers can reproduce the setup quickly.

## Security & Configuration Tips
Secrets live in `.env`; never hard-code them in settings or fixtures. When configuring new services, rely on environment variables surfaced via `core/settings/`. Keep the exposed SQLite file for local use only and update deployment docs if the target environment uses Postgres or another backend. Review nginx/ deployment assets in `nginx/` whenever altering domains or static hosting.
