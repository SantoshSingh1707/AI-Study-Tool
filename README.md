# 🎓 Ultimate Study Tool: RAG-Powered Quiz Platform

A professional-grade **Retrieval Augmented Generation (RAG)** study application that transforms your documents into interactive quizzes, flashcards, and exam simulations.

Built with **Streamlit**, **LangChain**, **ChromaDB**, and **Mistral AI**, this platform features a premium glassmorphic UI, modern analytics, and advanced learning modes.

## 🚀 Key Learning Features

✅ **Interactive Quiz Engine**: Generate and take quizzes with real-time scoring and persistent state.  
✅ **Mixed Question Types**: Support for Multiple Choice (MCQ) and True/False questions.  
✅ **Advanced Study Modes**:
  - **Exam Mode**: Timed sessions with hidden feedback to simulate real testing conditions.
  - **Flashcard Mode**: Focused memorization with a dedicated "flip-to-reveal" interface.
✅ **Topic Focusing**: Target specific concepts within your documents (e.g., "Internal Combustion Engine").  
✅ **Performance Analytics**: Visual dashboard tracking your score history across documents.  
✅ **Deep Learning Interaction**: "Ask a Follow-up" for AI-powered clarifications on any question.  
✅ **Multi-format Ingestion**: Support for PDF, TXT, and **DOCX** documents.  
✅ **OCR Fallback**: Automated text extraction for scanned or image-based PDFs.  
✅ **Exportable Study Sets**: Download your generated quizzes as CSV files for Anki or Quizlet.

## 🎨 Premium UX
- **Modern Design**: Sleek dark-themed UI with glassmorphism and elegant typography (Outfit/Inter).
- **Gamified Progress**: Live progress bars and celebration animations for mastery.
- **Source Transparency**: Clickable citations with similarity scores for every question.

## 📦 Core Stack

- **Frontend**: `Streamlit` (Custom CSS with Glassmorphism)
- **Orchestration**: `LangChain` & `Mistral AI` (`mistral-small-2506`)
- **Embeddings**: `Sentence-Transformers` (`multi-qa-MiniLM-L6-cos-v1`)
- **Database**: `ChromaDB` (Vector Store)
- **OCR**: `EasyOCR` & `PyMuPDF` (Fitz)
- **Logic**: Python 3.11+, `DOCX2TXT` for Word support.

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SantoshSingh1707/RAG-Learning.git
   cd RAG-Learning
   ```

2. **Setup Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📂 Project Structure

```
RAG-Learning/
├── app.py                  # Premium Study Platform UI
├── ingest_data.py          # CLI Bulk Ingestion Tool
├── src/                    # Core Logic
│   ├── data_loader.py      # PDF/TXT/DOCX/OCR loaders
│   ├── embedding.py        # Embedding management
│   ├── vector_store.py     # ChromaDB interface
│   └── search.py           # MCQ/Flashcard generation logic
├── data/
│   └── vector_store/      # Persistent Vector Database
└── brain/                  # Task & Implementation Artifacts
```

## 🔧 Usage

1. **Launch the platform**:
   ```bash
   streamlit run app.py
   ```
2. **Upload Documents**: Use the sidebar to add PDFs, Word files, or Text.
3. **Configure Your Session**:
   - Select difficulty (Easy/Medium/Hard).
   - Choose question types (MCQ/True-False).
   - Set a topic focus (optional).
4. **Study**: Toggle between **Exam Mode** or **Flashcards** to master your content.

## 📝 Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Source Chunks | 10 | Context length used for generation |
| Similarity | 0.25 | Search strictness (0-1) |
| Questions | 5 | Total items in the quiz (up to 15) |

## 📄 License & Credits

Created by **Santosh**  
Final Platform Version: **March 13, 2026**

*Educational project demonstrating production-grade RAG and LLM applications.*
