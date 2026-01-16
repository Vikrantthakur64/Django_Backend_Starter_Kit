from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated

from . import utils, models, database, schemas

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserCreate, db: Annotated[Session, Depends(database.get_db)]):
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created"}

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                response: Response, 
                db: Annotated[Session, Depends(database.get_db)]):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = utils.create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True, 
        max_age=1800  # 30 min
    )
    return {"msg": "Login successful"}
