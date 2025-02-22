# Pingdom Come (Delivers too!)
A system that aggregates data from multiple sources (Cloudflare, Vercel, GitHub, Chrome Web Store) and sends daily/weekly reports with key metrics via Temporal.

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   . venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install the project:
   ```bash
   # For development (includes all dev tools)
   pip install -e ".[dev]"

   # For production (minimal dependencies)
   pip install .
   ```

3. Set up PostgreSQL:
   - Create a new PostgreSQL database named `pingdom_db`
   - Copy `.env.example` to `.env` and update the database credentials

4. Initialize the Database:
   ```bash
   flask db init && flask db migrate -m "Initial migration" && flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

The application will be available at http://localhost:5000

## Project Structure

- Dependencies are managed in `pyproject.toml`:
  - Production dependencies under `[project.dependencies]`
  - Development tools under `[project.optional-dependencies.dev]`
  - Build configuration under `[build-system]`

- Version information is in `flask_app/__init__.py`

## Development

### Dependencies
- All dependencies are managed in `pyproject.toml`
- For development, install with `pip install -e ".[dev]"` to get:
  - Code formatting (black)
  - Linting (flake8)
  - Import sorting (isort)
  - Other development tools

### Database Management

#### Creating Models
Create your models in `flask_app/models.py`.

#### Managing Migrations
```bash
# After modifying models, create a new migration
flask db migrate -m "Description of changes"

# Apply pending migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```

### Building the Package
To create a distributable package:
```bash
python -m build
```

This creates:
- A wheel file (`.whl`) in `dist/` for pip installation
- A source distribution (`.tar.gz`) for distribution
# Show current migration
flask db current
```

### Common Issues
- If migrations aren't detecting model changes, ensure your models are imported in `migrations/env.py`
- Always review generated migrations before applying them
- Back up your database before applying migrations in production
