from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from app.core.llm import llm_router

# 1. Define System State Schema
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], lambda old, new: old + new]

# 2. Define the Core Reasoning Node
def call_groq_engine(state: AgentState):
    """
    Executes the live Groq Llama 3 70B model against the current historical message state.
    """
    messages = state["messages"]
    
    # Optional: Inject an executive system prompt if the history is fresh
    if len(messages) == 1:
        messages = [
            HumanMessage(content="System Prompt: You are EAIOS, an advanced enterprise orchestration intelligence layer running Llama 3. Execute all commands with precision.")
        ] + messages

    response = llm_router.invoke(messages)
    return {"messages": [response]}

# 3. Assemble the Graph Architecture
workflow = StateGraph(AgentState)

# Add our processing node
workflow.add_node("agent_core", call_groq_engine)

# Wire the execution path
workflow.add_edge(START, "agent_core")
workflow.add_edge("agent_core", END)

# 4. Compile with a Persistent Memory Layer
memory = MemorySaver()
app_graph = workflow.compile(checkpointer=memory)