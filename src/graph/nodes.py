import logging
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate

from typing import Literal

from .types import State

logger = logging.getLogger(__name__)

def coordinator_node(state: State) -> Command[Literal[ "__end__"]]:
    """Coordinator node that communicate with customers."""
    logger.info("Coordinator talking.")
    # messages = apply_prompt_template("coordinator", state)
    # response = (
    #     get_llm_by_type(AGENT_LLM_MAP["coordinator"])
    #     .bind_tools([handoff_to_planner])
    #     .invoke(messages)
    # )
    logger.debug(f"Current state messages: {state['messages']}")

    goto = "__end__"
    # if len(response.tool_calls) > 0:
    #     goto = "planner"

    return Command(
        goto=goto,
    )
