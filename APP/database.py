from fastapi import APIRouter, Depends
from openai import AsyncOpenAI
from .config import settings
from .auth import get_current_user

router = APIRouter()
client = AsyncOpenAI(api_key=settings.openai_api_key)

@router.post("/chat")
async def chat(prompt: str, current_user=Depends(get_current_user)):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"reply": response.choices[0].message.content}
