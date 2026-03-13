import time
from typing import List, Dict, Any

from src.vector_store import VectorStore
from src.embedding import EmbeddingManager

class RAGRetrieval:
    """Retrieves documents from vector store based on query similarity"""
    
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
    
    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.35, source_filter: List[str] = None) -> List[Dict[str, Any]]:
        """Retrieve top-k most similar documents"""
        print(f"Retrieving documents for query : '{query}' ")
        print(f"Top_k : {top_k} , Score_threshold : {score_threshold}")

        query_embedding = self.embedding_manager.generate_embeddings([query], is_query=True)[0]
        
        try:
            query_kwargs = {
                "query_embeddings": [query_embedding.tolist()],
                "n_results": top_k
            }
            if source_filter:
                if len(source_filter) == 1:
                    query_kwargs["where"] = {"source_file": source_filter[0]}
                else:
                    query_kwargs["where"] = {"source_file": {"$in": source_filter}}
                    
            results = self.vector_store.collection.query(**query_kwargs)

            retrieved_docs = []
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]

                for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    # ChromaDB returns squared L2 distance. Typical matches are ~1.0 to ~1.4.
                    # We map this to a more intuitive 0-1 similarity score where 1.3 distance = ~85% confidence.
                    similarity_score = max(0.0, min(1.0, 1.5 - (distance / 2.0)))
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            'id': doc_id,
                            'content': document,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'distance': distance,
                            'rank': i + 1
                        })
                
                print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
            else:
                print("No documents found")
            
            return retrieved_docs
        except Exception as e:
            print(f"Error during retrieval {e}")
            return []


# ==================== RAG Pipelines ====================

def rag_simple(query, retriever, llm, top_k=3):
    """Simple RAG pipeline - retrieves context and generates answer"""
    results = retriever.retrieve(query, top_k=top_k)
    context = "\n\n".join([doc['content'] for doc in results]) if results else ""
    if not context:
        return "No relevant context found"
    
    prompt = f"""Use the following context to answer the question concisely.
Context:
{context}

Question: {query}

Answer:"""
    
    response = llm.invoke([prompt])
    return response.content


def rag_enhanced(query, retriever, llm, top_k=5, min_score=0.2, return_context=False, source_filter=None):
    """Enhanced RAG pipeline with sources and confidence"""
    results = retriever.retrieve(query, top_k=top_k, score_threshold=min_score, source_filter=source_filter)
    
    if not results:
        return {
            'answer': 'No relevant context found',
            'sources': [],
            'confidence': 0.0
        }
    
    context = "\n\n".join([doc['content'] for doc in results])
    
    sources = [{
        'source_file': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
        'page': doc['metadata'].get('page', 'unknown'),
        'similarity_score': doc['similarity_score'],
        'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content']
    } for doc in results]
    
    confidence = max([doc['similarity_score'] for doc in results]) if results else 0

    prompt = f"""Use the following context to answer the question concisely.
Context:
{context}

Question: {query}

Answer:"""
    
    response = llm.invoke([prompt])

    output = {
        'answer': response.content,
        'sources': sources,
        'confidence': confidence
    }
    
    if return_context:
        output['context'] = context

    return output


import json
import re

def generate_questions(difficulty, retriever, llm, num_questions=5, top_k=10, min_score=0.2, source_filter=None, topic=None, question_types=["MCQ"]):
    """Generates a mix of MCQs and True/False questions in JSON format"""
    
    # Use topic focus if provided, else generic concepts
    search_query = topic if topic and topic.strip() else "important concepts and key information"
    
    results = retriever.retrieve(search_query, top_k=top_k, score_threshold=min_score, source_filter=source_filter)
    
    if not results:
        return {
            'questions': [],
            'sources': []
        }
    
    context = "\n\n".join([doc['content'] for doc in results])
    
    type_str = " and ".join(question_types)
    
    prompt = f"""Based on the following context, generate {num_questions} questions at a {difficulty} difficulty level.
    The questions should be a mix of {type_str}.
    
    If "True/False" is requested, provide exactly 2 options: ["True", "False"].
    
    You MUST respond ONLY with a JSON array of objects. Each object must have:
    - "type": One of {question_types}
    - "question": The question text
    - "options": A list of possible answers (4 for MCQ, 2 for True/False)
    - "answer": The exact string of the correct answer from the options list
    - "explanation": A brief explanation of why this answer is correct based on the context
    
    Topic Focus: {search_query}
    
    Difficulty Context:
    - Easy: Factual recall, direct information.
    - Medium: Understanding, application, or comparison.
    - Hard: Analysis, synthesis, or evaluation of complex ideas.
    
    Context:
    {context}
    
    JSON Output:"""
    
    response = llm.invoke([prompt])
    
    try:
        # Clean response string to ensure valid JSON
        json_str = response.content
        if "```json" in json_str:
            json_str = re.search(r"```json\n(.*?)\n```", json_str, re.DOTALL).group(1)
        
        parsed_questions = json.loads(json_str)
        
        sources = [{
            'source_file': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
            'page': doc['metadata'].get('page', 'unknown'),
            'similarity_score': doc['similarity_score'],
            'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content']
        } for doc in results]

        return {
            "questions": parsed_questions,
            "sources": sources
        }
    except Exception as e:
        print(f"Error parsing JSON questions: {e}")
        return {
            "questions": [],
            "sources": []
        }

def generate_learning_content(mode, retriever, llm, top_k=20, source_filter=None, topic=None):
    """Generates summaries or key notes from documents"""
    
    query = topic if topic and topic.strip() else "general overview and main themes"
    results = retriever.retrieve(query, top_k=top_k, score_threshold=0.1, source_filter=source_filter)
    
    if not results:
        return "No relevant content found to summarize. Try selecting more sources or adjusting your topic."
        
    context = "\n\n".join([doc['content'] for doc in results])
    
    if mode == "Summary":
        prompt = f"Provide a detailed, professional, and well-structured summary of the following content. Use clear headings and sections.\n\nContext:\n{context}"
    else: # Key Notes
        prompt = f"Extract the most important key notes, facts, formulas, and bullet points from the content below. Organize them logically.\n\nContext:\n{context}"
        
    if topic:
        prompt += f"\n\nSpecifically focus all your attention on the topic: {topic}"
        
    response = llm.invoke([prompt])
    return response.content
