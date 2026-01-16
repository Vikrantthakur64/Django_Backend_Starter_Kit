
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.rag.generator import generate_answer
from app.services.rag.indexer import index_documents
from app.config import settings

app = FastAPI(
    title="RAG Application Kit",
    description="Production RAG system with FAISS vector store",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
async def health():
    return {"status": "ok", "vector_store": settings.VECTOR_DB_PATH}

@app.post("/rag/query")
async def query_rag(request: QueryRequest):
    answer = await generate_answer(request.question)
    return {
        "answer": answer["answer"],
        "sources": answer["sources"],
        "confidence": answer.get("confidence", 0.0)
    }

@app.post("/documents/index")
async def upload_documents(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(400, "Unsupported file type")
    return await index_documents(file)

@app.delete("/documents/clear")
async def clear_vector_store():
    from app.services.vector_store.faiss_store import clear_store
    clear_store()
    return {"status": "cleared"}
