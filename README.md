# RepoPilot

AI-powered GitHub repository intelligence workspace. This repository is a runnable, extensible foundation with a real FastAPI backend, persistent SQLAlchemy models, JWT auth, GitHub REST integration for public repositories, static analysis, source-grounded retrieval, issue triage, test drafting, improvement suggestions and approval-gated PR proposals.

## Quick start (Windows PowerShell)

1. Install Python 3.12+ and Node.js 20+.
2. Copy `backend/.env.example` to `backend/.env` and set a long `SECRET_KEY`.
3. Optional: set `GITHUB_TOKEN` as a server-side token to raise public GitHub API rate limits. Do not commit `.env`. Private-repository OAuth/GitHub App authorization is not implemented in this build.
4. Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\dev.ps1
```

The script creates a Python venv, installs dependencies, starts the API and Vite dev server in separate windows. Open http://localhost:5173. API docs: http://localhost:8000/docs.

Alternative manual startup:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Default database is SQLite at `backend/repopilot.db` for zero-friction local development. Set `DATABASE_URL` to PostgreSQL for deployment. Docker Compose includes PostgreSQL and Redis.

## Functional boundaries

- Public GitHub repository reads work without credentials. Private repositories are deliberately rejected until per-user OAuth/GitHub App authorization is implemented; a shared service token is not treated as user consent.
- Analysis is deterministic static inspection; findings are heuristics, not confirmed vulnerabilities. Dependency advisory lookups and execution sandboxing are not enabled by default.
- RAG uses repository-aware lexical retrieval and exact line citations out of the box. Optional local model integrations can be added without requiring paid APIs.
- Test generation produces editable pytest drafts; it does not execute repository code on the API host.
- PR proposals are persisted as drafts. Approval is explicit; the starter does not push or create remote PRs automatically.
- Metrics are calculated from stored records and connected repository data; no historical trend is invented.

## Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

## Security notes before production

Set a unique 32+ character `SECRET_KEY`, configure HTTPS, managed PostgreSQL/Redis, restrictive CORS, rate limiting at the gateway, encrypted secrets/KMS, backups, audit retention, and an isolated container runner for untrusted code. Review GitHub App permissions and OAuth callback settings before enabling write scopes.
