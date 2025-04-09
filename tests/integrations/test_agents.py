import pytest
from src.agents.agents import create_agent, research_agent, coder_agent, browser_agent
from src.tools import (
    bash_tool,
    browser_tool,
    crawl_tool,
    python_repl_tool,
    tavily_tool,
)


def test_create_agent():
    """Test agent creation with custom tools and prompt"""
    tools = [bash_tool, python_repl_tool]
    agent = create_agent("coder", tools, "test_prompt")
    assert agent is not None
    assert hasattr(agent, "invoke")


def test_research_agent():
    """Test research agent creation and configuration"""
    assert research_agent is not None
    assert hasattr(research_agent, "invoke")


def test_coder_agent():
    """Test coder agent creation and configuration"""
    assert coder_agent is not None
    assert hasattr(coder_agent, "invoke")


def test_browser_agent():
    """Test browser agent creation and configuration"""
    assert browser_agent is not None
    assert hasattr(browser_agent, "invoke")


def test_create_agent_with_invalid_type():
    """Test agent creation with invalid agent type"""
    with pytest.raises(KeyError):
        create_agent("invalid_type", [], "test_prompt")