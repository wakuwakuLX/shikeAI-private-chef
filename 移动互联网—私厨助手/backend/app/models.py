from sqlalchemy import Column, String, Text, DateTime
from .database import Base
import datetime
import uuid

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HistoryRecord(Base):
    __tablename__ = "history_records"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FavoriteRecipe(Base):
    __tablename__ = "favorite_recipes"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    recipe_id = Column(String, index=True)
    recipe_name = Column(String, index=True)
    recipe_data = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
