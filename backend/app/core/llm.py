import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Ensure local environment variables are loaded
load_dotenv()

def get_base_llm(temperature: float = 0.0) -> ChatGroq:
    """
    Instantiates the Groq enterprise reasoning engine using Llama 3 70B.
    Temperature is locked to 0.0 for highly deterministic, factual agent routing.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL: GROQ_API_KEY is missing from the environment.")

    return ChatGroq(
        model_name="llama-3.1-8b-instant",  # Upgraded to Meta's active 3.1 generation
        temperature=temperature,
        groq_api_key=api_key,
        max_retries=3
    )

# Singleton instance for general orchestration tasks
llm_router = get_base_llm()