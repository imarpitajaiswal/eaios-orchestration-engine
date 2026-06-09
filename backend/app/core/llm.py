from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_base_llm(temperature: float = 0.0) -> ChatOpenAI:
    """
    Instantiates the core enterprise reasoning engine.
    Temperature is locked to 0.0 for highly deterministic, factual agent routing.
    """
    return ChatOpenAI(
        model="gpt-4o",  # Standardize on the flagship omni model
        temperature=temperature,
        openai_api_key=settings.OPENAI_API_KEY,
        max_retries=3
    )

# Singleton instance for general orchestration tasks
llm_router = get_base_llm()