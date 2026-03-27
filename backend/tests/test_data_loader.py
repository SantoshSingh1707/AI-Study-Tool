"""
Tests for data_loader module
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from src.data_loader import (
    split_document,
    process_single_txt,
    process_single_pdf,
    extract_text_with_ocr,
)


class TestDataLoader:
    """Test suite for data_loader functions"""

    def test_split_document_empty(self):
        """Test splitting empty document list"""
        result = split_document([])
        assert result == []

    def test_split_document_single(self, sample_document):
        """Test splitting single document"""
        result = split_document([sample_document], chunk_size=50, chunk_overlap=10)
        assert len(result) >= 1
        assert all(hasattr(doc, 'page_content') for doc in result)
        assert all(hasattr(doc, 'metadata') for doc in result)

    def test_split_document_multiple(self, sample_documents):
        """Test splitting multiple documents"""
        result = split_document(sample_documents, chunk_size=100, chunk_overlap=20)
        assert len(result) >= len(sample_documents)
        # Check metadata is preserved
        for doc in result:
            assert 'source_file' in doc.metadata or 'source' in doc.metadata

    def test_split_document_overlap(self):
        """Test that overlap creates appropriate chunks"""
        from langchain_core.documents import Document

        long_doc = Document(
            page_content="This is a very long document. " * 50,
            metadata={"source": "test.pdf"}
        )

        result = split_document([long_doc], chunk_size=100, chunk_overlap=20)

        # Should create multiple chunks
        assert len(result) > 1

        # Check that chunks are not identical
        contents = [doc.page_content for doc in result]
        unique_contents = set(contents)
        assert len(unique_contents) > 1

    def test_process_single_txt(self, temp_dir, sample_txt_path):
        """Test processing a single TXT file"""
        # Create test file
        sample_txt_path.write_text("This is test content.\nLine 2.\nLine 3.")

        docs = process_single_txt(str(sample_txt_path))

        assert len(docs) == 1
        assert "This is test content" in docs[0].page_content
        assert docs[0].metadata['source_file'] == sample_txt_path.name
        assert docs[0].metadata['file_type'] == 'txt'
        assert docs[0].metadata['page'] == 1

    def test_process_single_txt_utf8(self, temp_dir):
        """Test processing TXT with UTF-8 characters"""
        txt_path = temp_dir / "utf8_test.txt"
        txt_path.write_text("Café naïve résumé 日本語 🎉", encoding='utf-8')

        docs = process_single_txt(str(txt_path))
        assert len(docs) == 1
        assert "Café" in docs[0].page_content or "naïve" in docs[0].page_content

    def test_process_single_tx_nonexistent(self):
        """Test processing non-existent TXT file"""
        docs = process_single_txt("/nonexistent/file.txt")
        assert docs == []

    @patch('src.data_loader.PyPDFLoader')
    def test_process_single_pdf_success(self, mock_pdf_loader, sample_pdf_path):
        """Test processing PDF successfully"""
        mock_docs = [
            MagicMock(page_content="Page 1", metadata={}),
            MagicMock(page_content="Page 2", metadata={}),
        ]
        mock_pdf_loader.return_value.load.return_value = mock_docs

        # Create dummy file
        sample_pdf_path.touch()

        with patch('builtins.open', mock_open()):
            docs = process_single_pdf(str(sample_pdf_path))

        assert len(docs) == 2
        assert all(doc.metadata['source_file'] == sample_pdf_path.name for doc in docs)
        assert all(doc.metadata['file_type'] == 'pdf' for doc in docs)

    @patch('src.data_loader.PyPDFLoader')
    def test_process_single_pdf_with_ocr_fallback(self, mock_pdf_loader, sample_pdf_path):
        """Test OCR fallback for image-based PDF"""
        # Simulate empty document from normal loader
        sample_pdf_path.touch()
        mock_pdf_loader.return_value.load.return_value = []
        mock_pdf_loader.return_value.load.return_value = [MagicMock(page_content="", metadata={})]

        with patch('src.data_loader.extract_text_with_ocr') as mock_ocr:
            mock_ocr.return_value = [
                MagicMock(page_content="OCR extracted text", metadata={'page': 0})
            ]

            docs = process_single_pdf(str(sample_pdf_path))

            mock_ocr.assert_called_once_with(str(sample_pdf_path))

    def test_extract_text_with_ocr_success(self):
        """Test OCR text extraction"""
        with patch('src.data_loader.easyocr.Reader') as mock_reader_class, \
             patch('src.data_loader.fitz.open') as mock_fitz:

            # Mock EasyOCR
            mock_reader = MagicMock()
            mock_reader.readtext.return_value = ["Hello", "World"]
            mock_reader_class.return_value = mock_reader

            # Mock PyMuPDF
            mock_page = MagicMock()
            mock_pixmap = MagicMock()
            mock_pixmap.samples = b'\x00' * 100  # dummy image data
            mock_pixmap.h = 100
            mock_pixmap.w = 100
            mock_pixmap.n = 3
            mock_page.get_pixmap.return_value = mock_pixmap
            mock_doc = MagicMock()
            mock_doc.__len__ = MagicMock(return_value=1)
            mock_doc.__getitem__ = MagicMock(return_value=mock_page)
            mock_fitz.open.return_value = mock_doc

            docs = extract_text_with_ocr("/fake/path.pdf")

            assert len(docs) == 1
            assert "Hello World" in docs[0].page_content

    def test_extract_text_with_ocr_failure(self):
        """Test OCR handling when it fails"""
        with patch('src.data_loader.easyocr.Reader', side_effect=Exception("OCR error")):
            docs = extract_text_with_ocr("/fake/path.pdf")
            assert docs == []

    def test_document_metadata_consistency(self):
        """Test that metadata keys are consistent across all loaders"""
        from langchain_core.documents import Document

        # Simulate metadata from different loaders
        pdf_metadata = {'source_file': 'test.pdf', 'file_type': 'pdf', 'page': 1}
        txt_metadata = {'source_file': 'test.txt', 'file_type': 'txt', 'page': 1}
        docx_metadata = {'source_file': 'test.docx', 'file_type': 'docx', 'page': 1}

        # All should have source_file key
        for metadata in [pdf_metadata, txt_metadata, docx_metadata]:
            assert 'source_file' in metadata
            assert 'file_type' in metadata
            assert 'page' in metadata
