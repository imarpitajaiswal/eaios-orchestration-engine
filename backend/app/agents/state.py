from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The strict memory schema for the Multi-Agent OS.
    All agents in the graph will read and write to this single source of truth.
    """
    # The add_messages reducer ensures we append, not overwrite, conversation history
    messages: Annotated[list[AnyMessage], add_messages]
    
    # We will expand this state in later phases to include custom enterprise variables
    # like 'current_task', 'human_approval_required', etc.