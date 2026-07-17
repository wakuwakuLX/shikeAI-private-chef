from pydantic import BaseModel
from typing import List, Optional

class RecipeIngredient(BaseModel):
    name: str
    amount: str

class RecipeStep(BaseModel):
    step: int
    description: str

class NutritionInfo(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None

class Recipe(BaseModel):
    id: str
    name: str
    ingredients: List[RecipeIngredient]
    steps: List[RecipeStep]
    nutrition: NutritionInfo
    tips: str
    suitable_for: str

class DietPlanDay(BaseModel):
    day: int
    breakfast: Recipe
    lunch: Recipe
    dinner: Recipe

class UserRequest(BaseModel):
    ingredients: List[str]
    dietary_restrictions: List[str]
    taste_preferences: List[str]
    goals: List[str]
    message: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: Optional[List[ChatMessage]] = None
    user_request: Optional[UserRequest] = None

class ChatResponse(BaseModel):
    recipes: List[Recipe]
    diet_plan: Optional[List[DietPlanDay]] = None
    response_text: str
    conversation_id: str

class HistoryItem(BaseModel):
    id: str
    conversation_id: str
    title: str
    content: str
    created_at: str

class FavoriteItem(BaseModel):
    id: str
    recipe_id: str
    recipe_name: str
    recipe_data: dict
    created_at: str
