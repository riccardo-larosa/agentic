# import json
import logging

# import os
# from typing import Dict, List, Any, Optional, Union

from fastapi import FastAPI, HTTPException  # , Request
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.responses import FileResponse
# from pydantic import BaseModel, Field
# from sse_starlette.sse import EventSourceResponse
# import asyncio
# from typing import AsyncGenerator, Dict, List, Any

from src.graph import build_graph
from src.config import TEAM_MEMBER_CONFIGURATIONS

# from src.service.workflow_service import run_agent_workflow

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agentic API",
    description="API for Agentic LangGraph-based agent workflow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create the graph
graph = build_graph()


@app.get("/api/team_members")
async def get_team_members():
    """
    Get the configuration of all team members.

    Returns:
        dict: A dictionary containing team member configurations
    """
    try:
        return {"team_members": TEAM_MEMBER_CONFIGURATIONS}
    except Exception as e:
        logger.error(f"Error getting team members: {e}")
        raise HTTPException(status_code=500, detail=str(e))
