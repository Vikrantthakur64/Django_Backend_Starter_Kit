
from openai import AsyncOpenAI
import numpy as np
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def embed_query(text: str):
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

async def embed_documents(texts):
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts
    )
    return [np.array(e.embedding, dtype=np.float32) for e in response.data]
