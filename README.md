# RAG Question Generator

> Transform any document into interactive quizzes, flashcards, and study materials using AI

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-027BBD?style=flat)](https://mistral.ai/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat)

A production-grade **Retrieval Augmented Generation (RAG)** application that converts your documents into personalized learning experiences. Upload PDFs, Word docs, or PowerPoint presentations and instantly generate interactive quizzes, flashcards, and comprehensive study notes powered by AI.

### 🌟 Dual-Interface Design

- **Full-Stack Application**: Modern React + FastAPI with glassmorphic UI (production-ready, Dockerized)
- **Streamlit Prototype**: Single-file app for rapid experimentation and development

---

## 📸 Screenshots

> *Full-Stack Quiz Interface*

> *Streamlit Prototype*

---

## ✨ Features

### 🎯 Core Learning Tools

- **Smart Quiz Generation** - AI-powered MCQ and True/False questions from your documents
- **Flashcard Mode** - Interactive spaced repetition for effective memorization
- **Exam Simulation** - Timed quizzes with no instant feedback (test your knowledge)
- **Study Notes** - Automatically generated summaries and key takeaways
- **Topic Focusing** - Target specific concepts or sections within documents
- **Performance Tracking** - Visual progress dashboard to monitor improvement

### 💎 Technical Highlights

- **RAG-Powered** - Retrieval-augmented generation for accurate, context-aware responses
- **Multi-Format Support** - PDF, TXT, DOCX, PPTX with OCR fallback for image-based PDFs
- **Vector Database** - ChromaDB with persistent storage and efficient similarity search
- **Offline Privacy** - All data stored locally; no external document sharing
- **Modern Stack** - React 18, TypeScript, FastAPI, Tailwind CSS, Zustand
- **Production Ready** - Docker deployment, health checks, comprehensive error handling
- **Responsive Design** - Works seamlessly on desktop and mobile devices

---

## 🚀 Quick Start

### Option 1: Docker (Recommended - 5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/RAG-Question-Generator.git
cd RAG-Question-Generator

# Configure environment
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY (get one free at https://console.mistral.ai)

# Start all services
docker-compose up -d

# Access the application:
# Frontend: http://localhost
# Backend API: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Option 2: Local Development (Full-Stack)

**Prerequisites:** Python 3.11+, Node.js 18+, Git

```bash
# 1️⃣ Backend Setup
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp ../.env .env  # Add your MISTRAL_API_KEY

# Start backend server (auto-reload enabled)
uvicorn main:app --reload --port 8000
# API docs will be at http://localhost:8000/docs

# 2️⃣ Frontend Setup (new terminal)
cd frontend
npm install
npm run dev
# Frontend will be at http://localhost:5173
```

### Option 3: Streamlit Prototype (All-in-One)

Perfect for quick testing without running multiple servers:

```bash
# Install dependencies
pip install streamlit

# Run the app
streamlit run app.py
# Opens at http://localhost:8501

# All-in-one: RAG engine, UI, and logic in a single file
```

---

## 📋 Prerequisites

### Required

- **Mistral AI API Key** - Free tier available at [console.mistral.ai](https://console.mistral.ai)
- **Docker** (for Option 1) or **Python 3.11+** (for Option 2/3)
- **Node.js 18+** (for Option 2, full-stack frontend)

### Optional

- **GPU** - Accelerates embedding generation (~10x faster). Install PyTorch with CUDA:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu118
  ```
- **CUDA-enabled GPU drivers** - For GPU acceleration

---

## 📦 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 + TypeScript | Modern UI framework |
| | Vite | Lightning-fast build tool |
| | Tailwind CSS | Utility-first styling |
| | Zustand | Lightweight state management |
| | React Query | Server state & caching |
| | Framer Motion | Smooth animations |
| **Backend** | FastAPI |Async Python web framework |
| | LangChain | LLM orchestration |
| | Pydantic | Data validation |
| | Uvicorn | ASGI server |
| **AI/ML** | Mistral AI (`mistral-small-2506`) | Large language model |
| | Sentence-Transformers | Embedding generation |
| | ChromaDB | Vector database |
| **Infrastructure** | Docker + Docker Compose | Containerization |
| | Nginx | Reverse proxy |
| | GitHub Actions | CI/CD |

---

## 📂 Project Structure

```
Question-maker/
├── frontend/                    # React + TypeScript SPA
│   ├── src/
│   │   ├── components/         # Reusable UI (Button, Card, etc.)
│   │   │   ├── layout/        # Layout wrapper
│   │   │   └── ui/            # Atomic components
│   │   ├── pages/             # Route components
│   │   │   ├── Home.jsx       # Dashboard
│   │   │   ├── Upload.jsx     # Document upload
│   │   │   ├── Quiz.jsx       # Interactive quiz interface
│   │   │   └── Learning.jsx   # Study notes generation
│   │   ├── store/             # Zustand global state
│   │   ├── services/          # API client
│   │   ├── hooks/             # React Query hooks
│   │   ├── types/             # TypeScript definitions
│   │   └── utils/             # Helpers
│   ├── Dockerfile
│   └── nginx.conf
│
├── backend/                     # FastAPI backend
│   ├── main.py                # API routes & server
│   ├── config.py              # Configuration constants
│   ├── middleware/            # Custom middleware
│   ├── routes/                # (Routes in main.py)
│   ├── tests/                 # pytest test suite
│   │   ├── test_api.py
│   │   ├── test_data_loader.py
│   │   ├── test_embedding.py
│   │   ├── test_vector_store.py
│   │   ├── test_search.py
│   │   └── test_validation.py
│   ├── data/                  # Persistent storage (Docker volume)
│   │   ├── vector_store/      # ChromaDB (auto-created)
│   │   └── uploads/           # Uploaded docs (optional)
│   ├── requirements.txt
│   ├── requirements-test.txt
│   ├── pytest.ini
│   └── Dockerfile
│
├── src/                        # Shared RAG engine (library)
│   ├── data_loader.py         # Document loaders (PDF, TXT, DOCX, PPTX)
│   ├── embedding.py           # SentenceTransformer wrapper
│   ├── vector_store.py        # ChromaDB interface + deduplication
│   └── search.py              # RAG retrieval & generation logic
│
├── data/                       # Streamlit prototype data
│   ├── pdf/, txt/, docx/, pptx/  # Sample documents (git-tracked examples)
│   └── vector_store/              # ChromaDB (git-ignored)
│
├── app.py                      # Single-file Streamlit prototype
├── docker-compose.yml          # Full-stack orchestration
├── pyproject.toml              # Project metadata
├── uv.lock                    # Dependency lock (Python)
├── package-lock.json          # Dependency lock (Node.js)
├── .pre-commit-config.yaml    # Pre-commit hooks
├── CLAUDE.md                  # Claude Code guide
├── DEPLOYMENT.md              # Production deployment
│
└── [Documentation]
    ├── README.md              # This file
    ├── GITHUB_EXCLUDE.md      # Git safety guidelines
    ├── IMPROVEMENTS.md        # Changelog
    ├── TESTING.md             # Testing guide
    ├── TESTING_SUMMARY.md     # Test coverage report
    ├── MIGRATION_SUMMARY.md   # Migration notes
    ├── PREVIEW.md             # Feature preview
    └── COMPLETE_SUMMARY.md    # Project summary
```

---

## 🔧 API Reference

The FastAPI backend provides a RESTful API consumed by the frontend.

### Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/health` | Health check with statistics | None |
| `POST` | `/api/upload` | Upload document (PDF, TXT, DOCX, PPTX) | `file: UploadFile` |
| `GET` | `/api/documents` | List all source documents | None |
| `DELETE` | `/api/documents/{name}` | Delete a source document | None |
| `POST` | `/api/generate/quiz` | Generate quiz questions | `QuizRequest` |
| `POST` | `/api/generate/learning` | Generate summaries/key notes | `LearningRequest` |

### Interactive Documentation

When the backend is running, explore the live API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## 🎯 Usage Guide

### 1. Upload a Document

- Click **Upload** in the sidebar or navigate to `/upload`
- Supported formats: **PDF** (text or scanned with OCR), **TXT**, **DOCX**, **PPTX**
- Max file size: **50MB**
- The document is automatically processed, chunked, and embedded into ChromaDB

### 2. Configure Quiz Settings

- **Number of Questions**: 1-15
- **Difficulty**: Easy (factual), Medium (understanding), Hard (analysis)
- **Question Types**: Multiple Choice, True/False, or mixed
- **Source Filter**: Select specific documents (if multiple uploaded)
- **Topic Focus**: Optional - target a specific concept (max 200 chars)

### 3. Choose Learning Mode

- **Quiz Mode**: Interactive questions with instant feedback
- **Exam Mode**: Timed quiz with results only at the end
- **Flashcard Mode**: One question at a time, reveal on demand
- **Learning Hub**: Generate summaries or key notes

### 4. Review & Track Progress

- Performance analytics in the sidebar
- Download quiz results as CSV
- View sources that informed each question

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (or `backend/` for Docker):

```bash
# Required
MISTRAL_API_KEY=your_api_key_here

# Optional (defaults shown)
# EMBEDDING_MODEL=multi-qa-MiniLM-L6-cos-v1
# LLM_MODEL=mistral-small-2506
# LLM_TEMPERATURE=0.7
```

### RAG Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| `top_k` | Frontend slider / `/api/generate/*` | 10 | Number of context chunks to retrieve |
| `min_score` | Frontend slider | 0.2 | Similarity threshold (0.0-1.0) |
| `num_questions` | Frontend slider / API | 5 | Questions to generate |
| `max_questions` | Backend | 20 | Hard limit |

**Adjusting these affects:**
- Lower `min_score` → More results (including less relevant ones)
- Higher `top_k` → More context, more detailed answers (but slower)
- Too many questions → May cause repetition, stick to 1-15

---

## 🧪 Testing

### Run All Tests

```bash
# Backend + Frontend (recommended)
python run_tests.py

# With coverage report
python run_tests.py --coverage
```

### Backend Only (pytest)

```bash
cd backend
make install      # Install runtime + test deps
make test         # Run all tests
make test-unit    # Unit tests only (mocked)
make test-integration  # Integration tests (real API calls)
make test-coverage    # Coverage report
```

### Frontend Only (Vitest)

```bash
cd frontend
make install
make test         # Single run
make test:watch   # Watch mode
make test:coverage # Coverage report
make test:ui      # Visual test runner (if installed)
```

### Test Coverage

- **Backend**: ~85% coverage on core modules
- **Frontend**: Component tests with React Testing Library + MSW mocking
- **Tests include**: API endpoints, data loaders, embedding manager, vector store, search logic

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build images (first time)
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Production Deployment

For production deployment with SSL, Nginx configuration, and environment hardening, see **[DEPLOYMENT.md](./DEPLOYMENT.md)**.

---

## 🔒 Security & Privacy

### What Data Is Stored Where?

| Data Type | Location | Shared? |
|-----------|----------|---------|
| Uploaded documents | `backend/data/pdf/`, `docx/`, `pptx/` | No (local only) |
| Vector embeddings | `backend/data/vector_store/` | No (local only) |
| Quiz history | Frontend localStorage | No |
| API requests | Logged by backend (optional) | No |

**Privacy Guarantee**: No data is sent to external servers except Mistral AI for LLM inference (API key required). Documents never leave your infrastructure.

### Security Best Practices

1. **Never commit `.env`** - Already in `.gitignore`
2. **Rotate API keys** if accidentally exposed
3. **Use strong API keys** and restrict usage on Mistral AI dashboard
4. **Enable HTTPS** in production (see DEPLOYMENT.md)
5. **Set file upload limits** (default 50MB)

---

## 🛠️ Development

### Adding a New Document Type

Example: Adding `.xlsx` support

1. Add loader in `src/data_loader.py`:
   ```python
   def process_single_xlsx(file_path: str) -> List[Document]:
       # Implementation
   ```

2. Update `backend/main.py` allowed extensions:
   ```python
   allowed_extensions = {'.pdf', '.txt', '.docx', '.pptx', '.xlsx'}
   ```

3. Update frontend uploader (if needed)

4. Add tests in `backend/tests/test_data_loader.py`

5. Update this README

### Pre-commit Hooks

```bash
# Install (run once)
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

Hooks automatically run:
- **black** (Python formatting)
- **ruff** (Python linting)
- **isort** (Import sorting)
- **mypy** (Type checking)
- **typescript-eslint** (TypeScript linting)
- **prettier** (Markdown/JSON/JS formatting)

---

## 🚧 Known Limitations

- **LLM API required** - Mistral AI key needed for quiz/note generation (free tier available)
- **Large documents** - >100 pages may be slow to process (consider splitting)
- **OCR fallback** - EasyOCR is CPU-bound; ~10-30 seconds per page
- **First-run download** - Embedding model (~100MB) downloads automatically
- **Document quality** - Poor quality scans may produce inaccurate questions
- **Context window** - LLM has token limits; very long docs may be truncated

---

## 📈 Future Enhancements

See [`IMPROVEMENTS.md`](./IMPROVEMENTS.md) for:
- Planned features
- Recent changes
- Technical debt items
- Performance improvements

Some upcoming ideas:
- [ ] Image-based question generation
- [ ] Multi-language support
- [ ] Video transcript processing
- [ ] Collaborative study groups
- [ ] Spaced repetition algorithm
- [ ] Export to Anki/Quizlet format

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python run_tests.py`
5. Ensure pre-commit hooks pass
6. Commit: `git commit -m "Add amazing feature"`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

- **Backend**: black (88 char), ruff, isort, mypy (type hints required)
- **Frontend**: ESLint + Prettier (auto-fix on save recommended)
- **Commits**: Conventional Commits format: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, etc.

### PR Checklist

- [ ] Tests added/updated for new functionality
- [ ] All tests passing (`python run_tests.py`)
- [ ] Linting passes (pre-commit)
- [ ] README updated if user-facing changes
- [ ] No sensitive data in code/tests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Mistral AI** - For the powerful and accessible LLM API
- **LangChain** - RAG orchestration framework
- **ChromaDB** - Vector database with excellent Python integration
- **SentenceTransformers** - Quality embedding models
- **React & FastAPI communities** - Amazing documentation and tools

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [**CLAUDE.md**](./CLAUDE.md) | Guide for Claude Code AI assistant |
| [**DEPLOYMENT.md**](./DEPLOYMENT.md) | Production deployment guide |
| [**GITHUB_EXCLUDE.md**](./GITHUB_EXCLUDE.md) | Git safety & excluded files |
| [**TESTING.md**](./TESTING.md) | Testing strategies & coverage |
| [**IMPROVEMENTS.md**](./IMPROVEMENTS.md) | Changelog & roadmap |
| [**API Docs**](http://localhost:8000/docs) | Live API reference (when running) |

---

## ❓ FAQ

**Q: Do I need an API key?**
A: Yes, a Mistral AI API key is required for quiz/note generation. Get one free at [console.mistral.ai](https://console.mistral.ai).

**Q: Can I use OpenAI instead of Mistral?**
A: The codebase is built for Mistral AI. Porting to OpenAI would require changing the LLM initialization in `src/embedding.py` and `backend/main.py`.

**Q: Are my documents stored in the cloud?**
A: No. All documents and embeddings are stored locally on your machine (or server). Only the LLM inference queries are sent to Mistral's API.

**Q: How do I clear all data?**
A: Delete the `data/` directory (Streamlit) or `backend/data/` (full-stack). The vector store will be recreated empty on next startup.

**Q: Can I run without Docker?**
A: Yes! See "Option 2: Local Development" above. Just install Python 3.11+, Node.js 18+, and run the backend and frontend separately.

**Q: What's the difference between the two frontends?**
A: The full-stack (`frontend/` + `backend/`) is production-ready with TypeScript, state management, and proper separation. The Streamlit app (`app.py`) is a single-file prototype good for quick demos and RAG development without managing two servers.

**Q: How accurate are the generated questions?**
A: Quality depends on document clarity and the `top_k`/`min_score` settings. Generally 80-90% accuracy for well-formatted documents. Always review questions before using for assessments.

---

<div align="center">

**Built with ❤️ for learners and educators**

If this project helps you, consider giving it a ⭐!

[Report Bug](https://github.com/yourusername/RAG-Question-Generator/issues) • [Request Feature](https://github.com/yourusername/RAG-Question-Generator/issues)

</div>
