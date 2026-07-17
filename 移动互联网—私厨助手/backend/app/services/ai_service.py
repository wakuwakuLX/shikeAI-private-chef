import os
import json
import requests
from dotenv import load_dotenv
from app.utils.prompts import RECIPE_GENERATION_PROMPT, DIET_PLAN_PROMPT, MULTI_TURN_PROMPT

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class AIService:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip('/')
    
    def _repair_json(self, json_str):
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass
        
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        for _ in range(max(0, open_braces - close_braces)):
            json_str += '}'
        for _ in range(max(0, open_brackets - close_brackets)):
            json_str += ']'
        
        return json_str
    
    def _call_ollama(self, prompt, system_message=None):
        url = f"{self.base_url}/api/chat"
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 8192
            }
        }
        
        try:
            response = requests.post(url, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("message", {}).get("content", "").strip()
            
            print(f"AI Response Length: {len(content)}")
            print(f"AI Response (last 300 chars): {content[-300:] if len(content) > 300 else content}")
            
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                try:
                    data = json.loads(json_str)
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSON Parse Error after extraction: {e}")
                    print(f"Extracted JSON length: {len(json_str)}")
                    json_str = self._repair_json(json_str)
                    try:
                        data = json.loads(json_str)
                        print("JSON repair succeeded")
                        return data
                    except json.JSONDecodeError as e2:
                        return {"recipes": [], "response_text": f"解析失败: {str(e2)}"}
            else:
                return {"recipes": [], "response_text": content}
        except requests.exceptions.RequestException as e:
            return {"recipes": [], "response_text": f"网络请求失败: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"recipes": [], "response_text": f"解析失败: {str(e)}"}
        except Exception as e:
            return {"recipes": [], "response_text": f"生成失败: {str(e)}"}
    
    def generate_recipes(self, ingredients, dietary_restrictions, taste_preferences, goals, message=None):
        prompt = RECIPE_GENERATION_PROMPT.format(
            ingredients=", ".join(ingredients) if ingredients else "无",
            dietary_restrictions=", ".join(dietary_restrictions) if dietary_restrictions else "无",
            taste_preferences=", ".join(taste_preferences) if taste_preferences else "无",
            goals=", ".join(goals) if goals else "无",
            message=message if message else "无"
        )
        
        return self._call_ollama(prompt, "你是一位专业的私厨营养师AI助手")
    
    def generate_diet_plan(self, ingredients, dietary_restrictions, taste_preferences, goals):
        prompt = DIET_PLAN_PROMPT.format(
            ingredients=", ".join(ingredients) if ingredients else "无",
            dietary_restrictions=", ".join(dietary_restrictions) if dietary_restrictions else "无",
            taste_preferences=", ".join(taste_preferences) if taste_preferences else "无",
            goals=", ".join(goals) if goals else "无"
        )
        
        result = self._call_ollama(prompt, "你是一位专业的营养师AI助手")
        
        if "diet_plan" in result and isinstance(result["diet_plan"], list) and len(result["diet_plan"]) > 0:
            recipes = []
            for day in result["diet_plan"]:
                if "breakfast" in day:
                    recipes.append(day["breakfast"])
                if "lunch" in day:
                    recipes.append(day["lunch"])
                if "dinner" in day:
                    recipes.append(day["dinner"])
            result["recipes"] = recipes
        elif "recipes" not in result or not result["recipes"]:
            print("Diet plan failed, falling back to recipe generation")
            fallback_result = self.generate_recipes(ingredients, dietary_restrictions, taste_preferences, goals)
            result["recipes"] = fallback_result.get("recipes", [])
            result["response_text"] = fallback_result.get("response_text", "")
        
        return result
    
    def multi_turn_conversation(self, conversation_history, user_message):
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        prompt = MULTI_TURN_PROMPT.format(
            conversation_history=history_str,
            user_message=user_message
        )
        
        return self._call_ollama(prompt, "你是一位专业的私厨营养师AI助手")
