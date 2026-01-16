
import faiss
import numpy as np
import pickle
import os
from app.config import settings

class FAISSVectorStore:
    def __init__(self):
        self.index_path = f"{settings.VECTOR_DB_PATH}/faiss.index"
        self.metadata_path = f"{settings.VECTOR_DB_PATH}/metadata.pkl"
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(1536)
            self.metadata = []

    def add_embeddings(self, embeddings, metadata):
        self.index.add(np.stack(embeddings))
        self.metadata.extend(metadata)
        self._save()

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(query_embedding, k)
        return [
            {
                "content": self.metadata[i]["content"],
                "score": 1 - distances[0][idx]
            }
            for idx, i in enumerate(indices[0])
            if i < len(self.metadata)
        ]

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

vector_store = FAISSVectorStore()
