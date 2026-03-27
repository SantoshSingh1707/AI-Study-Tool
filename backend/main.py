import os
import uuid
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import RAG engine components
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.data_loader import (
    process_single_pdf, process_single_txt, process_single_docx,
    process_single_pptx, split_document
)
from src.embedding import EmbeddingManager
from src.vector_store import VectorStore
from src.search import RAGRetrieval, generate_questions, generate_learning_content

# Try to import Mistral AI
try:
    from langchain_mistralai import ChatMistralAI
    HAS_MISTRAL = True
except ImportError:
    HAS_MISTRAL = False
    logger.warning("langchain_mistralai not installed - LLM features disabled")

# ============== Pydantic Models ==============

class QuizRequest(BaseModel):
    difficulty: str = Field(..., description="Easy, Medium, or Hard")
    num_questions: int = Field(5, ge=1, le=20)
    top_k: int = Field(10, ge=1, le=50)
    min_score: float = Field(0.2, ge=0.0, le=1.0)
    source_filter: Optional[List[str]] = Field(None)
    topic: Optional[str] = Field(None, max_length=200)
    question_types: List[str] = Field(["MCQ"])

class LearningRequest(BaseModel):
    mode: str = Field(..., description="Summary or Key Notes")
    top_k: int = Field(20, ge=1, le=50)
    source_filter: Optional[List[str]] = Field(None)
    topic: Optional[str] = Field(None, max_length=200)

class SourceInfo(BaseModel):
    source_file: str
    similarity_score: float
    page: Optional[int] = None
    content: str

class Question(BaseModel):
    type: str
    question: str
    options: List[str]
    answer: str
    explanation: str

class QuizResponse(BaseModel):
    questions: List[Question]
    sources: List[SourceInfo]

class LearningResponse(BaseModel):
    content: str
    sources: List[SourceInfo]

class HealthResponse(BaseModel):
    status: str
    documents_count: int
    available_sources: List[str]

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# ============== FastAPI App ==============

app = FastAPI(
    title="RAG Question Generator API",
    description="Backend API for AI-powered study tool",
    version="1.0.0"
)

# CORS configuration - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components (initialized on startup)
vectorstore: Optional[VectorStore] = None
embedding_manager: Optional[EmbeddingManager] = None
retriever: Optional[RAGRetrieval] = None
llm: Optional[ChatMistralAI] = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG components on startup"""
    global vectorstore, embedding_manager, retriever, llm

    try:
        # Get API key from environment
        mistral_api_key = os.getenv("MISTRAL_API_KEY")

        # Initialize embedding manager
        logger.info("Loading embedding model...")
        embedding_manager = EmbeddingManager(model_name="multi-qa-MiniLM-L6-cos-v1")

        # Initialize vector store
        logger.info("Initializing vector store...")
        vectorstore = VectorStore(
            collection_name="pdf_documents",
            persist_directory="data/vector_store"
        )

        # Initialize retriever
        retriever = RAGRetrieval(vectorstore, embedding_manager)

        # Initialize LLM if key provided
        if mistral_api_key and HAS_MISTRAL:
            logger.info("Initializing Mistral LLM...")
            llm = ChatMistralAI(
                model="mistral-small-2506",
                temperature=0.7,
                api_key=mistral_api_key
            )
        else:
            logger.warning("MISTRAL_API_KEY not set or langchain_mistralai not installed - LLM features disabled")

        logger.info("Backend startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    sources = vectorstore.get_available_sources() if vectorstore else []
    count = vectorstore.collection.count() if vectorstore and vectorstore.collection else 0
    return HealthResponse(
        status="healthy",
        documents_count=count,
        available_sources=sources
    )

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    if not vectorstore or not embedding_manager:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    # Validate file type
    allowed_extensions = {'.pdf', '.txt', '.docx', '.pptx'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save to temp directory
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir) / file.filename

    try:
        # Write uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process based on file type
        logger.info(f"Processing {file.filename}...")
        if file_ext == '.pdf':
            docs = process_single_pdf(str(temp_path))
        elif file_ext == '.txt':
            docs = process_single_txt(str(temp_path))
        elif file_ext == '.docx':
            docs = process_single_docx(str(temp_path))
        elif file_ext == '.pptx':
            docs = process_single_pptx(str(temp_path))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not docs:
            raise HTTPException(status_code=400, detail="Failed to extract text from document")

        # Split into chunks
        logger.info(f"Splitting {len(docs)} pages into chunks...")
        chunks = split_document(docs)

        if not chunks:
            raise HTTPException(status_code=400, detail="Document processed but no text chunks found")

        # Generate embeddings
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        texts = [c.page_content for c in chunks]
        embeddings = embedding_manager.generate_embeddings(texts)

        # Add to vector store
        logger.info("Adding to vector database...")
        vectorstore.add_documents(chunks, embeddings)

        return {
            "success": True,
            "message": f"Successfully processed {file.filename}",
            "chunks_added": len(chunks),
            "pages_processed": len(docs)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/api/documents")
async def list_documents():
    """List all available source documents"""
    if not vectorstore:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    sources = vectorstore.get_available_sources()
    count = vectorstore.collection.count()

    return {
        "sources": sources,
        "total_chunks": count
    }

@app.delete("/api/documents/{source_name}")
async def delete_document(source_name: str):
    """Delete a specific source document"""
    if not vectorstore:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    success = vectorstore.remove_source(source_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Source '{source_name}' not found")

    return {"success": True, "message": f"Deleted {source_name}"}

@app.post("/api/generate/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions from documents"""
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    if not llm:
        raise HTTPException(status_code=503, detail="LLM not configured. Set MISTRAL_API_KEY")

    # Validate available sources
    available_sources = vectorstore.get_available_sources()
    if not available_sources:
        raise HTTPException(status_code=400, detail="No documents found. Please upload a document first.")

    if request.source_filter:
        invalid = [s for s in request.source_filter if s not in available_sources]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid sources: {', '.join(invalid)}")

    try:
        logger.info(f"Generating {request.num_questions} questions...")
        result = generate_questions(
            difficulty=request.difficulty,
            retriever=retriever,
            llm=llm,
            num_questions=request.num_questions,
            top_k=request.top_k,
            min_score=request.min_score,
            source_filter=request.source_filter,
            topic=request.topic,
            question_types=request.question_types
        )

        if not result["questions"]:
            raise HTTPException(status_code=400, detail="No questions generated. Try adjusting your filters or topic.")

        return QuizResponse(
            questions=result["questions"],
            sources=result["sources"]
        )

    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/learning", response_model=LearningResponse)
async def generate_learning(request: LearningRequest):
    """Generate summaries or key notes from documents"""
    if not retriever:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    if not llm:
        raise HTTPException(status_code=503, detail="LLM not configured. Set MISTRAL_API_KEY")

    # Validate available sources
    available_sources = vectorstore.get_available_sources()
    if not available_sources:
        raise HTTPException(status_code=400, detail="No documents found. Please upload a document first.")

    if request.source_filter:
        invalid = [s for s in request.source_filter if s not in available_sources]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid sources: {', '.join(invalid)}")

    try:
        logger.info(f"Generating {request.mode}...")
        content = generate_learning_content(
            mode=request.mode,
            retriever=retriever,
            llm=llm,
            top_k=request.top_k,
            source_filter=request.source_filter,
            topic=request.topic
        )
        return LearningResponse(content=content, sources=[])

    except Exception as e:
        logger.error(f"Error generating learning content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
