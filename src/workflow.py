import logging

# from src.config import TEAM_MEMBER_CONFIGURATIONS, TEAM_MEMBERS
from src.config import TEAM_MEMBER_CONFIGURATIONS, TEAM_MEMBERS
# from src.graph import build_graph
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from src.graph.types import State
from src.graph.nodes import (
    supervisor_node,
    research_node,
    code_node,
    coordinator_node,
    browser_node,
    reporter_node,
    planner_node,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """Enable debug level logging for more detailed execution information."""
    logging.getLogger("src").setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

# Create the graph for LangGraph Cloud deployment
# This is the graph referenced in langgraph.json
# graph = build_graph()
memory = MemorySaver()
logger.info(f"TEAM_MEMBERS: {TEAM_MEMBERS}")
# logger.info(f"TEAM_MEMBER_CONFIGURATIONS: {TEAM_MEMBER_CONFIGURATIONS}")

# build state graph
builder = StateGraph(State)

# After State initialization, add this logging block
logger.info("=== State Class Status ===")
logger.info("Class Attributes:")
logger.info(f"  TEAM_MEMBERS: {getattr(State, 'TEAM_MEMBERS', 'Not Set')}")
logger.info(f"  TEAM_MEMBER_CONFIGURATIONS: {getattr(State, 'TEAM_MEMBER_CONFIGURATIONS', 'Not Set')}")
logger.info("Runtime Variables (Default Values):")
logger.info(f"  next: {getattr(State, 'next', 'Not Set')}")
logger.info(f"  full_plan: {getattr(State, 'full_plan', 'Not Set')}")
logger.info(f"  deep_thinking_mode: {getattr(State, 'deep_thinking_mode', 'Not Set')}")
logger.info(f"  search_before_planning: {getattr(State, 'search_before_planning', 'Not Set')}")
logger.info("Parent Class (MessagesState) Status:")
logger.info(f"  messages: {getattr(State, 'messages', 'Not Set')}")
logger.info("========================")

builder.add_edge(START, "coordinator")
builder.add_node("coordinator", coordinator_node)
builder.add_node("planner", planner_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("researcher", research_node)
builder.add_node("coder", code_node)
builder.add_node("browser", browser_node)
builder.add_node("reporter", reporter_node)
graph = builder.compile(checkpointer=memory)


# def run_agent_workflow(user_input: str, debug: bool = False):
#     """Run the agent workflow with the given user input.

#     Args:
#         user_input: The user's query or request
#         debug: If True, enables debug level logging

#     Returns:
#         The final state after the workflow completes
#     """
#     if not user_input:
#         raise ValueError("Input could not be empty")

#     if debug:
#         enable_debug_logging()

#     logger.info(f"Starting workflow with user input: {user_input}")
#     initial_state = {
#         # Constants
#         "TEAM_MEMBERS": TEAM_MEMBERS,
#         "TEAM_MEMBER_CONFIGURATIONS": TEAM_MEMBER_CONFIGURATIONS,
#         # Runtime Variables
#         "messages": [{"role": "user", "content": user_input}],
#         "deep_thinking_mode": True,
#         "search_before_planning": True,
#     }
#     config = {"configurable": {"thread_id": "default"}}
#     result = graph.invoke(input=initial_state, config=config)
#     logger.debug(f"Final workflow state: {result}")
#     logger.info("Workflow completed successfully")
#     return result


if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())
