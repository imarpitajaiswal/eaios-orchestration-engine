from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

def mock_intelligence_core(messages) -> AIMessage:
    """
    A lightweight, decoupled tactical bypass.
    Simulates the LLM response without triggering Pydantic validation walls.
    """
    return AIMessage(content="[MOCK AI]: The capital of France is Paris. (Note: Live OpenAI routing is currently bypassed for development).")

# We cast the standard Python function into a LangChain Runnable.
# To the LangGraph state machine, this looks and acts exactly like a live ChatOpenAI model.
llm_router = RunnableLambda(mock_intelligence_core)