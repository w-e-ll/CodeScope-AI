# DECISIONS.md

## Project Overview

CodeScope AI is a Retrieval-Augmented Generation (RAG) application
for understanding and documenting Python repositories.

The system ingests repository archives, analyzes source code structure,
creates semantic code chunks, stores embeddings in a vector database,
and answers natural language questions with grounded citations.

The focus of this implementation is engineering quality,
maintainability, observability, and production-minded architecture.


---

# Key Technical Decisions


## 1. ZIP-Based Repository Ingestion

### Decision

The application accepts repository ZIP archives instead of GitHub URLs.

### Why

- Easier local execution
- No GitHub authentication complexity
- Deterministic evaluation for reviewers
- Works offline
- Reduces API rate limit concerns
- Simplifies assignment setup

### Trade-Off

Does not automatically pull latest repository changes.


---

## 2. ChromaDB Instead of Pinecone

### Decision

Use local persistent ChromaDB as vector storage.

### Why

- Zero external infrastructure required
- Faster assignment setup
- Easier local debugging
- No cloud billing
- Better reproducibility for reviewers

### Production Alternative

For production deployment I would consider:

- Pinecone
- Weaviate
- OpenSearch
- pgvector
- Vertex AI Vector Search

depending on cloud strategy and scale.


---

## 3. AST-Based Python Analysis

### Decision

Python files are parsed with the built-in `ast` module.

### Why

- Reliable symbol extraction
- Accurate class/function boundaries
- Better semantic chunking
- Enables metadata extraction
- Avoids naive text splitting

### Extracted Metadata

- Classes
- Functions
- Async functions
- Imports
- Decorators
- Docstrings
- Line ranges


---

## 4. Semantic Chunking by Symbols

### Decision

Chunk Python code by functions/classes instead of fixed windows.

### Why

Semantic chunks produce significantly better retrieval quality
than arbitrary line windows.

This improves:

- grounding
- answer precision
- retrieval explainability
- documentation generation


---

## 5. Hybrid Chunking Strategy

### Decision

Different chunking strategies are used depending on file type.

### Python

- AST-based symbol chunking

### Documentation / Config Files

- line window chunking

### Why

Non-code files usually do not have reliable AST structures.


---

## 6. Local-First Architecture

### Decision

The assignment implementation is intentionally local-first.

### Why

- Simplifies execution
- Easier reviewer onboarding
- No infrastructure dependency
- Faster development iteration

### Production Evolution

In production I would split services into:

- ingestion workers
- embedding workers
- vector storage layer
- retrieval API
- frontend layer


---

## 7. Centralized Logging

### Decision

Logging is configured globally with per-file loggers.

### Why

- Consistent formatting
- Easier observability
- Centralized control
- Better production operations

### Logging Includes

- business events
- ingestion metrics
- retrieval metrics
- warnings
- exceptions
- retries
- vector operations


---

## 8. Extensive Exception Hierarchy

### Decision

Custom domain exceptions are used throughout the application.

### Why

- Cleaner error handling
- Better debugging
- Operational visibility
- Explicit failure domains
- Easier monitoring integration


---

## 9. Retry Decorator

### Decision

Retry logic is implemented as a reusable decorator.

### Why

- Reduces duplicated retry code
- Easier maintenance
- Consistent operational behavior
- Cleaner service implementations

### Applied To

- LLM requests
- embedding generation
- external operations


---

## 10. YAML + ENV Configuration

### Decision

Application settings are stored in YAML.
Secrets are stored in `.env`.

### Why

- Separates configuration from secrets
- Easier deployment
- Better security practices
- Environment portability

### Secrets

- OPENAI_API_KEY


---

## 11. Streamlit Frontend

### Decision

Use Streamlit for UI.

### Why

- Rapid development
- Strong Python integration
- Excellent for demos
- Easy local execution
- Good developer productivity

### Trade-Off

Not ideal for highly customized enterprise frontends.


---

## 12. Grounded RAG Responses

### Decision

The assistant answers only from retrieved repository context.

### Why

- Reduces hallucinations
- Improves trustworthiness
- Improves explainability
- Easier debugging

### Additional Safeguards

- explicit grounding instructions
- file citations
- retrieval debug tab
- bounded context size


---

## 13. Retrieval Debug Visibility

### Decision

Expose retrieval matches in the UI.

### Why

This significantly improves:

- observability
- debugging
- explainability
- trust in generated answers

Users can inspect:

- retrieved chunks
- similarity scores
- line ranges
- source files


---

## 14. Why OpenAI Models

### Decision

Use:
- `text-embedding-3-small`
- `gpt-4o-mini`

### Why

These models currently provide a strong balance between:

- cost
- latency
- quality
- API simplicity

### Future Improvements

Could evaluate:

- Claude Sonnet
- Gemini
- local embedding models
- local LLM inference


---

## 15. What Was Intentionally Skipped

The assignment intentionally does not include:

- authentication
- RBAC
- async distributed ingestion
- Kubernetes deployment
- CI/CD pipelines
- caching layer
- multi-user isolation
- advanced reranking
- hybrid BM25 retrieval
- graph retrieval
- repository incremental sync


---

# What I Would Improve With More Time


## Retrieval Quality

- add reranking
- hybrid retrieval
- repository graph relationships
- dependency-aware retrieval


## Scalability

- async ingestion pipeline
- distributed embedding workers
- queue-based processing
- horizontal vector storage scaling


## Security

- malware archive scanning
- stricter ZIP validation
- content sanitization
- upload quotas


## Observability

- OpenTelemetry
- Prometheus metrics
- tracing
- structured JSON logs
- token usage dashboards


## UI/UX

- repository graph visualization
- architecture diagrams
- code dependency explorer
- conversation history
- syntax-highlighted citations


## AI Quality

- answer evaluation framework
- prompt versioning
- benchmark datasets
- hallucination detection


---

# Engineering Standards Followed

- modular architecture
- separation of concerns
- centralized configuration
- centralized logging
- domain exceptions
- retries with backoff
- type hints
- docstrings
- deterministic ingestion
- observable retrieval
- defensive validation
- readable code style


---

# Engineering Standards Skipped

Due to assignment scope and time constraints:

- full unit test coverage
- integration test suite
- distributed architecture
- production authentication
- production deployment automation
- enterprise RBAC


---

# AI-Assisted Development

AI coding assistants were used to accelerate:

- scaffolding
- repetitive boilerplate
- architecture iteration
- documentation drafting

However:

- architecture decisions
- trade-offs
- operational design
- engineering standards
- repository structure
- RAG design choices

were intentionally reviewed and adjusted manually.

The goal was not to maximize generated code volume,
but to maintain consistent engineering quality and readability.
