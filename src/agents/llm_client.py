import json
from groq import Groq
from typing import Dict, Any
from src.core.logger import logger
from src.core.configs import settings

class LLMClient:
    """
    A client that manages Grop API call
    """
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            logger.error("Warning: GROQ_API_KEY not found.")
            raise
        else:
            self.client = Groq(api_key=self.api_key)
        self.model = settings.config_yaml.get("groq", {}).get("model", "llama3-8b-8192")
        self.temp = settings.config_yaml.get("groq", {}).get("temperature", 0.0)

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Get JSON response from the Groq API.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model, 
                temperature=self.temp,
                response_format={"type": "json_object"}
            )   
            raw_content = chat_completion.choices[0].message.content
            return json.loads(raw_content)
        except Exception as e:
            logger.error("Error calling Groq API", error=str(e))
            raise

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Get text response from the Groq API.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model, 
                temperature=self.temp
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error("Error calling Groq API", error=str(e))
            raise

