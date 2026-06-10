from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.core.llm import llm_router

def call_model(state: AgentState):
    """
    The primary execution node. 
    Reads the current messages from the state, passes them to GPT-4o, 
    and returns the LLM's response to be appended to the state.
    """
    messages = state["messages"]
    response = llm_router.invoke(messages)
    
    # We return a dictionary that matches the AgentState schema.
    # The 'add_messages' reducer will handle appending this to the list.
    return {"messages": [response]}

# 1. Initialize the Graph Builder with our strict memory schema
workflow = StateGraph(AgentState)

# 2. Add our operational nodes (The "Workers")
workflow.add_node("agent", call_model)

# 3. Define the deterministic routing (The "Edges")
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# 4. Compile the enterprise state machine
# (Later, we will bind PostgreSQL here via LangGraph Checkpointers for persistent memory)
app_graph = workflow.compile()