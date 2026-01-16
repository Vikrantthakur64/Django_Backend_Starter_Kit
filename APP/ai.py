from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from openai import AsyncOpenAI
import stripe
from typing import Annotated

from . import config, database, models, utils
from .auth import get_current_user

router = APIRouter()
settings = config.settings
stripe.api_key = settings.stripe_secret_key
client = AsyncOpenAI(api_key=settings.openai_api_key)

class ChatRequest(BaseModel):
    message: str

@router.get("/me")
async def me(current_user=Depends(get_current_user), 
             db=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    return {"email": user.email, "credits": user.credits}

@router.post("/chat")
async def chat(request: ChatRequest, 
               current_user=Depends(get_current_user),
               db=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    if user.credits <= 0:
        raise HTTPException(status_code=402, detail="No credits left")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request.message}],
            max_tokens=500
        )
        reply = response.choices[0].message.content
        tokens_used = len(request.message) / 4 + 50  # Rough estimate
        
        user.credits -= tokens_used * 0.01  # $0.01 per token approx
        db.commit()
        
        return {"reply": reply, "credits_left": user.credits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
