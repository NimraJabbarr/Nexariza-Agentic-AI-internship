"""
agents/__init__.py
-------------------
Shared resources for agents - OPTIMIZED FOR SPEED + RELIABILITY
Fast models first, slow models as fallback only.
"""

import os
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import TavilySearchTool

load_dotenv()

# --- API Keys ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()

def validate_keys() -> list[str]:
    """Validate API keys are present."""
    problems = []
    if not OPENROUTER_API_KEY:
        problems.append("OPENROUTER_API_KEY is missing. Get a free key at https://openrouter.ai/keys")
    if not TAVILY_API_KEY:
        problems.append("TAVILY_API_KEY is missing. Get a free key at https://app.tavily.com")
    return problems

# 🚀 FAST MODELS (tried first) + 🐢 SLOW MODELS (fallback only)
MODEL_LIST = [
    # ===== FAST TIER (1-2 sec per response) =====
    "openrouter/meta-llama/llama-3.1-8b-instruct:free",       # 1. Fastest, most reliable
    "openrouter/mistralai/mistral-7b-instruct:free",          # 2. Very fast, good quality
    "openrouter/google/gemma-2-9b-it:free",                   # 3. Google's model, fast
    "openrouter/microsoft/phi-3-mini-128k-instruct:free",     # 4. Microsoft mini, fast
    
    # ===== MEDIUM TIER (3-5 sec per response) =====
    "openrouter/microsoft/phi-3-medium-128k-instruct:free",   # 5. Good balance
    
    # ===== SLOW TIER (5-10 sec) - Fallback only =====
    "openrouter/meta-llama/llama-3.3-70b-instruct:free",      # 6. 70B (if fast fails)
    "openrouter/openai/gpt-oss-120b:free",                    # 7. 120B (if fast fails)
    
    # ===== LAST RESORT (always works) =====
    "openrouter/openrouter/free",                             # 8. Auto-router
]

class FallbackLLM:
    """Try each model in order until one works."""
    
    def __init__(self, model_list=MODEL_LIST, api_key=None, temperature=0.3):
        self.model_list = model_list
        self.api_key = api_key or OPENROUTER_API_KEY
        self.temperature = temperature
        self.failed_models = []
        
    def get_working_llm(self):
        """Try models in order until one works."""
        for model in self.model_list:
            if model in self.failed_models:
                continue
            try:
                print(f"🔄 Trying model: {model}")
                llm = LLM(
                    model=model,
                    api_key=self.api_key,
                    temperature=self.temperature,
                )
                # Quick test
                test = llm.invoke("Hello")
                if test:
                    print(f"✅ Model working: {model}")
                    return llm
            except Exception as e:
                print(f"❌ Model failed: {model}")
                self.failed_models.append(model)
                continue
        
        # Last resort
        print("⚠️ All models failed, using auto-router")
        return LLM(
            model="openrouter/openrouter/free",
            api_key=self.api_key,
            temperature=self.temperature,
        )

# --- Create shared LLM (tries fast models first) ---
try:
    shared_llm = FallbackLLM(temperature=0.3).get_working_llm()
except Exception:
    # ✅ FIXED: Proper fallback with api_key
    shared_llm = LLM(
        model="openrouter/meta-llama/llama-3.1-8b-instruct:free",
        api_key=OPENROUTER_API_KEY,  # ✅ Added missing api_key
        temperature=0.3,
        max_tokens=2048,
    )

# --- Shared Tavily search tool (Optimized for Speed) ---
search_tool = TavilySearchTool(
    api_key=TAVILY_API_KEY,
    max_results=4,  # ✅ 50% faster - 8 se 4 kar diya
)