
from app.services.embeddings.embedding_service import embed_query
from app.services.vector_store.faiss_store import vector_store

async def retrieve_documents(query: str, k: int = 5):
    query_embedding = await embed_query(query)
    return vector_store.search(query_embedding, k)
