# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (Windows)
et-env\Scripts\activate

# Run the development server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**MoneyGoes** is a Flask expense-tracker web app built as a step-by-step learning project. The app is being constructed incrementally — many routes in `app.py` are stubs with placeholder strings until the corresponding step is implemented.

### Key files

- `app.py` — all Flask routes; single file, no blueprints
- `database/db.py` — SQLite helpers: `get_db()`, `init_db()`, `seed_db()` (currently stubs for Step 1)
- `templates/base.html` — shared layout with navbar and footer; all pages extend this
- `static/js/main.js` — client-side JS, grows as features are added

### Step roadmap (from route comments)

| Step | Feature |
|------|---------|
| 1 | Database setup (`database/db.py`) |
| 2 | Register |
| 3 | Login / Logout |
| 4 | Profile |
| 7–9 | Add / Edit / Delete expenses |

### Data layer

SQLite via a raw `sqlite3` connection (no ORM). `get_db()` must set `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. The database file lives in the `database/` directory.

### Currency

All monetary values are in PKR. Display with the ₨ symbol, never USD.

### Frontend stack

Jinja2 templates extending `base.html`. Fonts: DM Serif Display + DM Sans (Google Fonts). Styles live in `static/css/style.css`.
