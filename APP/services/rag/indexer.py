
import PyPDF2
from docx import Document
from app.services.embeddings.embedding_service import embed_documents
from app.services.vector_store.faiss_store import vector_store
from app.config import settings

async def index_documents(file):
    raw = await file.read()
    text = raw.decode(errors="ignore")

    chunks = [
        text[i:i+settings.CHUNK_SIZE]
        for i in range(0, len(text), settings.CHUNK_SIZE - settings.CHUNK_OVERLAP)
    ]

    embeddings = await embed_documents(chunks)
    metadata = [{"content": c, "source": file.filename} for c in chunks]
    vector_store.add_embeddings(embeddings, metadata)

    return {"chunks": len(chunks), "source": file.filename}
