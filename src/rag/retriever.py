
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

class Retriever:
    def __init__(self, collection_name="code_collection"):
        self.client = chromadb.Client()
        self.collection = self.client.get_collection(name=collection_name)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve_context(self, query: str, n_results: int = 5) -> List[str]:
        """Retrieves relevant context from the vector database."""
        query_embedding = self.model.encode([query])
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results['documents'][0]
