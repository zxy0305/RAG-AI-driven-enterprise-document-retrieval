# RAG — AI-driven enterprise document retrieval

## Sprint 0: Scaffolding

Monorepo with a FastAPI backend, a Next.js frontend, and Postgres+pgvector/Redis
for local dev, wired together with Docker Compose.

## Quickstart

```bash
docker compose up --build
```

- API: http://localhost:8000/hello
- Web: http://localhost:3000

## Structure

```
apps/api      FastAPI backend
apps/web      Next.js frontend
packages/     Shared code (future)
```

## Local dev without Docker

API:
```bash
cd apps/api
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Web:
```bash
cd apps/web
npm install
npm run dev
```

## Pre-commit

```bash
pip install pre-commit
pre-commit install
```
