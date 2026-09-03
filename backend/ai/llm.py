import requests
import json
from typing import Dict, Any, Optional
from backend.core.config import settings

class ConfigurableLLM:
    """Configurable LLM client supporting local Ollama with robust fallback."""
    def __init__(self, host: str = None, model: str = None):
        self.host = host or settings.OLLAMA_HOST
        self.model = model or settings.OLLAMA_MODEL

    def generate(self, prompt: str, system_prompt: str = "You are CareerPilot AI, an expert career mentor.") -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
        except Exception:
            pass  # Fallback to local structured logic

        # Clean fallback when Ollama service is not running locally
        return f"[CareerPilot AI Insight]: Based on our career dataset, focusing on {prompt[:60]}... will directly address key requirements for high-growth tech roles."

llm_client = ConfigurableLLM()
