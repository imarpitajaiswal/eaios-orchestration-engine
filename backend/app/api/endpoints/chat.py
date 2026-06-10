from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from app.api.endpoints.auth import oauth2_scheme
from app.schemas.chat import ChatRequest
from app.agents.graph import app_graph
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/invoke")
def invoke_agent(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    """
    Secure entry point for the Multi-Agent OS.
    Injects the human message into the LangGraph state machine.
    """
    try:
        # 1. Format the strict payload required by the graph state
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # 2. Execute the deterministic graph cycle
        result = app_graph.invoke(inputs)
        
        # 3. Extract the final AI message from the state history
        ai_message = result["messages"][-1].content
        
        return {
            "status": "success", 
            "response": ai_message
        }
    except Exception as e:
        logger.error(f"Agent Execution Failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Intelligence Core Error")