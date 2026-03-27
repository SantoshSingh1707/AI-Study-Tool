import os
import uuid
import hashlib
import chromadb
import numpy as np
from typing import List, Any

class VectorStore:
    """ChromaDB Vector Store for document embeddings"""
    
    def __init__(self, collection_name: str = "pdf_documents", persist_directory: str = "data/vector_store"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.initialize_store()
    
    def initialize_store(self):
        """Initialize ChromaDB client and collection"""
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "PDF document embeddings for RAG"}
            )
            print(f"Vector store initialized. Collection : {self.collection_name}")
            print(f"Existing documents in collection : {self.collection.count()}")
        except Exception as e:
            print(f"Error while initializing vector store {e}")
            raise

    def get_available_sources(self) -> List[str]:
        """Get a list of unique source files in the vector store"""
        try:
            results = self.collection.get(include=['metadatas'])
            if not results['metadatas']:
                return []
            sources = set()
            for metadata in results['metadatas']:
                if metadata and 'source_file' in metadata:
                    sources.add(metadata['source_file'])
            return sorted(list(sources))
        except Exception as e:
            print(f"Error getting available sources: {e}")
            return []

    def remove_source(self, source_name: str) -> bool:
        """Remove all documents from a specific source file"""
        try:
            print(f"Removing documents from source: {source_name}")
            self.collection.delete(where={"source_file": source_name})
            print(f"Successfully removed source: {source_name}")
            return True
        except Exception as e:
            print(f"Error removing source {source_name}: {e}")
            return False

    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        """Add documents and embeddings to vector store with deduplication"""
        if not documents or len(documents) == 0:
            print("No documents to add to vector store.")
            return

        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match the number of embeddings")

        print(f"Processing {len(documents)} documents for addition...")

        # Generate hashes for all documents
        docs_with_hashes = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            content_hash = hashlib.sha256(doc.page_content.encode('utf-8')).hexdigest()[:16]
            docs_with_hashes.append((i, doc, embedding, content_hash))

        # Batch query to find existing hashes (in chunks to avoid overwhelming the query)
        all_hashes = [h for (_, _, _, h) in docs_with_hashes]
        existing_hashes = set()

        # Query in batches of 1000 to stay within limits
        batch_size_query = 1000
        for i in range(0, len(all_hashes), batch_size_query):
            hash_batch = all_hashes[i:i+batch_size_query]
            try:
                existing = self.collection.get(
                    where={"content_hash": {"$in": hash_batch}},
                    include=['metadatas']
                )
                if existing['metadatas']:
                    for meta in existing['metadatas']:
                        if 'content_hash' in meta:
                            existing_hashes.add(meta['content_hash'])
            except Exception as e:
                print(f"Warning: Could not check for existing duplicates: {e}")
                # Continue anyway - may add duplicates but allows operation

        # Filter out documents that already exist
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        skipped_count = 0

        for (i, doc, embedding, content_hash) in docs_with_hashes:
            if content_hash in existing_hashes:
                skipped_count += 1
                print(f"Skipping duplicate chunk (hash: {content_hash[:8]}...)")
                continue

            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)

            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['context_length'] = len(doc.page_content)
            metadata['content_hash'] = content_hash
            metadatas.append(metadata)

            documents_text.append(doc.page_content)
            embeddings_list.append(embedding.tolist())

        if not ids:
            print("All documents were duplicates. Nothing to add.")
            return

        print(f"Adding {len(ids)} new documents to vector store (skipped {skipped_count} duplicates)")

        # Batch addition
        batch_size_add = 5000
        for i in range(0, len(ids), batch_size_add):
            batch_ids = ids[i : i + batch_size_add]
            batch_embeddings = embeddings_list[i : i + batch_size_add]
            batch_metadatas = metadatas[i : i + batch_size_add]
            batch_documents = documents_text[i : i + batch_size_add]

            try:
                self.collection.add(
                    ids=batch_ids,
                    embeddings=batch_embeddings,
                    metadatas=batch_metadatas,
                    documents=batch_documents,
                )
                print(f"Successfully added batch {i//batch_size_add + 1} ({len(batch_ids)} documents)")
            except Exception as e:
                print(f"Error adding batch to vector store: {e}")
                raise

        print(f"Successfully added {len(ids)} documents to vector store")
        print(f"Total Documents in collection: {self.collection.count()}")
