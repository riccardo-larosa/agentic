import logging
import json
from copy import deepcopy
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.types import Command
# from langchain_core.prompts import ChatPromptTemplate
from src.llms.llm import get_llm_by_type
from src.prompts.template import apply_prompt_template
from src.config.agents import AGENT_LLM_MAP
from src.config import TEAM_MEMBERS
from src.utils.json_utils import repair_json_output
from src.tools.search import tavily_tool
from src.agents.agents import research_agent, coder_agent, browser_agent
from typing import Literal

from .types import State, Router

logger = logging.getLogger(__name__)

RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"


@tool
def handoff_to_planner():
    """Handoff to planner agent to do plan."""
    # This tool is not returning anything: we're just using it
    # as a way for LLM to signal that it needs to hand off to planner agent
    return


def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
    """Coordinator node that communicate with customers."""
    logger.info("Coordinator talking.")
    messages = apply_prompt_template("coordinator", state)
    response = (
        get_llm_by_type(AGENT_LLM_MAP["coordinator"])
        .bind_tools([handoff_to_planner])
        .invoke(messages)
    )
    logger.info(f"Current state messages: {state['messages']}")

    goto = "__end__"
    if len(response.tool_calls) > 0:
        goto = "planner"

    return Command(
        goto=goto,
    )


def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    """Planner node that generate the full plan."""
    logger.info("Planner generating full plan")
    messages = apply_prompt_template("planner", state)
    # whether to enable deep thinking mode
    llm = get_llm_by_type("basic")
    if state.get("deep_thinking_mode"):
        llm = get_llm_by_type("reasoning")
    if state.get("search_before_planning"):
        searched_content = tavily_tool.invoke({"query": state["messages"][-1].content})
        if isinstance(searched_content, list):
            messages = deepcopy(messages)
            messages[
                -1
            ].content += f"\n\n# Relative Search Results\n\n{json.dumps([{'title': elem['title'], 'content': elem['content']} for elem in searched_content], ensure_ascii=False)}"
        else:
            logger.error(
                f"Tavily search returned malformed response: {searched_content}"
            )
    stream = llm.stream(messages)
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    logger.info(f"Current state messages: {state['messages']}")
    logger.info(f"Planner response: {full_response}")

    goto = "supervisor"
    try:
        full_response = repair_json_output(full_response)
    except json.JSONDecodeError:
        logger.warning("Planner response is not a valid JSON")
        goto = "__end__"

    return Command(
        update={
            "messages": [HumanMessage(content=full_response, name="planner")],
            "full_plan": full_response,
        },
        goto=goto,
    )

def supervisor_node(state: State) -> Command[Literal["researcher", "coder", "browser", "reporter", "__end__"]]:
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")
    messages = apply_prompt_template("supervisor", state)
    # preprocess messages to make supervisor execute better.
    messages = deepcopy(messages)
    for message in messages:
        logger.warning(f"Message: {message}")
        if isinstance(message, BaseMessage) and message.name in TEAM_MEMBERS:
            message.content = RESPONSE_FORMAT.format(message.name, message.content)
    # response = (
    #     get_llm_by_type(AGENT_LLM_MAP["supervisor"])
    #     .with_structured_output(schema=Router, method="json_mode")
    #     .invoke(messages)
    # )
    
    # goto = response["next"]
    # Remove structured output and use regular completion
    response = get_llm_by_type(AGENT_LLM_MAP["supervisor"]).invoke(messages)
    
    # Parse the response to get the next agent
    try:
        response_dict = json.loads(response.content)
        goto = response_dict.get("next", "FINISH")
    except json.JSONDecodeError:
        logger.warning("Invalid JSON response from supervisor")
        goto = "FINISH"
        
    logger.info(f"Current state messages: {state['messages']}")
    logger.info(f"Supervisor response: {response}")

    if goto == "FINISH":
        goto = "__end__"
        logger.info("Workflow completed")
    else:
        logger.info(f"Supervisor delegating to: {goto}")

    return Command(goto=goto, update={"next": goto})

def research_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the researcher agent that performs research tasks."""
    logger.info("Research agent starting task")
    result = research_agent.invoke(state)
    logger.info("Research agent completed task")
    response_content = result["messages"][-1].content
    
    response_content = repair_json_output(response_content)
    logger.info(f"Research agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="researcher",
                )
            ]
        },
        goto="supervisor",
    )
    
def code_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the coder agent that executes Python code."""
    logger.info("Code agent starting task")
    result = coder_agent.invoke(state)
    logger.info("Code agent completed task")
    response_content = result["messages"][-1].content
    
    response_content = repair_json_output(response_content)
    logger.info(f"Code agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="coder",
                )
            ]
        },
        goto="supervisor",
    )
    

def browser_node(state: State) -> Command[Literal["supervisor"]]:
    """Node for the browser agent that performs web browsing tasks."""
    logger.info("Browser agent starting task")
    result = browser_agent.invoke(state)
    logger.info("Browser agent completed task")
    response_content = result["messages"][-1].content
    response_content = repair_json_output(response_content)
    logger.info(f"Browser agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="browser",
                )
            ]
        },
        goto="supervisor",
    )
    
def reporter_node(state: State) -> Command[Literal["supervisor"]]:
    """Reporter node that write a final report."""
    logger.info("Reporter write final report")
    messages = apply_prompt_template("reporter", state)
    response = get_llm_by_type(AGENT_LLM_MAP["reporter"]).invoke(messages)
    logger.info(f"Current state messages: {state['messages']}")
    response_content = response.content
    
    response_content = repair_json_output(response_content)
    logger.info(f"reporter response: {response_content}")

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="reporter",
                )
            ]
        },
        goto="supervisor",
    )