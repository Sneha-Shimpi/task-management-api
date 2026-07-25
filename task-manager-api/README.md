# Task Management API

A small, production-style REST API for managing tasks, built with Flask, SQLAlchemy, and SQLite.

## Tech Stack

| Concern            | Choice                     |
|---------------------|-----------------------------|
| Backend framework   | Flask                      |
| Database            | SQLite                     |
| ORM                 | SQLAlchemy (via Flask-SQLAlchemy) |
| Validation          | Marshmallow                |
| Testing             | Pytest                     |
| API testing         | Postman (collection included) |

## Project Structure

```
task-manager-api/
├── app/
│   ├── __init__.py       # Application factory, error handlers, frontend route
│   ├── config.py         # Dev / testing / production configs
│   ├── extensions.py     # SQLAlchemy instance (avoids circular imports)
│   ├── models.py         # Task model
│   ├── routes.py         # API endpoints (/api/tasks...)
│   ├── schemas.py        # Marshmallow request/response schemas
│   ├── templates/
│   │   └── index.html    # Frontend shell (served at /)
│   └── static/
│       ├── css/style.css # Frontend styling
│       └── js/app.js     # Frontend logic (fetch calls to the API)
├── tests/
│   ├── conftest.py       # Pytest fixtures (app, client, sample_task)
│   └── test_tasks.py     # CRUD, validation, filtering, error-case tests
├── postman_collection.json
├── requirements.txt
├── run.py                # Local entry point
└── README.md
```

## Frontend

A small vanilla HTML/CSS/JS UI is served directly by Flask at `http://localhost:5000/`
— no separate build step, no Node required. It's a three-column board (todo /
in progress / done) styled like a drafting-desk logbook: index cards with a
priority-colored edge, filterable by priority, with a modal for creating,
editing, and deleting tasks. It talks to the same `/api/tasks` endpoints
documented below via `fetch()`.

If you'd rather build this as a separate React/Vite app later, the API
already returns plain JSON and doesn't care who the client is — you'd just
need to add CORS headers (e.g. `flask-cors`) since it would run on a
different port during development.

## Getting Started

### Prerequisites
- Python 3.10+

### Setup

```bash
git clone <your-repo-url>
cd task-manager-api
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
python run.py
```

The API will be available at `http://localhost:5000`. A SQLite file `tasks.db`
is created automatically in the project root on first run — no manual DB setup
required.

### Run the tests

```bash
pytest -v
```

Tests run against an in-memory SQLite database (see `TestingConfig`), so they
never touch `tasks.db` and are fully isolated from each other.

### Try it with Postman

Import `postman_collection.json` into Postman. It includes happy-path and
error-case requests for every endpoint, and automatically captures the
created task's `id` into a collection variable so follow-up requests
(`GET`/`PUT`/`DELETE` by id) work out of the box.

## API Reference

Base URL: `http://localhost:5000/api`

### Create a task
`POST /tasks`

```json
{
  "title": "Write README",
  "description": "Document setup and usage",
  "priority": "high"
}
```
`title` is the only required field. `status` defaults to `todo`, `priority`
defaults to `medium`, `description` defaults to `""`.

**201 Created**
```json
{
  "id": 1,
  "title": "Write README",
  "description": "Document setup and usage",
  "status": "todo",
  "priority": "high",
  "created_at": "2026-07-25T10:00:00+00:00",
  "updated_at": "2026-07-25T10:00:00+00:00"
}
```

### List tasks
`GET /tasks?status=todo&priority=high&page=1&per_page=20`

All query params are optional.
- `status`: one of `todo`, `in_progress`, `done`
- `priority`: one of `low`, `medium`, `high`
- `page` / `per_page`: pagination (default page 1, 20 per page, max 100 per page)

**200 OK**
```json
{
  "tasks": [ { "id": 1, "title": "...", "...": "..." } ],
  "page": 1,
  "per_page": 20,
  "total": 1,
  "total_pages": 1
}
```

### Get a task
`GET /tasks/<id>` → 200 with the task, or 404 if it doesn't exist.

### Update a task
`PUT /tasks/<id>` (partial updates supported — only send the fields you want
to change)

```json
{ "status": "in_progress" }
```
Returns 200 with the updated task, 404 if not found, 400 if the body is
empty or contains invalid values.

### Delete a task
`DELETE /tasks/<id>` → 204 No Content, or 404 if not found.

### Errors

All errors return a consistent JSON shape:

```json
{ "error": "Validation failed", "details": { "title": ["Missing data for required field."] } }
```

| Status | Meaning                          |
|--------|-----------------------------------|
| 400    | Validation error / bad request    |
| 404    | Resource not found                |
| 405    | Method not allowed on that route  |
| 500    | Unexpected server error           |

## Design Decisions & Trade-offs

- **SQLite over Postgres/MySQL**: matches the "very easy" persistence
  requirement and needs zero setup. The app only talks to the DB through
  SQLAlchemy, so swapping `SQLALCHEMY_DATABASE_URI` for a Postgres URL is a
  one-line change if this needed to scale.
- **Integer auto-increment IDs** rather than UUIDs: simpler to read and test
  against for a small internal-style API. A public-facing API might prefer
  UUIDs to avoid leaking sequence/volume information.
- **Marshmallow schemas separate from the SQLAlchemy model**: keeps
  validation rules (required fields, allowed enum values, length limits)
  independent from persistence, so the API contract can evolve without
  touching the DB schema and vice versa.
- **Partial updates on `PUT`**: strictly speaking `PATCH` is the more
  "correct" verb for partial updates, but `PUT` is aliased to the same
  handler for convenience since many API clients default to PUT. Either verb
  works.
- **No pagination by default limit surprises**: `per_page` is capped at 100
  to avoid a client accidentally pulling the entire table in one request.
- **Frontend served by Flask, not a separate SPA**: a plain HTML/CSS/JS UI
  under `app/templates` and `app/static`, rendered via `render_template`.
  This avoids a Node/npm build step entirely — `python run.py` is the only
  command needed to see the UI. The trade-off is it doesn't have a
  component framework's state management; that's a reasonable next step if
  the UI grows past a single board view.
- **Not implemented (optional)**: authentication, Docker, and CI/CD were
  left out to keep the submission focused and reviewable within the
  recommended time window. The app is structured (blueprint + config
  classes) so any of these could be layered on without a rewrite.

## AI Usage Disclosure

I used **[FILL IN: e.g. Claude / ChatGPT / GitHub Copilot]** while building
this project. Below is an honest account — replace the bracketed notes with
what actually happened for your submission, since the reviewers explicitly
compare this section against the code and may ask about it in a follow-up
discussion.

**What AI helped with:**
- Scaffolding the initial project structure (app factory pattern, blueprint
  registration, config classes for dev/test/prod).
- Drafting the Marshmallow schemas and the first pass of CRUD route handlers.
- Generating the initial Pytest test suite covering CRUD happy paths,
  validation failures, filtering, and pagination.
- Drafting this README.

**Example prompts used:**
- "Set up a Flask app factory with separate config classes for development
  and testing, using Flask-SQLAlchemy."
- "Write Marshmallow schemas for creating and partially updating a Task
  model with fields: title, description, status, priority."
- "Write pytest tests for a Flask CRUD API covering success and error cases
  for each endpoint, using an in-memory SQLite DB."

**What I reviewed / changed:**
- [FILL IN — be specific, e.g.: "Switched task IDs from UUID to integer
  auto-increment after deciding UUIDs added complexity without benefit for
  this use case."]
- [FILL IN — e.g.: "Verified error responses actually return the status
  codes and JSON shape documented in the README by running the test suite
  and hitting the endpoints manually in Postman."]
- [FILL IN — e.g.: "Checked that `db.session.get()` (not the deprecated
  `Model.query.get()`) is used, since that's the current SQLAlchemy 2.x
  pattern."]
- I read and understand every line of code in this repository and can walk
  through any design decision in the follow-up discussion.

## A note on this specific submission

This project was scaffolded with the help of Claude (Anthropic), running in
a sandboxed environment with **no internet access**, so the test suite
below could not be executed against the real `flask-sqlalchemy` /
`marshmallow` / `pytest` packages before hand-off. The code follows current,
standard APIs for these libraries (Flask-SQLAlchemy 3.x, Marshmallow 3.x),
but **you should run `pip install -r requirements.txt && pytest -v`
yourself before submitting**, and fix anything that doesn't pass. Treat this
as a strong first draft, not a verified final artifact — reviewing and
validating AI output is explicitly part of what this exercise is testing.
