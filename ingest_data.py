from src.data_loader import (
    process_all_pdf, process_all_txt, process_all_docx, process_all_pptx, split_document
)
from src.embedding import EmbeddingManager
from src.vector_store import VectorStore

def ingest_all_data():
    print("--- Starting Data Ingestion ---")
    
    # Initialize components
    # EmbeddingManager automatically uses GPU if available
    embedding_manager = EmbeddingManager(model_name="multi-qa-MiniLM-L6-cos-v1")
    vectorstore = VectorStore(
        collection_name="pdf_documents",
        persist_directory="data/vector_store"
    )
    
    all_docs = []
    
    # Process PDFs
    pdf_dir = "data/pdf"
    if os.path.exists(pdf_dir):
        print(f"Loading PDFs from {pdf_dir}...")
        all_docs.extend(process_all_pdf(pdf_dir))
    else:
        print(f"Directory {pdf_dir} does not exist. Skipping PDFs.")

    # Process TXT files
    txt_dir = "data/textfiles"
    if os.path.exists(txt_dir):
        print(f"Loading TXT files from {txt_dir}...")
        all_docs.extend(process_all_txt(txt_dir))
    else:
        print(f"Directory {txt_dir} does not exist. Skipping TXT files.")
        
    # Process DOCX files
    docx_dir = "data/docx"
    if os.path.exists(docx_dir):
        print(f"Loading DOCX files from {docx_dir}...")
        all_docs.extend(process_all_docx(docx_dir))
    else:
        print(f"Directory {docx_dir} does not exist. Skipping DOCX files.")

    # Process PPTX files
    pptx_dir = "data/pptx"
    if os.path.exists(pptx_dir):
        print(f"Loading PPTX files from {pptx_dir}...")
        all_docs.extend(process_all_pptx(pptx_dir))
    else:
        print(f"Directory {pptx_dir} does not exist. Skipping PPTX files.")
    
    if not all_docs:
        print("No documents found to process.")
        return
        
    print(f"Total documents to split: {len(all_docs)}")
    print("Splitting documents into chunks...")
    chunks = split_document(all_docs)
    
    if not chunks:
        print("No chunks generated.")
        return

    print(f"Generating embeddings for {len(chunks)} chunks...")
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)
    
    print("Adding chunks and embeddings to Vector Store...")
    vectorstore.add_documents(chunks, embeddings)
    
    print("--- Ingestion Complete ---")
    print("Available sources in DB:")
    for source in vectorstore.get_available_sources():
        print(f" - {source}")

if __name__ == "__main__":
    ingest_all_data()
