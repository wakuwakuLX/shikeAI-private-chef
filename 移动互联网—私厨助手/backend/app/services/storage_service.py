import json
import uuid
from sqlalchemy.orm import Session
from app.models import Conversation, Message, HistoryRecord, FavoriteRecipe
import datetime

class StorageService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_conversation(self, title: str = "新对话") -> str:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation.id
    
    def update_conversation_title(self, conversation_id: str, title: str):
        conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.datetime.utcnow()
            self.db.commit()
    
    def add_message(self, conversation_id: str, role: str, content: str):
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
    
    def get_conversation_messages(self, conversation_id: str) -> list:
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    def get_all_conversations(self) -> list:
        conversations = self.db.query(Conversation).order_by(
            Conversation.updated_at.desc()
        ).all()
        return [{
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        } for conv in conversations]
    
    def delete_conversation(self, conversation_id: str):
        self.db.query(Message).filter(Message.conversation_id == conversation_id).delete()
        self.db.query(Conversation).filter(Conversation.id == conversation_id).delete()
        self.db.commit()
    
    def save_history(self, conversation_id: str, title: str, content: str):
        history = HistoryRecord(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            title=title,
            content=content,
            created_at=datetime.datetime.utcnow()
        )
        self.db.add(history)
        self.db.commit()
    
    def get_history(self, limit: int = 20) -> list:
        records = self.db.query(HistoryRecord).order_by(
            HistoryRecord.created_at.desc()
        ).limit(limit).all()
        return [{
            "id": record.id,
            "conversation_id": record.conversation_id,
            "title": record.title,
            "content": record.content,
            "created_at": record.created_at.isoformat()
        } for record in records]
    
    def delete_history(self, history_id: str):
        self.db.query(HistoryRecord).filter(HistoryRecord.id == history_id).delete()
        self.db.commit()
    
    def add_favorite(self, recipe_id: str, recipe_name: str, recipe_data: dict):
        existing = self.db.query(FavoriteRecipe).filter(
            FavoriteRecipe.recipe_id == recipe_id
        ).first()
        if existing:
            return False
        
        favorite = FavoriteRecipe(
            id=str(uuid.uuid4()),
            recipe_id=recipe_id,
            recipe_name=recipe_name,
            recipe_data=json.dumps(recipe_data, ensure_ascii=False),
            created_at=datetime.datetime.utcnow()
        )
        self.db.add(favorite)
        self.db.commit()
        return True
    
    def get_favorites(self) -> list:
        favorites = self.db.query(FavoriteRecipe).order_by(
            FavoriteRecipe.created_at.desc()
        ).all()
        return [{
            "id": fav.id,
            "recipe_id": fav.recipe_id,
            "recipe_name": fav.recipe_name,
            "recipe_data": json.loads(fav.recipe_data),
            "created_at": fav.created_at.isoformat()
        } for fav in favorites]
    
    def remove_favorite(self, recipe_id: str):
        self.db.query(FavoriteRecipe).filter(FavoriteRecipe.recipe_id == recipe_id).delete()
        self.db.commit()
    
    def is_favorite(self, recipe_id: str) -> bool:
        return self.db.query(FavoriteRecipe).filter(
            FavoriteRecipe.recipe_id == recipe_id
        ).first() is not None
