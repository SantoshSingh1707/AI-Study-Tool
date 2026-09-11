# RAG Question Generator

> Transform any document into interactive quizzes and study materials using AI

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-local?style=flat)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **Retrieval Augmented Generation (RAG)** application that converts your documents into personalized learning experiences. Upload PDFs, Word docs, or PowerPoint presentations and instantly generate interactive quizzes and comprehensive study notes — fully locally, with no API keys or cloud costs.

---

## ✨ Features

- 📄 **Multi-Format Upload** - PDF, TXT, DOCX, PPTX support
- 🤖 **AI-Powered Generation** - Quiz questions, summaries, key notes
- 🎯 **Smart RAG** - ChromaDB vector store with sentence-transformers
- 🖥️ **Fully Local LLM** - Runs on Ollama, no API keys or cloud costs
- 🎨 **Modern UI** - Streamlit interface with quiz engine and study modes

---

## 🏗️ Architecture

```
Streamlit UI (app.py) → RAG Engine (src/) → ChromaDB Vector Store + Local LLM (Ollama)
```

---

## 🚀 Quick Start

### For Users

1. Start the app (see below)
2. Upload a document (PDF, TXT, DOCX, or PPTX)
3. Configure quiz settings (difficulty, number of questions)
4. Generate and review questions
5. Or switch to "Learning" mode for summaries

### For Developers (Local)

#### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/) installed and running (local LLM, no API keys needed)
- Pull the Mistral 7B model once: `ollama pull mistral:7b`

#### App Setup

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/Mac

pip install -r requirements.txt

# Set local config (copy .env.example)
cp .env.example .env

# Launch the app
streamlit run app.py
```

App: http://localhost:8501

---

## 🛠️ Tech Stack

- Python 3.11 + Streamlit (UI)
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- LangChain + LangChain-Ollama (RAG orchestration + local LLM)
- Ollama with Mistral 7B (local LLM)

---

## 📁 Project Structure

```
Question-maker/
├── app.py             # Streamlit UI (main entry point)
├── src/               # RAG engine modules
│   ├── data_loader.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── search.py
├── scripts/           # Dev startup scripts (dev.ps1 / dev.sh)
├── notebook/          # Exploration notebooks
└── data/              # Local data & vector store
```

---

## 🔧 Configuration

Copy `.env.example` to `.env`:

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_MODEL` | No | Local Ollama model (default `mistral:7b`) |
| `OLLAMA_BASE_URL` | No | Ollama server URL (default `http://localhost:11434`) |

---

## 🧪 Testing

```bash
# Syntax check
python -m py_compile app.py src/*.py
```

---

## 🔍 Troubleshooting

### App shows "Error loading RAG components"
- ✅ Make sure Ollama is running (`ollama serve`) and `OLLAMA_BASE_URL` is correct
- ✅ The model has been pulled: `ollama pull mistral:7b`

### Generation fails
- ✅ Documents are uploaded first
- ✅ Ollama model is loaded (first call loads Mistral 7B into memory, may take a minute)
- ✅ Machine has enough RAM/VRAM for the 7B model

### Upload fails
- ✅ Format: PDF, TXT, DOCX, PPTX

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) (to be created) and submit PRs.

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## 📚 Documentation

- [Improvements](./IMPROVEMENTS.md)

---

Built with ❤️ for learners everywhere
