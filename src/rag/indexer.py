
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

class Indexer:
    def __init__(self, collection_name="code_collection"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def index_documents(self, documents: List[str], metadatas: List[dict] = None):
        """Embeds and stores documents in the vector database."""
        embeddings = self.model.encode(documents)
        ids = [str(i) for i in range(len(documents))]
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
