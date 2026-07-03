# 🧠 CodeScope AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-RAG-412991?style=for-the-badge&logo=openai&logoColor=white)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-6E44FF?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Observability](https://img.shields.io/badge/Observability-Enabled-00C853?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Code_Assistant-orange?style=for-the-badge)

</div>

<div align="center">

AI-powered Code Documentation Assistant with Retrieval-Augmented Generation (RAG), semantic code understanding, repository analysis, observability, and grounded codebase Q&A.

</div>

---

# 📚 Overview

CodeScope AI is a fullstack AI application that analyzes software repositories and allows engineers to:

- upload repository archives;
- semantically analyze source code;
- generate vector embeddings;
- retrieve relevant code context;
- ask natural language questions about the codebase;
- generate project-level technical documentation;
- inspect retrieval/debug information;
- understand architecture and operational flow.

The platform was designed with a strong focus on:

- engineering quality;
- maintainability;
- observability;
- scalability;
- production-minded architecture;
- operational transparency.

This project intentionally focuses on:
- clean architecture;
- reliable ingestion;
- semantic retrieval quality;
- grounded AI responses;
- debugging visibility;
- production-oriented design decisions.

---

# 🚀 Main Features

## 📦 Repository ZIP Upload

Upload GitHub repositories or local projects as ZIP archives.

Supported examples:

- Python repositories
- AI projects
- Backend services
- Infrastructure repositories
- DevOps repositories
- Configuration-heavy projects

---

# ✨ Why CodeScope AI Exists

Modern repositories grow faster than engineers can understand them.

CodeScope AI was designed to reduce engineering onboarding time,
improve repository discoverability, and provide grounded AI-assisted
software understanding workflows.

Instead of acting as a generic chatbot, the platform focuses on:

- repository intelligence;
- operational explainability;
- semantic code understanding;
- engineering observability;
- grounded technical answers.

The goal is to make large repositories easier to operate,
debug, document, and evolve.

---

## 🧠 Semantic Code Understanding

The system understands:

- Python classes
- functions
- async functions
- decorators
- imports
- repository structure
- configuration files
- Docker files
- Markdown documentation

---

## 🔎 AI Codebase Chat

Example questions:

```text
Where is logging configured?
How does retry logic work?
Which files implement vector retrieval?
What is the ingestion flow?
How are embeddings generated?
Which services interact with ChromaDB?
How is exception handling implemented?
```

---

## 📄 AI Documentation Generation

Generate:

- project-level documentation
- file-level technical summaries
- architecture explanations
- ingestion flow explanations
- RAG flow explanations

---

## 🧩 Retrieval Debug Visibility

The UI exposes:

- retrieved chunks
- similarity scores
- source files
- line ranges
- retrieved symbols

This greatly improves:

- explainability
- trustworthiness
- observability
- debugging

---

# 🏗️ Architecture

```text
ZIP Repository Upload
        ↓
Archive Extraction
        ↓
Repository Discovery
        ↓
Source File Reading
        ↓
AST-Based Python Analysis
        ↓
Semantic Chunking
        ↓
Embedding Generation
        ↓
Vector Storage (ChromaDB)
        ↓
Semantic Retrieval
        ↓
Prompt Construction
        ↓
LLM Answer Generation
        ↓
Grounded Response + Citations
```

---

# 🧭 High-Level Architecture

```text
                ┌───────────────────────┐
                │   Streamlit Frontend  │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   Answer Service      │
                └──────────┬────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    ┌────────────────┐         ┌────────────────┐
    │   Retriever     │         │ Prompt Builder │
    └────────┬───────┘         └────────┬───────┘
             │                           │
             ▼                           ▼
    ┌────────────────┐         ┌────────────────┐
    │   ChromaDB      │         │    OpenAI LLM  │
    └────────────────┘         └────────────────┘


                   INGESTION PIPELINE
    
                      ZIP Upload
                          │
                          ▼
                      Archive Loader
                          │
                          ▼
                      File Discovery
                          │
                          ▼
                      Source Reader
                          │
                          ▼
                      AST Chunker
                          │
                          ▼
                      Embedding Client
                          │
                          ▼
                      Vector Store

---

# 📂 Project Structure

```text
CodeScope-AI/
│
├── codescope_ai/
│   ├── app/
│   │   ├── core/
│   │   │   ├── app_config.py
│   │   │   ├── exceptions.py
│   │   │   ├── retry.py
│   │   │   └── setup_logger.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── archive_loader.py
│   │   │   ├── file_discovery.py
│   │   │   ├── source_file_reader.py
│   │   │   └── code_chunker.py
│   │   │
│   │   ├── rag/
│   │   │   ├── embedding_client.py
│   │   │   ├── vector_store.py
│   │   │   ├── retriever.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── llm_client.py
│   │   │   └── answer_service.py
│   │   │
│   │   ├── documentation/
│   │   │   ├── file_documenter.py
│   │   │   └── project_documenter.py
│   │   │
│   │   └── ui/
│   │       └── streamlit_app.py
│   │
│   └── main.py
│
├── etc/
│   └── codescope_ai_config.yml
│
├── var/
│   ├── input_data/
│   ├── extracted_archives/
│   ├── vector_db/
│   ├── generated_docs/
│   ├── generated_answers/
│   └── log/
│
├── tests/
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── Makefile
├── README.md
├── DECISIONS.md
└── .env.example
```

---

# 🧠 Supported File Types

The platform currently supports:

```text
.py
.md
.txt
.yml
.yaml
.toml
.json
.sql
.ini
.cfg
Dockerfile
Makefile
requirements.txt
README.md
```

---

# 🧠 Repository Intelligence Design

The system intentionally analyzes repositories semantically instead of
treating source code as plain text.

The ingestion pipeline extracts:

- class boundaries;
- function boundaries;
- async execution paths;
- decorators;
- imports;
- docstrings;
- repository structure;
- configuration relationships.

This allows retrieval to operate on meaningful engineering units
instead of arbitrary text windows.

As a result:
- retrieval precision improves;
- hallucinations decrease;
- documentation quality improves;
- architecture understanding becomes more accurate.

---

# 📈 Scalability Strategy

The current implementation is intentionally optimized for:

- assignment simplicity;
- local execution;
- engineering clarity;
- deterministic evaluation.

However the architecture was designed to evolve toward distributed processing.

Future scaling strategy:

## Phase 1

Single-node deployment:

- Streamlit
- ChromaDB
- OpenAI APIs

## Phase 2

Service decomposition:

- ingestion workers
- embedding workers
- retrieval API
- vector database cluster

## Phase 3

Enterprise deployment:

- Kubernetes
- Redis queues
- distributed workers
- repository caching
- multi-tenant architecture
- observability stack
- autoscaling inference gateways

---

# 📊 Observability Philosophy

The system was intentionally designed with operational visibility in mind.

Every major operation emits logs:

- archive ingestion;
- repository discovery;
- chunk generation;
- embedding requests;
- retrieval matches;
- vector operations;
- retries;
- exceptions;
- LLM interactions.

The Retrieval Debug tab exists specifically to improve:

- explainability;
- debugging;
- trustworthiness;
- operational transparency.

In production I would extend this with:

- OpenTelemetry tracing;
- Prometheus metrics;
- Grafana dashboards;
- token usage monitoring;
- latency monitoring;
- distributed tracing.

---

# 🎨 Why Streamlit

Streamlit was selected intentionally for the assignment because it enables:

- rapid iteration;
- fast prototyping;
- Python-native integration;
- simplified local deployment;
- quick demonstration workflows.

For enterprise production systems I would likely move toward:

- React / Next.js frontend;
- FastAPI backend APIs;
- async service boundaries;
- dedicated authentication layer.

---

# 🧪 Testing

The project includes pytest-based coverage for:

- configuration loading;
- retry logic;
- archive extraction;
- repository discovery;
- source reading;
- semantic chunking;
- vector storage;
- prompt generation;
- answer generation.

Run tests:

```bash
pytest tests -v
```

---

# 🐳 Docker Compose

Run full stack:

```bash
docker-compose up --build

Detached mode:

docker-compose up -d

Stop:

docker-compose down
```

---

# 🤖 Future AI Improvements

Potential future enhancements:

- hybrid retrieval (BM25 + vector search);
- reranking models;
- repository graph retrieval;
- dependency-aware retrieval;
- long-context repository summarization;
- architecture diagram generation;
- code change impact analysis;
- pull request intelligence;
- AI onboarding workflows;
- repository risk analysis.

---

# ⚙️ How Repository Analysis Works

## 1. Archive Upload

The user uploads a repository ZIP archive.

Example:

```text
your-repository-main.zip
```

---

## 2. Safe Extraction

The archive loader:

- validates ZIP integrity;
- validates paths;
- blocks unsafe traversal paths;
- extracts into isolated workspace.

---

## 3. Repository Discovery

The system recursively scans repository files.

Ignored:

```text
.git
.venv
node_modules
__pycache__
dist
build
```

---

## 4. Source Reading

Each supported text file is:

- validated;
- safely decoded;
- hashed;
- analyzed.

---

## 5. Python AST Analysis

Python files are parsed with:

```python
ast.parse()
```

Extracted symbols:

- classes
- functions
- async functions
- decorators
- imports
- docstrings

---

## 6. Semantic Chunking

Python:

```text
chunk by symbols/classes/functions
```

Non-Python:

```text
chunk by line windows
```

This significantly improves retrieval quality.

---

## 7. Embedding Generation

Embeddings are generated using:

```text
text-embedding-3-small
```

---

## 8. Vector Storage

Embeddings are stored in:

```text
ChromaDB
```

with persistent local storage.

---

## 9. Retrieval

User questions are converted into embeddings and matched semantically against stored chunks.

---

## 10. AI Answering

Retrieved chunks are inserted into grounded prompts.

The LLM answers only from repository context.

---

# 🖥️ UI Tabs

## Upload & Index

Upload and analyze repositories.

---

## Chat With Codebase

Ask questions about repository internals.

---

## Generate Docs

Generate AI project documentation.

---

## Retrieval Debug

Inspect:
- retrieved chunks;
- similarity scores;
- source citations;
- retrieval evidence.

---

# 🧪 Example Questions

```text
Where is vector retrieval implemented?

How does retry logic work?

What configuration system is used?

How are embeddings generated?

How does the ingestion pipeline work?

Which files handle exceptions?

How does the Streamlit UI communicate with retrieval services?

What would be required to productionize this application?
```

---

# 🛠️ Installation

# Linux

## 1. Clone Repository

```bash
git clone https://github.com/w-e-ll/CodeScope-AI.git
cd CodeScope-AI
```

---

## 2. Create Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Create `.env`

```bash
cp .env.example .env
```

Example:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 5. Run Streamlit

```bash
streamlit run codescope_ai/app/ui/streamlit_app.py
```

---

# Windows

## 1. Create Virtual Environment

```powershell
python -m venv .venv
```

---

## 2. Activate Environment

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Run Application

```powershell
streamlit run codescope_ai/app/ui/streamlit_app.py
```

---

# macOS

## 1. Create Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 2. Install

```bash
pip install -r requirements.txt
```

---

## 3. Run

```bash
streamlit run codescope_ai/app/ui/streamlit_app.py
```

---

# 🐳 Docker Deployment

# Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "codescope_ai/app/ui/streamlit_app.py", "--server.address=0.0.0.0"]
```

---

# Build Docker Image

```bash
docker build -t codescope-ai .
```

---

# Run Docker Container

```bash
docker run -p 8501:8501 \
-e OPENAI_API_KEY=your_openai_api_key \
codescope-ai
```

---

# Access Application

```text
http://localhost:8501
```

---

# ☁️ Production Deployment Considerations

---

# 🖥️ Small Prototype Deployment

Good for:
- assignment;
- demos;
- 1–5 users;
- local testing.

Recommended:

```text
CPU: 2–4 cores
RAM: 8 GB
Disk: 20 GB SSD
Vector DB: local ChromaDB
```

Infrastructure:

```text
Laptop / small Linux VM
```

---

# 🏢 Internal Team Deployment

Good for:
- 10–100 users;
- internal engineering assistant;
- CI/CD repository analysis.

Recommended:

```text
CPU: 8 vCPU
RAM: 32 GB
Disk: 100–200 GB SSD
Database: PostgreSQL
Queue: Redis
Workers: Celery
```

Recommended architecture:

```text
Frontend: Streamlit or React
Backend API: FastAPI
Workers: Celery
Vector DB: Qdrant
Storage: S3
```

---

# 🌍 Enterprise / 1000+ Users

Recommended architecture:

```text
Frontend: React / Next.js
API: FastAPI / Django
Workers: Kubernetes jobs
Queue: Redis / RabbitMQ
Vector DB: Qdrant / Pinecone
Metadata DB: PostgreSQL
Storage: S3 / MinIO
Monitoring: Prometheus + Grafana + Loki
Authentication: OAuth2 / SSO
```

---

# 💰 Cost Considerations

---

# 1 User / Local Prototype

Typical usage:

```text
1–5 repositories/day
```

Estimated cost:

```text
Very low
Usually only a few dollars/month
```

---

# 100 Users

Typical usage:

```text
100–1000 repository analyses/day
```

Main cost drivers:

- embeddings
- LLM responses
- storage

Recommended:

```text
Use caching
Reuse embeddings
Avoid reprocessing identical repositories
```

---

# 1000 Users

At this scale:

```text
LLM cost becomes major operational concern
```

Important optimizations:

- repository deduplication
- embedding caching
- hybrid retrieval
- chunk filtering
- async processing
- background indexing
- rate limiting

---

# 🤖 Model Selection

## Embedding Model

Current:

```text
text-embedding-3-small
```

Why:

- strong quality/cost balance;
- low latency;
- inexpensive.

---

## LLM Model

Current:

```text
gpt-4o-mini
```

Why:

- strong reasoning;
- good code understanding;
- affordable;
- fast.

---

# Better Models for Production?

## Higher Quality

```text
Claude Sonnet
GPT-4.1
Gemini 2.5 Pro
```

Better:
- architecture reasoning;
- long-context analysis;
- documentation quality.

More expensive.

---

## Cheaper Models

```text
GPT-4o-mini
Gemini Flash
small local LLMs
```

Better for:
- internal tools;
- bulk documentation;
- retrieval summaries.

---

# 🔍 What the Assignment Actually Wants

This assignment is not only about building a chatbot.

The reviewers mainly want to evaluate:

- engineering thinking;
- architecture quality;
- tradeoff decisions;
- maintainability;
- observability;
- operational awareness;
- production mindset;
- AI engineering maturity.

They specifically mentioned:

```text
Chunking
Embedding strategy
Retrieval approach
Prompt engineering
Context management
Guardrails
Quality controls
Observability
Scalability
Engineering excellence
AI-assisted development process
```

This project intentionally focuses heavily on those areas.

---

# 📈 Production Improvements

With more time I would add:

- hybrid retrieval (BM25 + vectors)
- reranking
- repository graph relationships
- background workers
- async indexing
- OpenTelemetry tracing
- Prometheus metrics
- conversation memory
- repository incremental sync
- GitHub integration
- authentication/RBAC
- syntax-aware reranking
- evaluation framework
- benchmark datasets

---

# 🔐 Security Considerations

Future production improvements:

- malware ZIP scanning
- upload quotas
- RBAC
- SSO/OAuth2
- prompt injection protection
- repository isolation
- encrypted storage
- PII filtering
- secret scanning

---

# 📊 Observability

The system logs:

- ingestion events
- chunking metrics
- embedding requests
- retrieval matches
- vector DB operations
- retries
- warnings
- exceptions
- LLM requests

Future production monitoring:

```text
Prometheus
Grafana
Loki
OpenTelemetry
ELK
Splunk
```

---

# 🧱 Engineering Standards Followed

- modular architecture
- centralized configuration
- centralized logging
- typed models
- custom exception hierarchy
- retries with backoff
- semantic chunking
- grounded RAG
- defensive validation
- observability-first design
- readable code style
- production-oriented structure

---

# 🧠 AI-Assisted Development

AI coding assistants were used to accelerate:

- scaffolding;
- repetitive boilerplate;
- architectural iteration;
- documentation drafting.

However:
- architecture decisions;
- repository structure;
- observability strategy;
- RAG flow;
- chunking strategy;
- operational design;
- production tradeoffs;

were intentionally reviewed and refined manually.

---

# 📌 Final Engineering Goal

The long-term vision is to evolve CodeScope AI into an engineering intelligence platform capable of:

- understanding large codebases;
- assisting onboarding;
- generating technical documentation;
- accelerating debugging;
- improving repository observability;
- supporting engineering teams with grounded AI workflows.

The core engineering idea:

```text
AI becomes significantly more useful when integrated into operational engineering workflows instead of acting as an isolated chatbot.
```
