# Simple Task Tracker

Full-stack task/project tracker built with FastAPI, SQLAlchemy, PostgreSQL, and Vue 3.

## Features

- Create, list, update, and delete tasks
- Valid task statuses: `Todo`, `In Progress`, and `Done`
- Automatic PostgreSQL table initialization
- Responsive Vue interface with live state updates
- Environment-based database and CORS configuration

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

## PostgreSQL setup

### Windows

1. Install PostgreSQL from https://www.postgresql.org/download/windows/
2. Open `SQL Shell (psql)` or `psql` and sign in with the PostgreSQL superuser.
3. Create the application database:

```sql
CREATE DATABASE task_tracker;
```

4. Copy `.env.example` to `.env`, then update the credentials if they differ:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_tracker
CORS_ORIGINS=http://localhost:5173
```

## Backend setup

Run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
Copy-Item .env.example .env
Set-Location backend
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

The `tasks` table is created automatically when the FastAPI application starts.

## Frontend setup

Open a second terminal from the repository root:

```powershell
Set-Location frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update title, description, or status |
| DELETE | `/tasks/{id}` | Delete a task |

Example create payload:

```json
{
  "title": "Prepare internship presentation",
  "description": "Summarize the implementation and test results",
  "status": "Todo"
}
```

## Tests

```powershell
Set-Location backend
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/task_tracker"
..\.venv\Scripts\python.exe -m pytest -q
```

## Git branches

- `main`: stable integrated project
- `feat/backend`: FastAPI, SQLAlchemy, PostgreSQL, API validation
- `feat/frontend`: Vue 3 task interface
- `feat/docs`: setup and project documentation
