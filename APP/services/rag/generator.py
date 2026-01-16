
from openai import AsyncOpenAI
from app.services.rag.retriever import retrieve_documents
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_answer(question: str):
    docs = await retrieve_documents(question)
    context = "\n\n".join(d["content"] for d in docs)

    prompt = f"""
Answer using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": docs,
        "confidence": sum(d["score"] for d in docs) / len(docs)
    }
