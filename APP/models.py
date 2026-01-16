from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Float, default=100.0)  # Starting credits
    created_at = Column(String, server_default=func.now())
