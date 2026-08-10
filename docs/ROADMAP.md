# Roadmap — Sprint-by-Sprint

12 sprints (~1–2 weeks each). Each sprint ends in a working, demoable slice.
CI/CD grows one increment per sprint rather than being bolted on at the end.

## Sprint 1 — Scaffolding
- `RAG-001` Monorepo structure (`apps/api`, `apps/web`, `packages/shared`)
- `RAG-002` `docker-compose.yml`: Postgres+pgvector, Redis, api, web
- `RAG-003` Pre-commit: ruff/black (py), eslint/prettier (ts)
- `RAG-004` GitHub Actions: lint + unit test on PR
- `RAG-005` Hello-world FastAPI endpoint + Next.js page consuming it
- **DoD:** `docker-compose up` works locally, CI green
- **Demo:** full stack says hello from localhost

## Sprint 2 — MVP RAG
- `RAG-006` PDF folder-loader script
- `RAG-007` Naive recursive chunker
- `RAG-008` OpenAI embeddings → pgvector upsert
- `RAG-009` Top-k cosine retrieval endpoint
- `RAG-010` Prompt template + LLM generate endpoint
- `RAG-011` Minimal chat UI (no auth/streaming)
- `RAG-012` CI: build & push Docker images to GHCR on merge to main
- `RAG-013` Manual deploy to Fly.io/Railway (single box)
- **DoD:** ask → grounded answer, end to end
- **Demo:** live Q&A over 3–5 sample PDFs

## Sprint 3 — Real ingestion pipeline
- `RAG-014` Swap parser to Unstructured/Docling
- `RAG-015` LlamaIndex ingestion/indexing integration
- `RAG-016` MinIO (local) / S3 (prod) for raw docs
- `RAG-017` Prefect flow: watch → parse → chunk → embed → upsert (idempotent)
- `RAG-018` Metadata extraction (source, page, doc type)
- `RAG-019` CI: testcontainers integration tests (real Postgres+pgvector in CI)
- `RAG-020` CI/CD: auto-deploy `main` → staging on merge
- **DoD:** handles scanned + table-heavy PDFs, reruns are idempotent
- **Demo:** drop messy doc in folder, watch it become searchable

## Sprint 4 — Hybrid search (part 1)
- `RAG-021` Stand up OpenSearch/Elasticsearch (compose + staging)
- `RAG-022` BM25 keyword index alongside pgvector
- `RAG-023` RRF fusion of dense + lexical results
- `RAG-024` Retrieval smoke-test suite (fixed queries → expected doc IDs)
- **DoD:** fused ranked list returned; smoke tests pass locally
- **Demo:** exact part-number/legal-term query nails it via keyword leg

## Sprint 5 — Hybrid search (part 2) + reranking
- `RAG-025` Cohere Rerank as final precision step
- `RAG-026` Tune fusion weights / rerank top-N
- `RAG-027` Wire smoke-test suite into CI as required check
- `RAG-028` Latency budget check (p95 target)
- **DoD:** CI blocks PRs that regress retrieval smoke tests
- **Demo:** vector-only vs. hybrid+rerank side by side on a tricky query

## Sprint 6 — Agentic orchestration (LangGraph)
- `RAG-029` LangGraph state machine: rewrite → retrieve → rerank → generate → self-check
- `RAG-030` Self-check node (re-retrieve if answer isn't grounded)
- `RAG-031` LangSmith/Langfuse tracing integration
- `RAG-032` Expose trace ID in API response
- **DoD:** full graph runs end-to-end, trace visible
- **Demo:** multi-hop ambiguous question, walk the trace step by step

## Sprint 7 — Evaluation harness (RAGAS)
- `RAG-033` Golden Q&A/context dataset (30–50 examples)
- `RAG-034` RAGAS wiring: faithfulness, answer relevance, context precision/recall
- `RAG-035` Baseline scoring run + stored thresholds
- `RAG-036` CI: RAGAS gate — fail PR below baseline
- **DoD:** CI blocks a deliberately regressed PR
- **Demo:** show the red run, then the fix going green

## Sprint 8 — Auth & multi-tenancy (part 1)
- `RAG-037` Users/orgs/roles schema in Postgres
- `RAG-038` Document-level ACL table + row-level security policies
- `RAG-039` JWT auth on FastAPI
  - _Optional alternative:_ **Firebase Auth** may be used for identity
    (signup/login/OAuth/token issuance) instead of hand-rolled JWT. If chosen,
    FastAPI verifies Firebase-issued tokens, but the document-level ACL
    (`RAG-038`) stays in Postgres — Firebase provides *identity*, Postgres
    decides *authorization*. Trade-off: faster auth, but adds a managed
    Google dependency, which slightly weakens the self-hosted enterprise story.
- `RAG-040` Retrieval filters by ACL before ranking
- **DoD:** two tenants exist with distinct document sets
- **Demo:** raw query showing ACL filter applied

## Sprint 9 — Auth & multi-tenancy (part 2)
- `RAG-041` Login/session flow on Next.js
- `RAG-042` Per-tenant namespace isolation (pgvector + OpenSearch)
- `RAG-043` Authz test suite: tenant A never sees tenant B's docs
- `RAG-044` CI: authz suite as required, non-negotiable check
- **DoD:** authz tests in CI, fail loudly on any leak
- **Demo:** two logged-in tenants, same question, provably different answers

## Sprint 10 — Streaming UX + caching
- `RAG-045` SSE streaming endpoint (FastAPI)
- `RAG-046` Vercel AI SDK token-by-token render (Next.js)
- `RAG-047` shadcn/ui chat components
- `RAG-048` Redis response caching + per-tenant rate limiting
- `RAG-049` Playwright e2e on streaming endpoint, added to CI
- **DoD:** e2e passes in CI, rate limit demonstrably triggers
- **Demo:** ChatGPT-style streaming, then hit the rate limit

## Sprint 11 — Incremental/live indexing
- `RAG-050` Webhook/poll watcher (S3/SharePoint/Drive)
- `RAG-051` Diff-based reindexing (only changed docs)
- `RAG-052` Delete/version handling without full reindex
- `RAG-053` CI/CD: staging → prod promotion gate (manual approval)
- `RAG-054` Nightly scheduled eval run against prod-like data
- **DoD:** edited doc reflected within ~2 min, no manual reindex
- **Demo:** edit a live doc, ask again, show the update

## Sprint 12 — Production hardening
- `RAG-055` Cost/latency/token dashboards from trace data
- `RAG-056` (optional) Kubernetes manifests + deploy
- `RAG-057` Qdrant as second vector-store backend (portability)
- `RAG-058` One-command documented rollback (redeploy prior tag)
- `RAG-059` Document full CI/CD pipeline end-to-end
- **DoD:** rollback tested once in staging
- **Demo:** dashboard walkthrough + live rollback
