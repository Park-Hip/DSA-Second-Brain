from src.agents.llm_client import LLMClient
from src.core.configs import settings
from src.core.logger import logger

def generate_theory(topic_name: str) -> str:
    """Uses LLM to generate the theory for a topic."""
    logger.info("Generating Theory", topic=topic_name)
    client = LLMClient()
    system_prompt = settings.config_yaml.get("tutor", {}).get("system_prompt", "Explain this topic.")
    user_prompt = f"Topic: {topic_name}"
    try:
        return client.generate_text(system_prompt, user_prompt)
    except Exception as e:
        logger.error("Failed to generate theory from Groq", error=str(e))
        raise
