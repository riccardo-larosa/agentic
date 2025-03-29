from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Constants
    TEAM_MEMBERS: list[str]
    TEAM_MEMBER_CONFIGURATIONS: dict[str, dict]

    # Runtime Variables
    next: str
    full_plan: str
    deep_thinking_mode: bool
    search_before_planning: bool
