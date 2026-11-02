# RepoPilot architecture notes

## Request path

React (Vite) → Axios service layer → FastAPI `/api/v1` → ownership checks → SQLAlchemy → SQLite (local) / PostgreSQL (Compose).
GitHub reads are made server-side through `httpx`; no GitHub token is sent to browser code.

## Implemented modules

- Authentication: registration/login, PBKDF2 password hashing, signed short-lived access JWT, refresh JWT, protected profile and stateless logout.
- Repository linking: public GitHub repository metadata, contents, commit history, branches, open issues and pull requests.
- Analysis: GitHub tree retrieval, text-file filtering, language/entry-point/dependency manifest summary, Python AST long-function signal and regex security heuristics.
- Code Q&A: code chunking, lexical relevance ranking, exact source file and line-range citations, insufficient-context response, stored sessions/messages.
- Issue triage: keyword classification, urgency rule and evidence explanation.
- Test drafts: Python AST validation and editable pytest scaffold; never executed by the API.
- Improvement workspace: explicitly returns a rule-based placeholder when no local model is configured; does not fabricate a rewritten implementation.
- PR proposals: unified-diff draft persistence and approve/reject state changes; approval is local only and cannot push or create a remote PR.
- Analytics: aggregates saved repository and analysis records only.

## Persistence

SQLAlchemy models include users, connected GitHub account metadata, repositories, repository files, analyses, findings, issues, embedding metadata, chat sessions/messages, generated tests, PR proposals and agent execution logs. Alembic configuration and an initial schema migration are included. Local startup currently calls `create_all` for convenience.

## Explicitly not implemented in this starter

- Per-user GitHub OAuth/GitHub App authorization and private repository access. Private repositories are rejected rather than accessed through a shared service credential.
- LangChain/LangGraph multi-agent orchestration, ChromaDB/Sentence Transformers semantic embeddings, reranking or local Ollama generation. Retrieval is deterministic lexical ranking with exact citations.
- OSV/NVD dependency advisory synchronization, full static-analysis engine, or verified vulnerability claims.
- Isolated execution sandbox for arbitrary repository code. Test generation is draft-only and never runs code.
- Remote branch creation, patch application, push, or GitHub PR creation. PR proposals remain local and approval-gated.
- Redis/Celery background workers. Redis is provisioned in Compose as an infrastructure extension point.
- Historical health trend data beyond recorded analysis runs.

These boundaries are intentionally visible in the UI and API responses; they should not be presented as completed functionality.
