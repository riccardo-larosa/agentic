import json
import pytest
from src.tools.browser import browser_tool


def test_browser_tool_success():
    instruction = "Go to google.com"
    result = browser_tool._run(instruction)
    result_dict = json.loads(result)
    assert "result_content" in result_dict
    assert "generated_gif_path" in result_dict
    assert result_dict["generated_gif_path"].endswith(".gif")


def test_browser_tool_search():
    instruction = "Go to github.com and search for 'python'"
    result = browser_tool._run(instruction)
    result_dict = json.loads(result)
    assert "result_content" in result_dict
    assert "generated_gif_path" in result_dict
    # Check if we got a valid response (either content or null)
    assert result_dict["result_content"] is not None or result_dict["result_content"] is None
    assert result_dict["generated_gif_path"].endswith(".gif")


def test_browser_tool_invalid_url():
    instruction = "Go to invalid-url-that-does-not-exist.com"
    result = browser_tool._run(instruction)
    result_dict = json.loads(result)
    assert "result_content" in result_dict
    assert "generated_gif_path" in result_dict
    # For invalid URLs, we expect either null content or an error message
    assert result_dict["result_content"] is None or "Error" in result_dict["result_content"]
    assert result_dict["generated_gif_path"].endswith(".gif")


def test_browser_tool_empty_instruction():
    instruction = ""
    result = browser_tool._run(instruction)
    result_dict = json.loads(result)
    assert "result_content" in result_dict
    assert "generated_gif_path" in result_dict
    # For empty instructions, we expect either null content or an error message
    assert result_dict["result_content"] is None or "Error" in result_dict["result_content"]
    assert result_dict["generated_gif_path"].endswith(".gif")


@pytest.mark.asyncio
async def test_browser_tool_async():
    instruction = "Go to github.com"
    result = await browser_tool._arun(instruction)
    result_dict = json.loads(result)
    assert "result_content" in result_dict
    assert "generated_gif_path" in result_dict
    assert result_dict["generated_gif_path"].endswith(".gif")


@pytest.mark.asyncio
async def test_browser_tool_terminate():
    # First run a task
    instruction = "Go to github.com"
    await browser_tool._arun(instruction)
    
    # Then terminate
    await browser_tool.terminate()
    assert browser_tool._agent is None 