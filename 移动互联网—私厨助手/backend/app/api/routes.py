from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserRequest, ChatRequest, ChatResponse, HistoryItem, FavoriteItem
from app.services.ai_service import AIService
from app.services.storage_service import StorageService
import json

router = APIRouter()

ai_service = AIService()

@router.post("/api/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    storage = StorageService(db)
    
    try:
        if request.user_request:
            user_req = request.user_request
            if "饮食计划" in user_req.goals or "三餐" in user_req.goals:
                result = ai_service.generate_diet_plan(
                    user_req.ingredients,
                    user_req.dietary_restrictions,
                    user_req.taste_preferences,
                    user_req.goals
                )
                conversation_id = storage.create_conversation(
                    title=f"饮食计划 - {', '.join(user_req.ingredients)[:20]}"
                )
                storage.add_message(conversation_id, "user", json.dumps(user_req.dict()))
                storage.add_message(conversation_id, "assistant", json.dumps(result))
                
                diet_plan = result.get("diet_plan", [])
                recipes = []
                for day in diet_plan:
                    if "breakfast" in day:
                        recipes.append(day["breakfast"])
                    if "lunch" in day:
                        recipes.append(day["lunch"])
                    if "dinner" in day:
                        recipes.append(day["dinner"])
                
                recipes = [normalize_recipe(r) for r in recipes]
                
                return {
                    "recipes": recipes,
                    "diet_plan": diet_plan,
                    "response_text": result.get("response_text", ""),
                    "conversation_id": conversation_id
                }
            else:
                result = ai_service.generate_recipes(
                    user_req.ingredients,
                    user_req.dietary_restrictions,
                    user_req.taste_preferences,
                    user_req.goals,
                    user_req.message
                )
                conversation_id = storage.create_conversation(
                    title=f"菜谱 - {', '.join(user_req.ingredients)[:20]}"
                )
                storage.add_message(conversation_id, "user", json.dumps(user_req.dict()))
                storage.add_message(conversation_id, "assistant", json.dumps(result))
                
                recipes = result.get("recipes", [])
                recipes = [normalize_recipe(r) for r in recipes]
                
                return {
                    "recipes": recipes,
                    "response_text": result.get("response_text", ""),
                    "conversation_id": conversation_id
                }
        else:
            if request.messages:
                conversation_id = request.messages[0].get("conversation_id", "")
                history = storage.get_conversation_messages(conversation_id) if conversation_id else []
                history.extend([{"role": m.role, "content": m.content} for m in request.messages])
                
                user_message = next((m.content for m in request.messages if m.role == "user"), "")
                result = ai_service.multi_turn_conversation(history, user_message)
                
                if conversation_id:
                    storage.add_message(conversation_id, "user", user_message)
                    storage.add_message(conversation_id, "assistant", json.dumps(result))
                else:
                    conversation_id = storage.create_conversation(title="多轮对话")
                    storage.add_message(conversation_id, "user", user_message)
                    storage.add_message(conversation_id, "assistant", json.dumps(result))
                
                recipes = result.get("recipes", [])
                recipes = [normalize_recipe(r) for r in recipes]
                
                return {
                    "recipes": recipes,
                    "response_text": result.get("response_text", ""),
                    "conversation_id": conversation_id
                }
        
        raise HTTPException(status_code=400, detail="Invalid request")
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

def normalize_recipe(recipe):
    if isinstance(recipe, dict):
        if "nutrition" in recipe and isinstance(recipe["nutrition"], dict):
            if "fiber" not in recipe["nutrition"]:
                recipe["nutrition"]["fiber"] = 0
        return recipe
    return recipe

@router.get("/api/history")
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    storage = StorageService(db)
    return storage.get_history(limit)

@router.delete("/api/history/{history_id}")
def delete_history(history_id: str, db: Session = Depends(get_db)):
    storage = StorageService(db)
    storage.delete_history(history_id)
    return {"message": "History deleted"}

@router.get("/api/favorites")
def get_favorites(db: Session = Depends(get_db)):
    storage = StorageService(db)
    return storage.get_favorites()

@router.post("/api/favorites")
def add_favorite(recipe_data: dict, db: Session = Depends(get_db)):
    storage = StorageService(db)
    recipe_id = recipe_data.get("id")
    recipe_name = recipe_data.get("name")
    
    if not recipe_id or not recipe_name:
        raise HTTPException(status_code=400, detail="Recipe ID and name are required")
    
    success = storage.add_favorite(recipe_id, recipe_name, recipe_data)
    return {"success": success, "message": "Added to favorites" if success else "Already in favorites"}

@router.delete("/api/favorites/{recipe_id}")
def remove_favorite(recipe_id: str, db: Session = Depends(get_db)):
    storage = StorageService(db)
    storage.remove_favorite(recipe_id)
    return {"message": "Removed from favorites"}

@router.get("/api/conversations")
def get_conversations(db: Session = Depends(get_db)):
    storage = StorageService(db)
    return storage.get_all_conversations()

@router.get("/api/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    storage = StorageService(db)
    return storage.get_conversation_messages(conversation_id)

@router.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    storage = StorageService(db)
    storage.delete_conversation(conversation_id)
    return {"message": "Conversation deleted"}
