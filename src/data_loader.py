from pathlib import Path
from typing import List, Any
from langchain_core.documents import Document

try:
    from langchain_community.document_loaders import PyMuPDFLoader,PyPDFLoader
except ImportError:
    pass
    
try:
    from langchain_community.document_loaders import Docx2txtLoader, TextLoader
    from langchain_community.document_loaders.excel import UnstructuredExcelLoader
    from langchain_community.document_loaders import JSONLoader
except ImportError:
    pass

def extract_text_with_ocr(file_path: str):
    """Fallback OCR method for image-based PDFs using EasyOCR and PyMuPDF"""
    print(f"Applying OCR fallback to {Path(file_path).name}...")
    try:
        import fitz # PyMuPDF
        import easyocr
        import numpy as np
        
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        doc = fitz.open(file_path)
        documents = []
        
        for i in range(len(doc)):
            page = doc[i]
            pix = page.get_pixmap(dpi=150)
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            
            if pix.n == 4:
                import cv2
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
                
            result = reader.readtext(img_array, detail=0)
            content = " ".join(result)
            
            if content.strip():
                metadata = {
                    'source': str(file_path),
                    'page': i,
                    'source_file': Path(file_path).name,
                    'file_type': 'pdf'
                }
                documents.append(Document(page_content=content, metadata=metadata))
            
        print(f"OCR successfully extracted text from {len(documents)} pages.")
        return documents
    except Exception as e:
        print(f"OCR Failed on {file_path}: {e}")
        return []
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_all_pdf(pdf_directory):
    """Load all PDF files from a directory recursively"""
    all_documents = []
    pdf_dir = Path(pdf_directory)

    pdf_files = list(pdf_dir.glob("**/*.pdf"))

    print(f"Found {len(pdf_files)} pdf files to process")

    for pdf_file in pdf_files:
        print(f"processing : {pdf_file.name}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            documents = loader.load()
            
            # Check if document is image-based (no raw text layer)
            if not documents or sum(len(doc.page_content.strip()) for doc in documents) == 0:
                print(f"No text found via standard loader. Using OCR on {pdf_file.name}...")
                documents = extract_text_with_ocr(str(pdf_file))

            for doc in documents:
                doc.metadata['source_file'] = pdf_file.name
                doc.metadata['file_type'] = 'pdf'

            all_documents.extend(documents)
            print(f"Loaded {len(documents)} pages")
        
        except Exception as e:
            print(f"Error : {e}")
        
        print(f"Total documents loaded : {len(all_documents)}")
    return all_documents


def process_all_txt(txt_directory):
    """Load all TXT files from a directory recursively"""
    all_documents = []
    txt_dir = Path(txt_directory)

    txt_files = list(txt_dir.glob("**/*.txt"))

    print(f"Found {len(txt_files)} txt files to process")

    for txt_file in txt_files:
        print(f"processing : {txt_file.name}")
        try:
            loader = TextLoader(str(txt_file), encoding='utf-8')
            documents = loader.load()
            
            for doc in documents:
                doc.metadata['source_file'] = txt_file.name
                doc.metadata['file_type'] = 'txt'
                doc.metadata['page'] = 1

            all_documents.extend(documents)
            print(f"Loaded {len(documents)} documents")
        
        except Exception as e:
            print(f"Error : {e}")
        
        print(f"Total documents loaded : {len(all_documents)}")
    return all_documents


    return all_documents


def process_all_docx(docx_directory):
    """Load all DOCX files from a directory recursively"""
    all_documents = []
    docx_dir = Path(docx_directory)
    docx_files = list(docx_dir.glob("**/*.docx"))

    print(f"Found {len(docx_files)} docx files to process")

    for docx_file in docx_files:
        print(f"processing : {docx_file.name}")
        try:
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(str(docx_file))
            documents = loader.load()
            
            for doc in documents:
                doc.metadata['source_file'] = docx_file.name
                doc.metadata['file_type'] = 'docx'
                doc.metadata['page'] = 1

            all_documents.extend(documents)
            print(f"Loaded {len(documents)} documents")
        
        except Exception as e:
            print(f"Error : {e}")
        
    print(f"Total documents loaded from DOCX : {len(all_documents)}")
    return all_documents


def process_all_pptx(pptx_directory):
    """Load all PPTX files from a directory recursively"""
    all_documents = []
    pptx_dir = Path(pptx_directory)
    pptx_files = list(pptx_dir.glob("**/*.pptx"))

    print(f"Found {len(pptx_files)} pptx files to process")

    for pptx_file in pptx_files:
        print(f"processing : {pptx_file.name}")
        try:
            docs = process_single_pptx(str(pptx_file))
            all_documents.extend(docs)
            print(f"Loaded {len(docs)} documents")
        except Exception as e:
            print(f"Error : {e}")
            
    print(f"Total documents loaded from PPTX : {len(all_documents)}")
    return all_documents


def process_single_pdf(file_path: str):
    """Load a single PDF file and return documents"""
    pdf_file = Path(file_path)
    print(f"processing single pdf : {pdf_file.name}")
    try:
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()
        
        # Check if document is image-based (no raw text layer)
        if not documents or sum(len(doc.page_content.strip()) for doc in documents) == 0:
            print(f"No text found via standard loader. Using OCR on {pdf_file.name}...")
            documents = extract_text_with_ocr(str(pdf_file))

        for doc in documents:
            doc.metadata['source_file'] = pdf_file.name
            doc.metadata['file_type'] = 'pdf'

        print(f"Loaded {len(documents)} pages from {pdf_file.name}")
        return documents
    
    except Exception as e:
        print(f"Error processing {pdf_file.name}: {e}")
        return []

def process_single_txt(file_path: str):
    """Load a single text file and return documents"""
    txt_file = Path(file_path)
    print(f"processing single txt : {txt_file.name}")
    try:
        loader = TextLoader(str(txt_file), encoding='utf-8')
        documents = loader.load()
        
        for doc in documents:
            doc.metadata['source_file'] = txt_file.name
            doc.metadata['file_type'] = 'txt'
            doc.metadata['page'] = 1 # Text files don't have pages, but we keep it for consistency

        print(f"Loaded text content from {txt_file.name}")
        return documents
    
    except Exception as e:
        print(f"Error processing {txt_file.name}: {e}")
        return []

def process_single_docx(file_path: str):
    """Load a single DOCX file and return documents"""
    docx_file = Path(file_path)
    print(f"processing single docx : {docx_file.name}")
    try:
        loader = Docx2txtLoader(str(docx_file))
        documents = loader.load()
        
        for doc in documents:
            doc.metadata['source_file'] = docx_file.name
            doc.metadata['file_type'] = 'docx'
            doc.metadata['page'] = 1

        print(f"Loaded DOCX content from {docx_file.name}")
        return documents
    
    except Exception as e:
        print(f"Error processing {docx_file.name}: {e}")
        return []


def process_single_pptx(file_path: str) -> List[Document]:
    """Extracts text from PPTX files using python-pptx"""
    try:
        from pptx import Presentation
        prs = Presentation(file_path)
        documents = []
        
        for i, slide in enumerate(prs.slides):
            text_runs = []
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
            
            # Also extract notes
            if slide.has_notes_slide:
                notes_text = slide.notes_slide.notes_text_frame.text
                if notes_text.strip():
                    text_runs.append(f"\n[Speaker Notes]: {notes_text}")
            
            content = "\n".join(text_runs)
            if content.strip():
                metadata = {
                    'source': str(file_path),
                    'page': i + 1,
                    'source_file': Path(file_path).name,
                    'file_type': 'pptx'
                }
                documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    except Exception as e:
        print(f"Error processing PPTX {file_path}: {e}")
        return []

def split_document(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200):
    """Split documents into chunks with overlap"""
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_spliter.split_documents(documents)
    print(f"split {len(documents)} documents into {len(split_docs)} chunks")

    if split_docs:
        print("Example Chunk: ")
        print(f"Content : {split_docs[0].page_content[:200]}")
        print(f"Metadata : {split_docs[0].metadata}")
    return split_docs
